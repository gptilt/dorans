from dorans import xp
import pytest


def test_level_from_xp_raises_on_negative():
    with pytest.raises(ValueError):
        xp.level_from_xp(-100)


def test_level_from_xp_inverts_total_from_level():
    for level in range(1, 19):
        _xp = xp.total_from_level(level)
        assert xp.level_from_xp(_xp) == level


def test_total_from_level_raises_out_of_bounds():
    with pytest.raises(ValueError):
        xp.total_from_level(0)
    with pytest.raises(ValueError):
        xp.total_from_level(19)


def test_from_kill_and_assist_return_positive():
    kill_xp_lvl1 = xp.from_kill(champion_level=1, enemy_level=1)
    assist_xp_lvl1 = xp.from_kill(champion_level=1, enemy_level=1, number_of_assists=1)

    assert kill_xp_lvl1 > 0
    assert assist_xp_lvl1 > 0
    assert kill_xp_lvl1 > assist_xp_lvl1

    kill_xp_lvl6 = xp.from_kill(champion_level=6, enemy_level=6)
    assist_xp_lvl6 = xp.from_kill(champion_level=6, enemy_level=6, number_of_assists=2)
    assert assist_xp_lvl6 * 3 > kill_xp_lvl6
    

def test_from_dragon_returns_positive_xp():
    _xp = xp.from_dragon(dragon_level=14)
    assert _xp > 0

def test_from_dragon_raises_if_level_too_low():
    with pytest.raises(AssertionError):
        xp.from_dragon(dragon_level=0)
