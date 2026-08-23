"""Graph model for the drone simulation."""

import heapq
from typing import Optional

from flying.models.zone import Zone, ZoneType
from flying.models.connection import Connection


class Graph:
    """Graph representing the network of zones and connections.

    Attributes:
        zones: Dictionary mapping zone names to Zone objects.
        connections: Dictionary mapping connection keys to Connection objects.
        adjacency: Adjacency list mapping zone names to neighbor names.
        start_zone: Name of the start hub.
        end_zone: Name of the end hub.
    """

    def __init__(self) -> None:
        """Initialize an empty Graph."""
        self.zones: dict[str, Zone] = {}
        self.connections: dict[tuple[str, str], Connection] = {}
        self.adjacency: dict[str, list[str]] = {}
        self.start_zone: Optional[str] = None
        self.end_zone: Optional[str] = None

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph.

        Args:
            zone: The zone to add.

        Raises:
            ValueError: If a zone with the same name already exists.
        """
        if zone.name in self.zones:
            raise ValueError(f"Duplicate zone name: '{zone.name}'")
        self.zones[zone.name] = zone
        self.adjacency[zone.name] = []
        if zone.is_start:
            self.start_zone = zone.name
        if zone.is_end:
            self.end_zone = zone.name

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the graph.

        Args:
            connection: The connection to add.

        Raises:
            ValueError: If zones don't exist or connection is duplicate.
        """
        if connection.zone_a not in self.zones:
            raise ValueError(
                f"Zone '{connection.zone_a}' not found"
            )
        if connection.zone_b not in self.zones:
            raise ValueError(
                f"Zone '{connection.zone_b}' not found"
            )
        key = connection.key()
        if key in self.connections:
            raise ValueError(
                f"Duplicate connection: "
                f"{connection.zone_a}-{connection.zone_b}"
            )
        self.connections[key] = connection
        self.adjacency[connection.zone_a].append(connection.zone_b)
        self.adjacency[connection.zone_b].append(connection.zone_a)

    def neighbors(self, zone_name: str) -> list[str]:
        """Get neighboring zone names.

        Args:
            zone_name: Name of the zone.

        Returns:
            List of adjacent zone names.
        """
        return self.adjacency.get(zone_name, [])

    def get_connection(
        self, zone_a: str, zone_b: str
    ) -> Optional[Connection]:
        """Get the connection between two zones.

        Args:
            zone_a: First zone name.
            zone_b: Second zone name.

        Returns:
            The Connection object, or None if not connected.
        """
        if zone_a < zone_b:
            key = (zone_a, zone_b)
        else:
            key = (zone_b, zone_a)
        return self.connections.get(key)

    def shortest_path(
        self,
        start: str,
        end: str,
    ) -> Optional[list[str]]:
        """Find shortest path using modified Dijkstra.

        Costs: normal=1, priority=0.5 (favored), restricted=2,
        blocked=inaccessible.

        Args:
            start: Start zone name.
            end: End zone name.

        Returns:
            List of zone names from start to end, or None if no path.
        """
        dist: dict[str, float] = {start: 0.0}
        prev: dict[str, Optional[str]] = {start: None}
        heap: list[tuple[float, str]] = [(0.0, start)]

        while heap:
            cost, current = heapq.heappop(heap)
            if current == end:
                path: list[str] = []
                node: Optional[str] = end
                while node is not None:
                    path.append(node)
                    node = prev[node]
                path.reverse()
                return path
            if cost > dist.get(current, float("inf")):
                continue
            for neighbor in self.neighbors(current):
                zone = self.zones[neighbor]
                if not zone.is_accessible():
                    continue
                edge_cost = zone.movement_cost()
                new_cost = cost + edge_cost
                if new_cost < dist.get(neighbor, float("inf")):
                    dist[neighbor] = new_cost
                    prev[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
        return None

    def k_shortest_paths(
        self,
        start: str,
        end: str,
        k: int = 10,
    ) -> list[list[str]]:
        """Find k shortest paths using Yen's algorithm.

        Args:
            start: Start zone name.
            end: End zone name.
            k: Maximum number of paths to find.

        Returns:
            List of paths (each path is a list of zone names).
        """
        best = self.shortest_path(start, end)
        if best is None:
            return []
        a_paths: list[list[str]] = [best]
        b_candidates: list[tuple[float, list[str]]] = []

        for ki in range(1, k):
            if ki - 1 >= len(a_paths):
                break
            prev_path = a_paths[ki - 1]
            for i in range(len(prev_path) - 1):
                spur_node = prev_path[i]
                root_path = prev_path[: i + 1]

                blocked_edges: set[tuple[str, str]] = set()
                blocked_nodes: set[str] = set()

                for path in a_paths:
                    if path[: i + 1] == root_path and i + 1 < len(path):
                        a_name = path[i]
                        b_name = path[i + 1]
                        if a_name < b_name:
                            blocked_edges.add((a_name, b_name))
                        else:
                            blocked_edges.add((b_name, a_name))

                for node in root_path[:-1]:
                    blocked_nodes.add(node)

                spur = self._dijkstra_with_blocks(
                    spur_node, end, blocked_edges, blocked_nodes
                )
                if spur is not None:
                    total_path = root_path[:-1] + spur
                    cost = self._path_cost(total_path)
                    if total_path not in a_paths:
                        heapq.heappush(
                            b_candidates, (cost, total_path)
                        )

            if not b_candidates:
                break
            _, next_path = heapq.heappop(b_candidates)
            if next_path not in a_paths:
                a_paths.append(next_path)

        return a_paths

    def _dijkstra_with_blocks(
        self,
        start: str,
        end: str,
        blocked_edges: set[tuple[str, str]],
        blocked_nodes: set[str],
    ) -> Optional[list[str]]:
        """Dijkstra with blocked edges and nodes.

        Args:
            start: Start zone name.
            end: End zone name.
            blocked_edges: Set of edge keys to block.
            blocked_nodes: Set of node names to block.

        Returns:
            Path from start to end, or None.
        """
        dist: dict[str, float] = {start: 0.0}
        prev: dict[str, Optional[str]] = {start: None}
        heap: list[tuple[float, str]] = [(0.0, start)]

        while heap:
            cost, current = heapq.heappop(heap)
            if current == end:
                path: list[str] = []
                node: Optional[str] = end
                while node is not None:
                    path.append(node)
                    node = prev[node]
                path.reverse()
                return path
            if cost > dist.get(current, float("inf")):
                continue
            for neighbor in self.neighbors(current):
                if neighbor in blocked_nodes:
                    continue
                zone = self.zones[neighbor]
                if not zone.is_accessible():
                    continue
                edge_key = (
                    (current, neighbor) if current < neighbor
                    else (neighbor, current)
                )
                if edge_key in blocked_edges:
                    continue
                edge_cost = zone.movement_cost()
                new_cost = cost + edge_cost
                if new_cost < dist.get(neighbor, float("inf")):
                    dist[neighbor] = new_cost
                    prev[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
        return None

    def _path_cost(self, path: list[str]) -> float:
        """Calculate the weighted cost of a path.

        Args:
            path: List of zone names.

        Returns:
            Total weighted cost.
        """
        cost: float = 0.0
        for i in range(1, len(path)):
            zone = self.zones[path[i]]
            cost += zone.movement_cost()
        return cost

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"Graph(zones={len(self.zones)}, "
            f"connections={len(self.connections)})"
        )
