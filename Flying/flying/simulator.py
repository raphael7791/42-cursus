"""Turn-by-turn simulation engine for drone routing."""

from flying.models.graph import Graph
from flying.models.drone import Drone, DroneState
from flying.models.zone import ZoneType


class Simulator:
    """Simulates drone movement through the graph turn by turn.

    Handles capacity constraints, restricted zone transit,
    and outputs movement lines.

    Attributes:
        graph: The simulation graph.
        drones: List of all drones.
        turns: List of turn output lines.
        turn_count: Number of turns executed.
    """

    def __init__(
        self, graph: Graph, drones: list[Drone]
    ) -> None:
        """Initialize the Simulator.

        Args:
            graph: The simulation graph.
            drones: List of drones to simulate.
        """
        self.graph: Graph = graph
        self.drones: list[Drone] = drones
        self.turns: list[str] = []
        self.turn_count: int = 0

    def run(self) -> list[str]:
        """Run the simulation until all drones arrive.

        Returns:
            List of output lines, one per turn.
        """
        max_turns = 10000
        stall_count = 0
        max_stall = 100

        for turn_num in range(1, max_turns + 1):
            if self._all_arrived():
                break

            movements = self._execute_turn()
            if movements:
                self.turns.append(" ".join(movements))
                self.turn_count += 1
                stall_count = 0
            else:
                stall_count += 1
                if stall_count >= max_stall:
                    break

        return self.turns

    def _all_arrived(self) -> bool:
        """Check if all drones have arrived.

        Returns:
            True if every drone is in ARRIVED state.
        """
        return all(d.has_arrived() for d in self.drones)

    def _has_in_transit(self) -> bool:
        """Check if any drone is in transit.

        Returns:
            True if any drone is IN_TRANSIT.
        """
        return any(
            d.state == DroneState.IN_TRANSIT
            for d in self.drones
        )

    def _execute_turn(self) -> list[str]:
        """Execute one simulation turn.

        Returns:
            List of movement strings for this turn.
        """
        movements: list[str] = []
        zone_occupancy: dict[str, int] = {}
        conn_usage: dict[tuple[str, str], int] = {}

        for zone_name, zone in self.graph.zones.items():
            if zone.has_unlimited_capacity():
                zone_occupancy[zone_name] = 0
            else:
                count = 0
                for d in self.drones:
                    if (
                        d.position == zone_name
                        and d.state != DroneState.ARRIVED
                        and d.state != DroneState.IN_TRANSIT
                    ):
                        count += 1
                zone_occupancy[zone_name] = count

        just_arrived: set[int] = self._process_transit(
            movements, zone_occupancy
        )

        leaving: dict[str, int] = {}
        planned: list[tuple[Drone, str]] = []

        active = [
            d for d in self.drones
            if (
                d.state != DroneState.ARRIVED
                and d.state != DroneState.IN_TRANSIT
                and d.drone_id not in just_arrived
                and d.next_zone() is not None
            )
        ]

        active.sort(key=lambda d: (
            len(d.path) - d.path_index,
            d.drone_id,
        ))

        for drone in active:
            next_z = drone.next_zone()
            if next_z is None:
                continue

            dest = self.graph.zones[next_z]

            if not dest.is_accessible():
                continue

            conn = self.graph.get_connection(
                drone.position, next_z
            )
            if conn is None:
                continue

            conn_key = conn.key()
            cur_usage = conn_usage.get(conn_key, 0)
            if cur_usage >= conn.max_link_capacity:
                continue

            if dest.has_unlimited_capacity():
                can_enter = True
            else:
                cur_occ = zone_occupancy.get(next_z, 0)
                will_leave = leaving.get(next_z, 0)
                eff_occ = cur_occ - will_leave
                can_enter = eff_occ < dest.max_drones

            if not can_enter:
                continue

            is_restr = (
                dest.zone_type == ZoneType.RESTRICTED
            )

            planned.append((drone, next_z))
            conn_usage[conn_key] = cur_usage + 1

            leaving[drone.position] = (
                leaving.get(drone.position, 0) + 1
            )

            if not dest.has_unlimited_capacity():
                if not is_restr:
                    zone_occupancy[next_z] = (
                        zone_occupancy.get(next_z, 0) + 1
                    )

        for drone, next_z in planned:
            dest = self.graph.zones[next_z]
            is_restr = (
                dest.zone_type == ZoneType.RESTRICTED
            )

            if is_restr:
                conn = self.graph.get_connection(
                    drone.position, next_z
                )
                if conn is not None:
                    cn = f"{conn.zone_a}-{conn.zone_b}"
                else:
                    cn = f"{drone.position}-{next_z}"
                drone.transit_from = drone.position
                drone.transit_target = next_z
                drone.state = DroneState.IN_TRANSIT
                movements.append(
                    f"{drone.label()}-{cn}"
                )
            else:
                drone.advance()
                drone.state = DroneState.MOVING

                if drone.position == self.graph.end_zone:
                    drone.state = DroneState.ARRIVED

                movements.append(
                    f"{drone.label()}-{drone.position}"
                )

        return movements

    def _process_transit(
        self,
        movements: list[str],
        zone_occupancy: dict[str, int],
    ) -> set[int]:
        """Process drones arriving from transit.

        In-transit drones MUST arrive at their destination.

        Args:
            movements: List to append movement strings to.
            zone_occupancy: Zone occupancy counts.

        Returns:
            Set of drone IDs that just arrived from transit.
        """
        arrived_ids: set[int] = set()

        for drone in self.drones:
            if drone.state != DroneState.IN_TRANSIT:
                continue
            if drone.transit_target is None:
                continue

            target = drone.transit_target
            drone.advance()
            drone.position = target
            drone.transit_target = None
            drone.transit_from = None
            drone.state = DroneState.MOVING

            dest = self.graph.zones[target]
            if not dest.has_unlimited_capacity():
                zone_occupancy[target] = (
                    zone_occupancy.get(target, 0) + 1
                )

            if drone.position == self.graph.end_zone:
                drone.state = DroneState.ARRIVED

            movements.append(
                f"{drone.label()}-{drone.position}"
            )
            arrived_ids.add(drone.drone_id)

        return arrived_ids

    def get_stats(self) -> dict[str, object]:
        """Get simulation statistics.

        Returns:
            Dict with turn_count, drones_per_turn, total_cost.
        """
        total_cost = 0
        for drone in self.drones:
            for i in range(1, len(drone.path)):
                zone = self.graph.zones[drone.path[i]]
                total_cost += zone.movement_cost()

        dpt = 0.0
        if self.turn_count > 0:
            dpt = len(self.drones) / self.turn_count

        return {
            "turn_count": self.turn_count,
            "total_drones": len(self.drones),
            "drones_per_turn": round(dpt, 2),
            "total_cost": total_cost,
        }
