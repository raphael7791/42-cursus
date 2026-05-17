"""ex0 package — exposes only factories, not concrete Creatures."""
from ex0.factory import CreatureFactory  # noqa: F401
from ex0.factory import FlameFactory  # noqa: F401
from ex0.factory import AquaFactory  # noqa: F401

__all__ = ["CreatureFactory", "FlameFactory", "AquaFactory"]
