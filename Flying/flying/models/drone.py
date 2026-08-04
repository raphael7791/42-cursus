"""Drone model for the simulation."""

from enum import Enum
from typing import Optional


class DroneState(Enum):
    """Possible states of a drone during simulation."""

    WAITING = "waiting"
    MOVING = "moving"
    IN_TRANSIT = "in_transit"
    ARRIVED = "arrived"


class Drone:
    """A drone navigating through the zone graph.

    Attributes:
        drone_id: Unique identifier (1-based).
        position: Current zone name.
        path: Planned path (list of zone names).
        state: Current state.
        path_index: Current position in the path.
        transit_target: Zone being transited to (for restricted).
        transit_from: Zone transiting from (for restricted).
    """

    def __init__(self, drone_id: int, start_zone: str) -> None:
        """Initialize a Drone.

        Args:
            drone_id: Unique identifier (1-based).
            start_zone: Name of the starting zone.
        """
        self.drone_id: int = drone_id
        self.position: str = start_zone
        self.path: list[str] = []
        self.state: DroneState = DroneState.WAITING
        self.path_index: int = 0
        self.transit_target: Optional[str] = None
        self.transit_from: Optional[str] = None

    def assign_path(self, path: list[str]) -> None:
        """Assign a path for this drone to follow.

        Args:
            path: List of zone names from start to end.
        """
        self.path = path
        self.path_index = 0
        self.state = DroneState.WAITING

    def next_zone(self) -> Optional[str]:
        """Get the next zone in the drone's path.

        Returns:
            Next zone name, or None if at end of path.
        """
        next_idx = self.path_index + 1
        if next_idx < len(self.path):
            return self.path[next_idx]
        return None

    def advance(self) -> None:
        """Move drone to the next position in its path."""
        self.path_index += 1
        if self.path_index < len(self.path):
            self.position = self.path[self.path_index]

    def has_arrived(self) -> bool:
        """Check if the drone has reached its destination.

        Returns:
            True if at the end of its path.
        """
        return self.state == DroneState.ARRIVED

    def label(self) -> str:
        """Return the display label for this drone.

        Returns:
            String like 'D1', 'D2', etc.
        """
        return f"D{self.drone_id}"

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"Drone({self.label()}, pos={self.position}, "
            f"state={self.state.value})"
        )
