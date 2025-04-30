from dorans import death
import pytest

def test_time_increase_factor_negative():
    with pytest.raises(ValueError):
        death.time_increase_factor(-1)

def test_timer_basic():
    level = 5
    game_minutes = 0
    expected = death.BASE_RESPAWN_WAIT_TIME_PER_LEVEL[level]
    assert death.timer(level, game_minutes) == expected

def test_timer_with_max_death_time():
    level = 18
    game_minutes = 55
    max_death_time = 78.75
    assert death.timer(level, game_minutes) == max_death_time

def test_timer_invalid_level():
    with pytest.raises(ValueError):
        death.timer(0)
    with pytest.raises(ValueError):
        death.timer(19)
