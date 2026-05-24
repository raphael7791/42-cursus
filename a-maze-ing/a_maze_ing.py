#!/usr/bin/env python3
"""A-Maze-ing: Maze generator with visual representation.

Reads a configuration file, generates a maze, writes it to
a file, and provides an interactive terminal display.

Usage:
    python3 a_maze_ing.py config.txt
"""
from __future__ import annotations

import os
import sys
import time
from typing import Optional

from mazegen import MazeGenerator


def parse_config(filepath: str) -> dict[str, str]:
    """Parse a KEY=VALUE configuration file.

    Lines starting with # are comments and are ignored.
    Empty lines are ignored.

    Args:
        filepath: Path to the configuration file.

    Returns:
        Dictionary of key-value pairs.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        ValueError: If config syntax is invalid.
    """
    config: dict[str, str] = {}
    with open(filepath, 'r') as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError(
                    f"Bad syntax at line {lineno}: {line}")
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
    return config


def validate_config(config: dict[str, str]) -> dict[str, object]:
    """Validate and parse configuration values.

    Args:
        config: Raw key-value configuration.

    Returns:
        Parsed configuration with typed values.

    Raises:
        ValueError: If required keys are missing or invalid.
    """
    required: list[str] = [
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
        'OUTPUT_FILE', 'PERFECT'
    ]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    try:
        width: int = int(config['WIDTH'])
        height: int = int(config['HEIGHT'])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be integers")

    if width < 3 or height < 3:
        raise ValueError("Maze must be at least 3x3")

    try:
        ex, ey = config['ENTRY'].split(',')
        entry: tuple[int, int] = (int(ex.strip()),
                                  int(ey.strip()))
    except (ValueError, IndexError):
        raise ValueError("ENTRY must be x,y format")

    try:
        xx, xy = config['EXIT'].split(',')
        exit_pos: tuple[int, int] = (int(xx.strip()),
                                     int(xy.strip()))
    except (ValueError, IndexError):
        raise ValueError("EXIT must be x,y format")

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError(f"ENTRY {entry} out of bounds")
    if not (0 <= exit_pos[0] < width
            and 0 <= exit_pos[1] < height):
        raise ValueError(f"EXIT {exit_pos} out of bounds")
    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT must be different")

    perfect_str: str = config['PERFECT'].lower()
    if perfect_str not in ('true', 'false'):
        raise ValueError("PERFECT must be True or False")
    perfect: bool = perfect_str == 'true'

    output_file: str = config['OUTPUT_FILE']

    seed: Optional[int] = None
    if 'SEED' in config:
        try:
            seed = int(config['SEED'])
        except ValueError:
            raise ValueError("SEED must be an integer")

    return {
        'width': width,
        'height': height,
        'entry': entry,
        'exit_pos': exit_pos,
        'perfect': perfect,
        'output_file': output_file,
        'seed': seed,
    }


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_maze(maze: MazeGenerator, show_path: bool,
                 wall_color: str, pattern_color: str) -> None:
    """Display the maze with current settings.

    Args:
        maze: The generated maze.
        show_path: Whether to show the solution path.
        wall_color: Color name for walls.
        pattern_color: Color name for 42 pattern.
    """
    clear_screen()
    print("=" * 50)
    print("       A-MAZE-ING  -  Maze Generator")
    print("=" * 50)
    print()
    print(maze.to_ascii(
        show_path=show_path,
        wall_color=wall_color,
        pattern_color=pattern_color,
    ))
    print()
    info: str = (
        f"Size: {maze.width}x{maze.height} | "
        f"Entry: {maze.entry} | Exit: {maze.exit_pos} | "
        f"Perfect: {maze.perfect}"
    )
    print(info)
    if maze.has_42_pattern():
        print("42 pattern: visible")
    else:
        print("42 pattern: maze too small")
    if show_path:
        sol: list[str] = maze.get_solution()
        print(f"Path length: {len(sol)} steps")
    print()


def print_menu() -> None:
    """Print the interactive menu."""
    print("--- Menu ---")
    print("[r] Regenerate maze (new seed)")
    print("[s] Show/Hide solution path")
    print("[c] Change wall color")
    print("[p] Change 42 pattern color")
    print("[q] Quit")
    print()


def interactive_loop(maze: MazeGenerator,
                     output_file: str) -> None:
    """Run the interactive display loop.

    Args:
        maze: The generated maze.
        output_file: Path to write maze output.
    """
    show_path: bool = False
    wall_colors: list[str] = [
        "white", "red", "green", "blue",
        "yellow", "cyan", "magenta"
    ]
    pattern_colors: list[str] = [
        "yellow", "red", "cyan", "magenta",
        "green", "blue", "white"
    ]
    wall_idx: int = 0
    pattern_idx: int = 0

    while True:
        display_maze(maze, show_path,
                     wall_colors[wall_idx],
                     pattern_colors[pattern_idx])
        print_menu()

        try:
            choice: str = input("Choice: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == 'r':
            maze.seed = int(time.time())
            maze.generate()
            maze.write_output(output_file)
            print("Maze regenerated with new seed!")
        elif choice == 's':
            show_path = not show_path
        elif choice == 'c':
            wall_idx = (wall_idx + 1) % len(wall_colors)
            print(f"Wall color: {wall_colors[wall_idx]}")
        elif choice == 'p':
            pattern_idx = (
                (pattern_idx + 1) % len(pattern_colors)
            )
            print(f"Pattern color: "
                  f"{pattern_colors[pattern_idx]}")
        else:
            print(f"Unknown option: {choice}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_path: str = sys.argv[1]

    try:
        raw_config: dict[str, str] = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: file '{config_path}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error in config: {e}")
        sys.exit(1)

    try:
        config: dict[str, object] = validate_config(raw_config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    width: int = int(str(config['width']))
    height: int = int(str(config['height']))
    entry: tuple[int, int] = config['entry']  # type: ignore
    exit_pos: tuple[int, int] = config['exit_pos']  # type: ignore
    perfect: bool = bool(config['perfect'])
    output_file: str = str(config['output_file'])
    seed: Optional[int] = config.get('seed')  # type: ignore

    try:
        maze: MazeGenerator = MazeGenerator(
            width=width, height=height,
            entry=entry, exit_pos=exit_pos,
            perfect=perfect, seed=seed,
        )
        maze.generate()
    except ValueError as e:
        print(f"Error generating maze: {e}")
        sys.exit(1)

    if not maze.has_42_pattern():
        print("Warning: maze too small for '42' pattern")

    try:
        maze.write_output(output_file)
        print(f"Maze written to '{output_file}'")
    except OSError as e:
        print(f"Error writing output: {e}")
        sys.exit(1)

    interactive_loop(maze, output_file)


if __name__ == "__main__":
    main()
