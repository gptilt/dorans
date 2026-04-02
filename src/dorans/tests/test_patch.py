from datetime import datetime, timezone
from dorans import patch

def test_get_patches():
    expected = {
        "9.21": datetime(2019, 10, 23, 8, 37, 4, tzinfo=timezone.utc),
        "16.6": datetime(2026, 3, 18, 5, 58, 42, tzinfo=timezone.utc)
    }
    patches = patch.get_patches()
    assert patches['9.21'] == expected['9.21']
    assert patches['16.6'] == expected['16.6']