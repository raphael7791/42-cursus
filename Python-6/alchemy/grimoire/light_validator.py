"""Light validator module."""
from alchemy.grimoire.light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    """Validate ingredients for light magic."""
    allowed: list[str] = light_spell_allowed_ingredients()
    ingredients_lower: str = ingredients.lower()
    for item in allowed:
        if item in ingredients_lower:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
