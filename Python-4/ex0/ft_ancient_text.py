#!/usr/bin/env python3
import sys
from typing import IO


def main() -> None:
    """Read and display the contents of a file."""
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    f: IO[str]
    try:
        f = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    try:
        content: str = f.read()
        print("---")
        print(content, end="")
        print("---")
    finally:
        f.close()
        print(f"File '{filename}' closed.")


if __name__ == "__main__":
    main()
