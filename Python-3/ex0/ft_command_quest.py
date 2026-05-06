#!/usr/bin/env python3
import sys


def main() -> None:
    """Display command-line arguments information."""
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    arg_count: int = len(sys.argv) - 1
    if arg_count == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {arg_count}")
        i: int = 1
        for arg in sys.argv[1:]:
            print(f"Argument {i}: {arg}")
            i += 1

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
