"""Capability abstract classes for Creatures."""
from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Abstract capability for healing."""

    @abstractmethod
    def heal(self) -> str:
        """Perform a healing action."""


class TransformCapability(ABC):
    """Abstract capability for transformation."""

    is_transformed: bool

    @abstractmethod
    def transform(self) -> str:
        """Transform into a different form."""

    @abstractmethod
    def revert(self) -> str:
        """Revert to the original form."""
