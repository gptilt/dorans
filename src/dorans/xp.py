PER_LEVEL = lambda i: 100 * i + 80 if i > 1 else 0

PER_SOLO_KILL_OR_ASSISTED_KILL = {
    # Enemy Level: (Solo Kill XP, Assisted Kill XP)
    1: (42, 28),
    2: (114, 76),
    3: (144, 125),
    4: (174, 172),
    5: (204, 220),
    6: (234, 268),
    7: (308, 355.5),
    8: (392, 409.5),
    9: (486, 515),
    10: (590, 590),
    11: (640, 640),
    12: (690, 690),
    13: (740, 740),
    14: (790, 790),
    15: (840, 840),
    16: (890, 890),
    17: (940, 940),
    18: (990, 990)
}

PER_DRAGON_LEVEL = lambda i: 30 + i * 20 if i < 15 else 330
PER_ELDER_DRAGON_LEVEL = lambda i: 530 + i * 20 if i < 15 else 830
PER_GRUB_LEVEL = lambda i: 75 * 1.02 ** (i - 4)  # 2% increase per level over 4
PER_RIFT_HERALD_LEVEL = lambda i: 306 if i < 8 else 312  # Simplification


def total_from_level(level: int) -> int:
    """
    Get the XP required to reach the given level.
    Args:
        level (int): The level to get the XP for.
    Returns:
        int: The XP required to reach the given level.
    """
    if level < 1 or level > 18:
        raise ValueError("Level must be between 1 and 18.")
    return sum(PER_LEVEL(i) for i in range(1, level + 1))


def level_from_xp(xp: int) -> int:
    """
    Get the level from the given XP.
    Args:
        xp (int): The XP to determine the level for.
    Returns:
        int: The level corresponding to the given XP.
    """
    if xp < 0:
        raise ValueError("XP must be a non-negative integer.")
    
    for level in reversed(range(1, 19)):  # Levels are from 1 to 18
        total_xp = total_from_level(level)
        if xp >= total_xp:
            return level


def takedown_multiplier(
    champion_level: int,
    enemy_level: int,
) -> float:
    """
    Get the XP multiplier for a takedown.
    Args:
        champion_level (int): The level of the champion participating in the takedown.
        enemy_level (int): The level of the enemy.
    Returns:
        float: The XP multiplier for the takedown.
    """
    level_advantage = champion_level - enemy_level
    if level_advantage < -2:
        # Technically, level deficit is computed using decimals
        # So this is a simplification
        return 1.0 + 0.2 * -level_advantage
    elif level_advantage == 2 or level_advantage == 3:
        return 1.0 - 0.24 * (level_advantage - 1)
    elif level_advantage >= 4:
        return 0.4
    else:
        return 1.0


def from_kill(
    champion_level: int,
    enemy_level: int,
    number_of_assists: int = 0,
) -> float:
    """
    Get the takedown XP gained by a single player,
    from a solo kill or assisted kill.
    Args:
        champion_level (int): The level of the champion participating in the kill.
        enemy_level (int): The level of the enemy.
        number_of_assists (int): The number of players assisting the kill,
            not including the killer. By default, is 0, which implies a solo kill.
    Returns:
        float: The XP for the kill.
    """
    return (
        PER_SOLO_KILL_OR_ASSISTED_KILL[enemy_level][min(number_of_assists, 1)]
        * takedown_multiplier(champion_level, enemy_level)
    ) / (1 + number_of_assists)


def from_dragon(dragon_level: int) -> int:
    """
    Get the total XP gained from a dragon.
    Args:
        dragon_level (int): The level of the dragon.
    Returns:
        int: The total XP for the dragon.

    **TODO:** From the Wiki:
    "If the team that slays a dragon has a lower average level
    than that of their opponents,
    they receive 25% bonus experience per average level difference.
    The bonus experience is sharply increased
    for the lowest level members of the team,
    equal to 15% per number of levels behind the dragon squared,
    up to a maximum of 200%."
    """
    return PER_DRAGON_LEVEL(dragon_level)


def from_elder_dragon(elder_dragon_level: int) -> int:
    """
    Get the total XP gained from the Elder Dragon.
    Args:
        elder_dragon_level (int): The level of the Elder Dragon.
    Returns:
        int: The total XP for the Elder Dragon.
    """
    return PER_ELDER_DRAGON_LEVEL(elder_dragon_level)


def from_grub(grub_level: int) -> int:
    """
    Get the total XP from a single grub.
    Args:
        grub_level (int): The level of the grub.
            The Grub's level is the average of
            the two teams' levels at any point in the game.
    Returns:
        int: The total XP for the grub.
    """
    return PER_GRUB_LEVEL(grub_level)


def from_rift_herald(rift_herald_level: int) -> int:
    """
    Get the total XP gained from Rift Herald.
    Args:
        rift_herald_level: The level of the Rift Herald.
            The Rift Herald's level is the average of
            the two teams' levels when she spawns at 14 minutes.
    Returns:
        int: The total XP for the Rift Herald.
    """
    return PER_RIFT_HERALD_LEVEL(rift_herald_level)


def from_baron(is_within_2000_units: bool) -> int:
    """
    Get the total XP gained from Baron Nashor.
    Args:
        is_within_2000_units (bool): Whether the champion is within 2000 units of the baron.
    Returns:
        int: The total XP for the Baron Nashor.
    """
    return 1400 if is_within_2000_units == True else 600


def from_control_ward() -> float:
    """
    Get the total XP from a control ward.
    Returns:
        float: The XP for the control ward.
    """
    return 38.0  # Simplification: players can get assist XP from control wards
