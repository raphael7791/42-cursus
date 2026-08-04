"""Terminal visualizer for the drone simulation."""

from typing import Optional

from flying.models.graph import Graph
from flying.models.drone import Drone, DroneState


ANSI_COLORS: dict[str, str] = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "orange": "\033[33m",
    "purple": "\033[35m",
    "gray": "\033[90m",
    "gold": "\033[93m",
    "lime": "\033[92m",
    "brown": "\033[33m",
    "crimson": "\033[91m",
    "violet": "\033[95m",
    "maroon": "\033[31m",
    "darkred": "\033[31m",
    "black": "\033[90m",
    "rainbow": "\033[96m",
}
RESET: str = "\033[0m"
BOLD: str = "\033[1m"
DIM: str = "\033[2m"


class Visualizer:
    """Terminal-based visualizer for drone simulation.

    Displays the graph, drone positions, and simulation stats
    using ANSI color codes.
    """

    def __init__(self, graph: Graph) -> None:
        """Initialize the Visualizer.

        Args:
            graph: The simulation graph.
        """
        self.graph: Graph = graph

    def display_graph(self) -> None:
        """Display the graph structure with zone info."""
        print(f"\n{BOLD}=== Graph Structure ==={RESET}")
        print(
            f"Zones: {len(self.graph.zones)}  "
            f"Connections: {len(self.graph.connections)}"
        )

        print(f"\n{BOLD}Zones:{RESET}")
        for name, zone in sorted(self.graph.zones.items()):
            color_code = self._get_color(zone.color)
            role = ""
            if zone.is_start:
                role = " [START]"
            elif zone.is_end:
                role = " [END]"

            cap = (
                "unlimited"
                if zone.has_unlimited_capacity()
                else str(zone.max_drones)
            )
            print(
                f"  {color_code}{name}{RESET}"
                f" ({zone.zone_type.value}, cap={cap})"
                f"{role}"
            )

        print(f"\n{BOLD}Connections:{RESET}")
        for key, conn in sorted(self.graph.connections.items()):
            print(
                f"  {conn.zone_a} <-> {conn.zone_b}"
                f" (cap={conn.max_link_capacity})"
            )
        print()

    def display_turn(
        self,
        turn_num: int,
        movements: str,
        drones: list[Drone],
    ) -> None:
        """Display a single turn's movements.

        Args:
            turn_num: The turn number.
            movements: Space-separated movement string.
            drones: List of all drones.
        """
        arrived = sum(
            1 for d in drones if d.state == DroneState.ARRIVED
        )
        total = len(drones)

        print(
            f"{BOLD}Turn {turn_num}{RESET} "
            f"{DIM}[{arrived}/{total} arrived]{RESET}  "
            f"{self._colorize_movements(movements)}"
        )

    def display_stats(self, stats: dict[str, object]) -> None:
        """Display simulation statistics.

        Args:
            stats: Dictionary with simulation metrics.
        """
        print(f"\n{BOLD}=== Simulation Results ==={RESET}")
        print(f"  Total turns: {stats['turn_count']}")
        print(f"  Total drones: {stats['total_drones']}")
        print(
            f"  Drones/turn: {stats['drones_per_turn']}"
        )
        print(f"  Total path cost: {stats['total_cost']}")
        print()

    def _colorize_movements(self, movements: str) -> str:
        """Add colors to movement output.

        Args:
            movements: Space-separated movements.

        Returns:
            Colorized string.
        """
        if not movements:
            return f"{DIM}(no movements){RESET}"

        parts: list[str] = []
        for move in movements.split():
            if "-" in move:
                drone_part = move.split("-", 1)[0]
                zone_part = move.split("-", 1)[1]

                zone = self.graph.zones.get(zone_part)
                if zone and zone.color:
                    color_code = self._get_color(zone.color)
                    parts.append(
                        f"{BOLD}{drone_part}{RESET}-"
                        f"{color_code}{zone_part}{RESET}"
                    )
                else:
                    parts.append(
                        f"{BOLD}{drone_part}{RESET}-{zone_part}"
                    )
            else:
                parts.append(move)
        return " ".join(parts)

    @staticmethod
    def _get_color(color: Optional[str]) -> str:
        """Get ANSI color code for a color name.

        Args:
            color: Color name string.

        Returns:
            ANSI escape code.
        """
        if color is None:
            return ""
        return ANSI_COLORS.get(color, "")
