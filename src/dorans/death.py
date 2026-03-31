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


def time_increase_factor(game_minutes: int | float) -> int | float:
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
    
    game_minutes += 0.5  # For some reason documented values are shifted by 0.5

    if game_minutes < 15:
        return 0
    elif game_minutes < 30:
        previous_increase = 0
        multiplier = 0.425
        milestone = 15
        factor = previous_increase + ceil(2 * (game_minutes - milestone)) * multiplier / 100
    elif game_minutes < 45:
        previous_increase = 0.1275
        multiplier = 0.3
        milestone = 30
        factor = previous_increase + ceil(2 * (game_minutes - milestone)) * multiplier / 100
    else:
        previous_increase = 0.2175
        multiplier = 1.45
        milestone = 45
        factor = previous_increase + ceil(2 * (game_minutes - milestone)) * multiplier / 100

    return min(0.5, factor)  # TIF is capped at 50%


def timer(
    level: int,
    game_minutes: int | float = 0,
) -> int | float:
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
