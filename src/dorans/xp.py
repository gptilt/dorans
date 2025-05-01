PER_LEVEL = lambda i: 100 * i + 80 if i > 1 else 0

PER_KILL_OR_ASSIST = {
    # By enemy level
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
    :param level: The level to get the XP for.
    :return: The XP required to reach the given level.
    """
    if level < 1 or level > 18:
        raise ValueError("Level must be between 1 and 18.")
    return sum(PER_LEVEL(i) for i in range(1, level + 1))


def level_from_xp(xp: int) -> int:
    """
    Get the level from the given XP.
    :param xp: The XP to determine the level for.
    :return: The level corresponding to the given XP.
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
    :param champion_level: The level of the champion participating in the takedown.
    :param enemy_level: The level of the enemy.
    :return: The XP multiplier for the takedown.
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
):
    """
    Get the XP from a kill.
    :param champion_level: The level of the champion participating in the kill.
    :param enemy_level: The level of the enemy.
    :return: The XP for the kill.
    """
    return (
        PER_KILL_OR_ASSIST[enemy_level][0]
        * takedown_multiplier(champion_level, enemy_level)
    )

def from_assist(
    champion_level: int,
    enemy_level: int,
    number_of_assists: int
):
    """
    Get the XP from an assist.
    :param champion_level: The level of the champion participating in the assist.
    :param enemy_level: The level of the enemy.
    :param number_of_assists: The number of assists.
    :return: The XP for the assist.
    """
    return (
        PER_KILL_OR_ASSIST[enemy_level][1]
        * takedown_multiplier(champion_level, enemy_level)
        / number_of_assists
    )


def from_dragon(dragon_level: int):
    """
    Get the XP from a dragon.
    :param dragon_level: The level of the dragon.
    :return: The XP for the dragon.

    TODO: From the Wiki:
    "If the team that slays a dragon has a lower average level
    than that of their opponents,
    they receive 25% bonus experience per average level difference.
    The bonus experience is sharply increased
    for the lowest level members of the team,
    equal to 15% per number of levels behind the dragon squared,
    up to a maximum of 200%."
    """
    return PER_DRAGON_LEVEL(dragon_level)


def from_elder_dragon(elder_dragon_level: int):
    """
    Get the XP from an elder dragon.
    :param elder_dragon_level: The level of the elder dragon.
    :return: The XP for the elder dragon.
    """
    return PER_ELDER_DRAGON_LEVEL(elder_dragon_level)


def from_grub(grub_level: int):
    """
    Get the XP from a grub.
    :param grub_level: The level of the grub.
        The Grub's level is the average of
        the two teams' levels at any point in the game.
    :return: The XP for the grub.
    """
    return PER_GRUB_LEVEL(grub_level)


def from_rift_herald(rift_herald_level: int):
    """
    Get the XP from a rift herald.
    :param rift_herald_level: The level of the rift herald.
        The Rift Herald's level is the average of
        the two teams' levels when she spawns at 14 minutes.
    :return: The XP for the rift herald.
    """
    return PER_RIFT_HERALD_LEVEL(rift_herald_level)


def from_baron(
    is_within_2000_units: bool
):
    """
    Get the XP from a baron.
    :param is_within_2000_units: Whether the champion is within 2000 units of the baron.
    :return: The XP for the baron.
    """
    return 1400 if is_within_2000_units == True else 600


def from_control_ward():
    """
    Get the XP from a control ward.
    :return: The XP for the control ward.
    """
    return 38.0  # Simplification: players can get assist XP from control wards
