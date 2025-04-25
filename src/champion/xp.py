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


def from_event(
    event: str,
    **kwargs: dict[str, int]
) -> int:
    """
    Get the XP from the given event.
    :param event: The event to get the XP for.
    :return: The XP for the given event.
    """
    match event:
        case "kill":
            champion_level = kwargs["champion_level"]
            enemy_level = kwargs["enemy_level"]
            return (
                PER_KILL_OR_ASSIST[enemy_level][0]
                * takedown_multiplier(champion_level, enemy_level)
            )
        case "assist":
            champion_level = kwargs["champion_level"]
            enemy_level = kwargs["enemy_level"]
            return (
                PER_KILL_OR_ASSIST[enemy_level][1]
                * takedown_multiplier(champion_level, enemy_level)
                / kwargs["number_of_assists"]
            )
        case "dragon":
            dragon_level = kwargs["dragon_level"]
            return PER_DRAGON_LEVEL(dragon_level)
        case "elder_dragon":
            elder_dragon_level = kwargs["elder_dragon_level"]
            return PER_ELDER_DRAGON_LEVEL(elder_dragon_level)
        case "rift_herald":
            # The Rift Herald's level is the average of the two teams' levels
            # when she spawns at 14 minutes
            rift_herald_level = kwargs["rift_herald_level"]
            return PER_RIFT_HERALD_LEVEL(rift_herald_level)
        case "baron":
            is_within_2000_units = kwargs.get("is_within_2000_units", False)
            return 1400 if is_within_2000_units == True else 600
        case _:
            raise ValueError(f"Unknown event: {event}")
