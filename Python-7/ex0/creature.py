"""Creature abstract and concrete classes."""
from abc import ABC, abstractmethod


class Creature(ABC):
    """Abstract base class for all Creatures."""

    def __init__(self, name: str, creature_type: str) -> None:
        self.name: str = name
        self.creature_type: str = creature_type

    @abstractmethod
    def attack(self) -> str:
        """Perform an attack."""

    def describe(self) -> str:
        """Return a description of the Creature."""
        return f"{self.name} is a {self.creature_type} type Creature"


class Flameling(Creature):
    """Base Fire Creature."""

    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        """Perform Ember attack."""
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    """Evolved Fire/Flying Creature."""

    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        """Perform Flamethrower attack."""
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    """Base Water Creature."""

    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        """Perform Water Gun attack."""
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    """Evolved Water Creature."""

    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        """Perform Hydro Pump attack."""
        return f"{self.name} uses Hydro Pump!"
