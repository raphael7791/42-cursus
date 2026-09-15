"""Pathfinder for distributing drones across multiple paths."""

from flying.models.graph import Graph
from flying.models.drone import Drone
from flying.models.zone import ZoneType
from flying.simulator import Simulator


class Pathfinder:
    """Finds and distributes drone paths through the graph.

    Uses k-shortest-paths + greedy distribution + simulation
    verification to find optimal drone assignments.
    """

    def __init__(self, graph: Graph) -> None:
        """Initialize the Pathfinder.

        Args:
            graph: The simulation graph.
        """
        self.graph: Graph = graph

    def find_and_assign_paths(
        self, drones: list[Drone]
    ) -> None:
        """Find paths and assign them to drones.

        Args:
            drones: List of drones to assign paths to.

        Raises:
            RuntimeError: If no path exists.
        """
        start = self.graph.start_zone
        end = self.graph.end_zone
        if not start or not end:
            raise RuntimeError(
                "Graph missing start or end zone"
            )

        candidates = self.graph.k_shortest_paths(
            start, end, k=20
        )
        if not candidates:
            raise RuntimeError(
                "No path exists from start to end"
            )

        seen: set[tuple[str, ...]] = set()
        paths: list[list[str]] = []
        for p in candidates:
            key = tuple(p)
            if key not in seen:
                seen.add(key)
                paths.append(p)

        total = len(drones)
        best_turns = float("inf")
        best_assignment: list[tuple[list[str], int]] = [
            (paths[0], total)
        ]

        for n_paths in range(1, len(paths) + 1):
            subset = paths[:n_paths]
            throughputs = [
                self._path_throughput(p) for p in subset
            ]
            costs = [
                self._real_turn_cost(p) for p in subset
            ]

            assignment = self._distribute_drones(
                subset, throughputs, costs, total
            )

            turns = self._simulate_assignment(
                assignment, total
            )
            if turns < best_turns:
                best_turns = turns
                best_assignment = assignment

        self._assign_interleaved(drones, best_assignment)

    def _real_turn_cost(self, path: list[str]) -> int:
        """Real turn cost: 1 for normal/priority, 2 for restricted.

        Args:
            path: List of zone names.

        Returns:
            Total turns to traverse this path.
        """
        cost = 0
        for i in range(1, len(path)):
            zone = self.graph.zones[path[i]]
            if zone.zone_type == ZoneType.RESTRICTED:
                cost += 2
            else:
                cost += 1
        return cost

    def _path_throughput(self, path: list[str]) -> int:
        """Calculate path throughput.

        Throughput = min capacity along the path,
        excluding start/end (unlimited).

        Args:
            path: List of zone names.

        Returns:
            Minimum capacity of the path.
        """
        min_cap = float("inf")

        for i in range(1, len(path) - 1):
            zone = self.graph.zones[path[i]]
            if not zone.has_unlimited_capacity():
                cap = zone.max_drones
                if cap < min_cap:
                    min_cap = cap

        for i in range(len(path) - 1):
            conn = self.graph.get_connection(
                path[i], path[i + 1]
            )
            if conn and conn.max_link_capacity < min_cap:
                min_cap = conn.max_link_capacity

        if min_cap == float("inf"):
            return 1
        return int(min_cap)

    def _distribute_drones(
        self,
        paths: list[list[str]],
        throughputs: list[int],
        costs: list[int],
        total: int,
    ) -> list[tuple[list[str], int]]:
        """Distribute drones greedily minimizing max time.

        Args:
            paths: Candidate paths.
            throughputs: Per-path throughput.
            costs: Per-path real turn cost.
            total: Total drones.

        Returns:
            List of (path, count) pairs with count > 0.
        """
        n = len(paths)
        counts = [0] * n

        for _ in range(total):
            best_i = 0
            best_time = float("inf")
            for i in range(n):
                t = self._est_turns(
                    counts[i] + 1,
                    throughputs[i],
                    costs[i],
                )
                if t < best_time:
                    best_time = t
                    best_i = i
            counts[best_i] += 1

        return [
            (paths[i], counts[i])
            for i in range(n)
            if counts[i] > 0
        ]

    @staticmethod
    def _est_turns(
        count: int,
        throughput: int,
        cost: int,
    ) -> float:
        """Estimate turns for count drones on a path.

        Args:
            count: Number of drones.
            throughput: Path throughput.
            cost: Path turn cost.

        Returns:
            Estimated turns.
        """
        if count == 0:
            return 0.0
        if throughput == 0:
            return float("inf")
        waves = (count + throughput - 1) // throughput
        return float(cost + waves - 1)

    def _simulate_assignment(
        self,
        assignment: list[tuple[list[str], int]],
        total: int,
    ) -> int:
        """Run the simulator to get real turn count.

        Args:
            assignment: List of (path, count) pairs.
            total: Total drones.

        Returns:
            Actual number of turns from simulation.
        """
        start = self.graph.start_zone
        if start is None:
            return total * 100

        drones = [
            Drone(i + 1, start) for i in range(total)
        ]
        self._assign_interleaved(drones, assignment)

        sim = Simulator(self.graph, drones)
        sim.run()
        return sim.turn_count

    @staticmethod
    def _assign_interleaved(
        drones: list[Drone],
        assignment: list[tuple[list[str], int]],
    ) -> None:
        """Round-robin assignment to reduce contention.

        Args:
            drones: Drones to assign paths to.
            assignment: List of (path, count) pairs.
        """
        remaining = [count for _, count in assignment]
        drone_idx = 0

        while drone_idx < len(drones):
            assigned_any = False
            for pi in range(len(assignment)):
                if (
                    remaining[pi] > 0
                    and drone_idx < len(drones)
                ):
                    drones[drone_idx].assign_path(
                        assignment[pi][0]
                    )
                    drone_idx += 1
                    remaining[pi] -= 1
                    assigned_any = True
            if not assigned_any:
                break
