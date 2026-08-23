"""Zone model for the drone simulation graph."""

from enum import Enum
from typing import Optional


class ZoneType(Enum):
    """Types of zones in the simulation graph."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    """A zone (node) in the simulation graph.

    Attributes:
        name: Unique identifier for the zone.
        x: X coordinate.
        y: Y coordinate.
        zone_type: Type of zone affecting movement cost.
        color: Optional color for visualization.
        max_drones: Maximum drones allowed simultaneously.
        is_start: Whether this is the start hub.
        is_end: Whether this is the end hub.
    """

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: Optional[str] = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Initialize a Zone.

        Args:
            name: Unique identifier for the zone.
            x: X coordinate.
            y: Y coordinate.
            zone_type: Type of zone (default: NORMAL).
            color: Optional color for visualization.
            max_drones: Maximum simultaneous drones (default: 1).
            is_start: Whether this is the start hub.
            is_end: Whether this is the end hub.
        """
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: ZoneType = zone_type
        self.color: Optional[str] = color
        self.max_drones: int = max_drones
        self.is_start: bool = is_start
        self.is_end: bool = is_end

    def movement_cost(self) -> float:
        """Return the movement cost to enter this zone.

        Returns:
            Cost to enter this zone.
        """
        if self.zone_type == ZoneType.PRIORITY:
            return 0.5
        if self.zone_type == ZoneType.RESTRICTED:
            return 2.0
        return 1.0

    def is_accessible(self) -> bool:
        """Check if drones can enter this zone.

        Returns:
            True if the zone is not blocked.
        """
        return self.zone_type != ZoneType.BLOCKED

    def has_unlimited_capacity(self) -> bool:
        """Check if this zone has unlimited capacity.

        Returns:
            True if start or end hub.
        """
        return self.is_start or self.is_end

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Zone({self.name}, {self.zone_type.value})"

    def __eq__(self, other: object) -> bool:
        """Check equality by name."""
        if not isinstance(other, Zone):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash by name."""
        return hash(self.name)
