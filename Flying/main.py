"""Main entry point for the Flying drone simulation."""

import sys
from flying.parser import Parser, ParseError
from flying.models.drone import Drone
from flying.pathfinder import Pathfinder
from flying.simulator import Simulator
from flying.visualizer import Visualizer


def main() -> None:
    """Run the drone simulation.

    Usage: python main.py <map_file> [--debug] [--no-visual]
    """
    if len(sys.argv) < 2:
        print(
            "Usage: python main.py <map_file> "
            "[--debug] [--no-visual]",
            file=sys.stderr,
        )
        sys.exit(1)

    filepath: str = sys.argv[1]
    debug: bool = "--debug" in sys.argv
    visual: bool = "--no-visual" not in sys.argv

    try:
        graph, nb_drones = Parser.parse(filepath)
    except ParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if debug:
        print(f"[DEBUG] Parsed: {graph}")
        print(f"[DEBUG] Drones: {nb_drones}")

    if graph.start_zone is None or graph.end_zone is None:
        print("Error: Missing start or end zone", file=sys.stderr)
        sys.exit(1)

    try:
        drones: list[Drone] = [
            Drone(i + 1, graph.start_zone) for i in range(nb_drones)
        ]

        visualizer = Visualizer(graph)
        if visual:
            visualizer.display_graph()

        pathfinder = Pathfinder(graph)
        pathfinder.find_and_assign_paths(drones)

        if debug:
            for drone in drones:
                print(
                    f"[DEBUG] {drone.label()}: "
                    f"{' -> '.join(drone.path)}"
                )

        simulator = Simulator(graph, drones)
        turn_lines = simulator.run()

        total_drones: int = len(drones)
        for i, line in enumerate(turn_lines, start=1):
            if line:
                if visual:
                    arrived: int = simulator.arrived_per_turn[i - 1]
                    visualizer.display_turn(
                        i, line, arrived, total_drones
                    )
                else:
                    print(line)

        if visual:
            stats = simulator.get_stats()
            visualizer.display_stats(stats)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
