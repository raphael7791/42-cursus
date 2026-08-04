*This project has been created as part of the 42 curriculum by rbriguet.*

# Flying - Drone Routing Simulation

## Description

Flying is a drone fleet routing simulation that efficiently routes drones from a start hub to an end hub through a network of zones. The system navigates capacity constraints, zone types (normal, restricted, priority, blocked), and connection limits to minimize the total number of simulation turns.

The simulation handles simultaneous drone movements, restricted zone transit (2-turn cost), and strategic drone distribution across multiple paths.

## Instructions

### Installation

```bash
make install
```

### Running

```bash
# Default map
make run

# Specific map
make run MAP=maps/medium/01_dead_end_trap.txt

# Direct execution
python main.py maps/easy/01_linear_path.txt

# Debug mode
make debug MAP=maps/easy/01_linear_path.txt

# Without visual output
python main.py maps/easy/01_linear_path.txt --no-visual
```

### Linting

```bash
make lint        # flake8 + mypy
make lint-strict # mypy --strict
make clean       # Remove caches
```

## Algorithm

### Pathfinding Strategy

1. **Modified Dijkstra**: Finds shortest paths with weighted costs:
   - Normal zones: cost 1
   - Priority zones: cost 0.5 (favored)
   - Restricted zones: cost 2
   - Blocked zones: inaccessible

2. **Yen's K-Shortest Paths**: Finds up to 20 alternative paths to distribute drones across multiple routes.

3. **Throughput-Based Distribution**: Each path's throughput is calculated as the minimum capacity (zone or connection) along the path. Drones are distributed proportionally to throughput, then rebalanced to minimize the maximum turn count across all paths.

### Simulation Engine

- **Turn-by-turn**: Each turn, drones move simultaneously respecting all capacity constraints.
- **Departure frees capacity**: Drones leaving a zone free up space for that same turn.
- **Restricted zones**: Require 2 turns. Drone enters the connection on turn 1 and MUST arrive on turn 2.
- **Priority scheduling**: Drones closer to their destination move first.

### Complexity

- Dijkstra: O((V + E) log V)
- Yen's K-shortest: O(K * V * (V + E) log V)
- Simulation: O(T * D) where T = turns, D = drones

## Visual Representation

The terminal visualizer uses ANSI colors to display:
- Zone colors matching the map definition
- Drone movements with bold identifiers
- Per-turn arrival progress (arrived/total)
- Final statistics (turns, drones/turn, total cost)

Colors enhance readability by visually grouping zones by type and showing drone positions at a glance.

## Example

Input (`maps/easy/01_linear_path.txt`):
```
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]
connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Output:
```
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

## Resources

- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Yen's K-Shortest Paths](https://en.wikipedia.org/wiki/Yen%27s_algorithm)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- AI was used (Claude) to assist with code generation, algorithm design, and documentation. All code was reviewed and understood by the student.
