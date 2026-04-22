#!/usr/bin/env python3
import sys
from typing import IO


def main() -> None:
    """Read a file, transform content, use stderr for errors."""
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    f: IO[str]
    try:
        f = open(filename, "r")
    except OSError as e:
        print(f"[STDERR] Error opening file '{filename}': {e}",
              file=sys.stderr)
        return

    try:
        content: str = f.read()
        print("---")
        print(content, end="")
        print("---")
    finally:
        f.close()
        print(f"File '{filename}' closed.")

    lines: list[str] = content.splitlines()
    transformed: str = "\n".join(line + "#" for line in lines) + "\n"

    print("Transform data:")
    print("---")
    print(transformed, end="")
    print("---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_name: str = sys.stdin.readline().strip()

    if not new_name:
        print("Not saving data.")
        return

    print(f"Saving data to '{new_name}'")
    out: IO[str]
    try:
        out = open(new_name, "w")
    except OSError as e:
        print(f"[STDERR] Error opening file '{new_name}': {e}",
              file=sys.stderr)
        print("Data not saved.")
        return

    try:
        out.write(transformed)
    finally:
        out.close()
    print(f"Data saved in file '{new_name}'.")


if __name__ == "__main__":
    main()
