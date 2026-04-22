#!/usr/bin/env python3
import sys
from typing import IO


def main() -> None:
    """Read a file, transform content, optionally save to new file."""
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
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

    lines: list[str] = content.splitlines()
    transformed: str = "\n".join(line + "#" for line in lines) + "\n"

    print("Transform data:")
    print("---")
    print(transformed, end="")
    print("---")

    new_name: str = input("Enter new file name (or empty): ")

    if not new_name:
        print("Not saving data.")
        return

    print(f"Saving data to '{new_name}'")
    out: IO[str]
    try:
        out = open(new_name, "w")
    except OSError as e:
        print(f"Error opening file '{new_name}': {e}")
        return

    try:
        out.write(transformed)
    finally:
        out.close()
    print(f"Data saved in file '{new_name}'.")


if __name__ == "__main__":
    main()
