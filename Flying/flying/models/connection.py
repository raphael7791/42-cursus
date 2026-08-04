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

    def connects(self, name_a: str, name_b: str) -> bool:
        """Check if this connection links the two given zones.

        Args:
            name_a: First zone name.
            name_b: Second zone name.

        Returns:
            True if the connection links these zones in either direction.
        """
        return (
            (self.zone_a == name_a and self.zone_b == name_b)
            or (self.zone_a == name_b and self.zone_b == name_a)
        )

    def other(self, zone_name: str) -> str:
        """Return the zone on the other end of the connection.

        Args:
            zone_name: Name of one zone.

        Returns:
            Name of the other zone.

        Raises:
            ValueError: If zone_name is not part of this connection.
        """
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(
            f"Zone '{zone_name}' is not part of connection "
            f"{self.zone_a}-{self.zone_b}"
        )

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
