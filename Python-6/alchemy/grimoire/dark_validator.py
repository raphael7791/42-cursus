"""Dark validator module."""
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    """Validate ingredients for dark magic."""
    allowed: list[str] = dark_spell_allowed_ingredients()
    ingredients_lower: str = ingredients.lower()
    for item in allowed:
        if item in ingredients_lower:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
