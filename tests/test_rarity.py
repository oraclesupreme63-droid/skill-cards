import pytest

from app.core.rarity import calculate_rarity


@pytest.mark.parametrize(
    "level,expected",
    [
        (1, "bronce"),
        (20, "bronce"),
        (21, "plata"),
        (40, "plata"),
        (41, "oro"),
        (60, "oro"),
        (61, "platino"),
        (80, "platino"),
        (81, "dios"),
        (100, "dios"),
    ],
)
def test_calculate_rarity(level, expected):
    assert calculate_rarity(level) == expected
