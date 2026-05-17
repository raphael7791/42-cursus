"""Concrete Creatures with capabilities."""
from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    """Base Grass Creature with healing."""

    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def attack(self) -> str:
        """Perform Vine Whip attack."""
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        """Heal for a small amount."""
        return f"{self.name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    """Evolved Grass/Fairy Creature with healing."""

    def __init__(self) -> None:
        super().__init__("Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        """Perform Petal Dance attack."""
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        """Heal self and others."""
        return f"{self.name} heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    """Base Normal Creature with transform."""

    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
        self.is_transformed: bool = False

    def attack(self) -> str:
        """Attack, boosted if transformed."""
        if self.is_transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        """Shift into a sharper form."""
        self.is_transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        """Return to normal."""
        self.is_transformed = False
        return f"{self.name} returns to normal."


class Morphagon(Creature, TransformCapability):
    """Evolved Normal/Dragon Creature with transform."""

    def __init__(self) -> None:
        super().__init__("Morphagon", "Normal/Dragon")
        self.is_transformed: bool = False

    def attack(self) -> str:
        """Attack, devastating if transformed."""
        if self.is_transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        """Morph into dragonic battle form."""
        self.is_transformed = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        """Stabilize form."""
        self.is_transformed = False
        return f"{self.name} stabilizes its form."
