"""Alchemy potions module."""
from alchemy.elements import create_earth, create_air
from elements import create_fire, create_water


def healing_potion() -> str:
    """Brew a healing potion."""
    return (
        f"Healing potion brewed with "
        f"'{create_earth()}' and '{create_air()}'"
    )


def strength_potion() -> str:
    """Brew a strength potion."""
    return (
        f"Strength potion brewed with "
        f"'{create_fire()}' and '{create_water()}'"
    )
