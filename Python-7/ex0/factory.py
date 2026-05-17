"""CreatureFactory abstract and concrete classes."""
from abc import ABC, abstractmethod
from ex0.creature import (
    Creature,
    Flameling,
    Pyrodon,
    Aquabub,
    Torragon,
)


class CreatureFactory(ABC):
    """Abstract factory for creating Creatures."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Create the base Creature of this family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create the evolved Creature of this family."""


class FlameFactory(CreatureFactory):
    """Factory for Fire family Creatures."""

    def create_base(self) -> Creature:
        """Create a Flameling."""
        return Flameling()

    def create_evolved(self) -> Creature:
        """Create a Pyrodon."""
        return Pyrodon()


class AquaFactory(CreatureFactory):
    """Factory for Water family Creatures."""

    def create_base(self) -> Creature:
        """Create an Aquabub."""
        return Aquabub()

    def create_evolved(self) -> Creature:
        """Create a Torragon."""
        return Torragon()
