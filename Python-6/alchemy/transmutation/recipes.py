"""Transmutation recipes module."""
from alchemy.potions import strength_potion
from ..elements import create_air
from elements import create_fire


def lead_to_gold() -> str:
    """Transmute lead into gold."""
    return (
        f"Recipe transmuting Lead to Gold: "
        f"brew '{create_air()}' and "
        f"'{strength_potion()}' "
        f"mixed with '{create_fire()}'"
    )
