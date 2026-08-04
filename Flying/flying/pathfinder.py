"""Pathfinder for distributing drones across multiple paths."""

from dataclasses import dataclass

from flying.models.graph import Graph
from flying.models.drone import Drone


@dataclass
class PathInfo:
    """Analysis result for a single path.

    Attributes:
        path: List of zone names from start to end.
        throughput: Minimum capacity along the path.
        cost: Total turn cost of the path.
        length: Number of edges in the path.
    """

    path: list[str]
    throughput: int
    cost: int
    length: int


class Pathfinder:
    """Finds and distributes drone paths through the graph.

    Uses divergent paths from start to avoid deadlocks,
    and distributes drones to minimize total turns.
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

        paths = self._find_divergent_paths(start, end)

        if not paths:
            raise RuntimeError(
                "No path exists from start to end"
            )

        infos = self._analyze_paths(paths)
        assignments = self._distribute_drones(
            infos, len(drones)
        )

        idx = 0
        for pi, count in enumerate(assignments):
            for _ in range(count):
                if idx < len(drones):
                    drones[idx].assign_path(infos[pi].path)
                    idx += 1

    def _find_divergent_paths(
        self,
        start: str,
        end: str,
    ) -> list[list[str]]:
        """Find paths diverging through different neighbors.

        Each path goes through a different first hop from start,
        avoiding conflicting flows through bottleneck zones.

        Args:
            start: Start zone name.
            end: End zone name.

        Returns:
            List of distinct paths.
        """
        base = self.graph.shortest_path(start, end)
        if base is None:
            return []

        paths: list[list[str]] = [base]
        used_first_hops: set[str] = set()
        if len(base) > 1:
            used_first_hops.add(base[1])

        for neighbor in self.graph.neighbors(start):
            if neighbor in used_first_hops:
                continue
            zone = self.graph.zones[neighbor]
            if not zone.is_accessible():
                continue

            sub = self.graph.shortest_path(neighbor, end)
            if sub is None:
                continue

            full_path = [start] + sub
            if self._has_cycle(full_path):
                continue

            paths.append(full_path)
            used_first_hops.add(neighbor)

        return paths

    def _has_cycle(self, path: list[str]) -> bool:
        """Check if a path visits any zone twice.

        Args:
            path: List of zone names.

        Returns:
            True if any zone appears more than once.
        """
        return len(path) != len(set(path))

    def _analyze_paths(
        self, paths: list[list[str]]
    ) -> list[PathInfo]:
        """Analyze paths for throughput and cost.

        Args:
            paths: List of paths to analyze.

        Returns:
            List of PathInfo sorted by cost.
        """
        result: list[PathInfo] = []
        seen: set[tuple[str, ...]] = set()

        for path in paths:
            key = tuple(path)
            if key in seen:
                continue
            seen.add(key)

            info = PathInfo(
                path=path,
                throughput=self._path_throughput(path),
                cost=self._path_actual_cost(path),
                length=len(path) - 1,
            )
            result.append(info)

        result.sort(
            key=lambda x: (x.cost, -x.throughput)
        )
        return result

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

    def _path_actual_cost(self, path: list[str]) -> int:
        """Calculate the actual turn cost of a path.

        Args:
            path: List of zone names.

        Returns:
            Total turns to traverse this path.
        """
        cost = 0
        for i in range(1, len(path)):
            zone = self.graph.zones[path[i]]
            cost += zone.movement_cost()
        return cost

    def _distribute_drones(
        self,
        infos: list[PathInfo],
        total: int,
    ) -> list[int]:
        """Distribute drones across paths.

        Args:
            infos: Analyzed path information.
            total: Total number of drones.

        Returns:
            List of drone counts per path.
        """
        if len(infos) == 1:
            return [total]

        n = len(infos)
        assignments: list[int] = [0] * n
        remaining = total

        tps = [p.throughput for p in infos]
        total_tp = sum(tps)
        if total_tp == 0:
            assignments[0] = total
            return assignments

        for i in range(n):
            share = max(
                1,
                (tps[i] * total) // total_tp
            )
            assignments[i] = min(share, remaining)
            remaining -= assignments[i]
            if remaining <= 0:
                break

        if remaining > 0:
            assignments[0] += remaining

        self._balance(assignments, infos, total)
        return assignments

    def _balance(
        self,
        assignments: list[int],
        infos: list[PathInfo],
        total: int,
    ) -> None:
        """Rebalance to minimize max turns.

        Args:
            assignments: Counts (modified in place).
            infos: Path analysis info.
            total: Total drones.
        """
        for _ in range(total):
            turns: list[float] = []
            for i in range(len(assignments)):
                if assignments[i] == 0:
                    turns.append(float("inf"))
                    continue
                pi = infos[i]
                if pi.throughput == 0:
                    turns.append(float("inf"))
                    continue
                waves = (
                    (assignments[i] + pi.throughput - 1)
                    // pi.throughput
                )
                t = pi.cost + waves - 1
                turns.append(float(t))

            max_t = max(turns)
            max_i = turns.index(max_t)

            improved = False
            for j in range(len(assignments)):
                if j == max_i or assignments[max_i] <= 1:
                    continue
                assignments[max_i] -= 1
                assignments[j] += 1

                nm = self._est_turns(
                    assignments[max_i],
                    infos[max_i],
                )
                nj = self._est_turns(
                    assignments[j],
                    infos[j],
                )
                if max(nm, nj) < max_t:
                    improved = True
                    break
                assignments[max_i] += 1
                assignments[j] -= 1

            if not improved:
                break

    @staticmethod
    def _est_turns(
        count: int, info: PathInfo
    ) -> float:
        """Estimate turns for a path.

        Args:
            count: Number of drones.
            info: Path info.

        Returns:
            Estimated turns.
        """
        if count == 0 or info.throughput == 0:
            return 0.0
        waves = (
            (count + info.throughput - 1)
            // info.throughput
        )
        return float(info.cost + waves - 1)
