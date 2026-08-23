"""Connection model for the drone simulation graph."""


class Connection:
    """A bidirectional connection (edge) between two zones.

    Attributes:
        zone_a: Name of the first zone.
        zone_b: Name of the second zone.
        max_link_capacity: Maximum drones traversing simultaneously.
    """

    def __init__(
        self,
        zone_a: str,
        zone_b: str,
        max_link_capacity: int = 1,
    ) -> None:
        """Initialize a Connection.

        Args:
            zone_a: Name of the first zone.
            zone_b: Name of the second zone.
            max_link_capacity: Max simultaneous traversals (default: 1).
        """
        self.zone_a: str = zone_a
        self.zone_b: str = zone_b
        self.max_link_capacity: int = max_link_capacity

    def key(self) -> tuple[str, str]:
        """Return a canonical key for this connection.

        Returns:
            Sorted tuple of zone names.
        """
        if self.zone_a < self.zone_b:
            return (self.zone_a, self.zone_b)
        return (self.zone_b, self.zone_a)

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"Connection({self.zone_a}-{self.zone_b}, "
            f"cap={self.max_link_capacity})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Connection):
            return NotImplemented
        return self.key() == other.key()

    def __hash__(self) -> int:
        """Hash by canonical key."""
        return hash(self.key())
