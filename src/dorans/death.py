from math import ceil

BASE_RESPAWN_WAIT_TIME_PER_LEVEL = {
    1: 10,
    2: 10,
    3: 12,
    4: 12,
    5: 14,
    6: 16,
    7: 20,
    8: 25,
    9: 28,
    10: 32.5,
    11: 35,
    12: 37.5,
    13: 40,
    14: 42.5,
    15: 45,
    16: 47.5,
    17: 50,
    18: 52.5
}


def time_increase_factor(game_minutes: float) -> float:
    """
    Calculate the time increase factor based on the game time.
    Reference: https://wiki.leagueoflegends.com/en-us/Death
    Args:
        game_time (float): The current game time in minutes, in decimal form.
    Returns:
        float: The time increase factor.
    """
    if game_minutes < 0:
        raise ValueError("Game time cannot be negative.")

    def tif(game_minutes, multiplier, milestone):
        previous_increase = tif(milestone, multiplier, milestone - 15) if milestone > 15 else 0
        return previous_increase + ceil(2 * (game_minutes - milestone)) * multiplier / 100

    if game_minutes < 15:
        return 0
    elif game_minutes < 30:
        multiplier = 0.425
        milestone = 15
        factor = tif(game_minutes, multiplier, milestone)
    elif game_minutes < 45:
        multiplier = 0.3
        milestone = 30
        factor = tif(game_minutes, multiplier, milestone)
    else:
        multiplier = 1.45
        milestone = 45
        factor = tif(game_minutes, multiplier, milestone)

    return min(0.5, factor)  # TIF is capped at 50%


def timer(
    level: int,
    game_minutes: float = 0,
) -> float:
    """
    Calculate the death timer based on the player's level.
    Args:
        level (int): The player's level.
    Returns:
        float: The death timer in seconds.
    """
    if level < 1 or level > 18:
        raise ValueError("Level must be between 1 and 18.")
    
    return BASE_RESPAWN_WAIT_TIME_PER_LEVEL[level] * (1 + time_increase_factor(game_minutes))
