"""Dark spellbook module."""
from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    """Return allowed ingredients for dark magic."""
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    """Record a dark spell after validation."""
    result: str = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
