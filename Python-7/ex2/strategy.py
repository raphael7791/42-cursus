"""Battle strategy abstract and concrete classes."""
from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """Raised when a Creature is not suitable for a strategy."""


class BattleStrategy(ABC):
    """Abstract base class for battle strategies."""

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Execute the strategy for the given Creature."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Check if the Creature is suitable for this strategy."""


class NormalStrategy(BattleStrategy):
    """Strategy that simply attacks."""

    def is_valid(self, creature: Creature) -> bool:
        """Any Creature can use the normal strategy."""
        return True

    def act(self, creature: Creature) -> None:
        """Just attack."""
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """Strategy that transforms, attacks, then reverts."""

    def is_valid(self, creature: Creature) -> bool:
        """Only Creatures with TransformCapability."""
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        """Transform, attack, revert."""
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this aggressive strategy"
            )
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    """Strategy that attacks then heals."""

    def is_valid(self, creature: Creature) -> bool:
        """Only Creatures with HealCapability."""
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        """Attack then heal."""
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this defensive strategy"
            )
        print(creature.attack())
        if isinstance(creature, HealCapability):
            print(creature.heal())
