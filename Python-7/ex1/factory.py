"""Factories for Creatures with capabilities."""
from ex0.creature import Creature
from ex0.factory import CreatureFactory
from ex1.creatures import Sproutling, Bloomelle, Shiftling, Morphagon


class HealingCreatureFactory(CreatureFactory):
    """Factory for Grass family Creatures with healing."""

    def create_base(self) -> Creature:
        """Create a Sproutling."""
        return Sproutling()

    def create_evolved(self) -> Creature:
        """Create a Bloomelle."""
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    """Factory for Normal family Creatures with transform."""

    def create_base(self) -> Creature:
        """Create a Shiftling."""
        return Shiftling()

    def create_evolved(self) -> Creature:
        """Create a Morphagon."""
        return Morphagon()
