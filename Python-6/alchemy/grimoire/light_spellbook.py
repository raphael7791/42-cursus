"""Light spellbook module."""
from typing import List


def light_spell_allowed_ingredients() -> List[str]:
    """Return allowed ingredients for light magic."""
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    """Record a light spell after validation."""
    from alchemy.grimoire.light_validator import validate_ingredients
    result: str = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
