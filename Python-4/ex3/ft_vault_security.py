#!/usr/bin/env python3


def secure_archive(filename: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:
    """Safely read or write a file using context manager.

    Args:
        filename: Path to the file.
        mode: 'r' for read, 'w' for write.
        content: Content to write (only used in write mode).

    Returns:
        A tuple (success: bool, message: str).
    """
    try:
        with open(filename, mode) as f:
            if mode == "r":
                data: str = f.read()
                return (True, data)
            else:
                f.write(content)
                return (True, "Content successfully written to file")
    except OSError as e:
        return (False, str(e))


def main() -> None:
    """Demonstrate secure_archive function."""
    print("=== Cyber Archives Security ===")

    print("Using 'secure_archive' to read from a nonexistent file:")
    result: tuple[bool, str] = secure_archive("/not/existing/file")
    print(result)

    print("Using 'secure_archive' to read from an inaccessible file:")
    result = secure_archive("/etc/master.passwd")
    print(result)

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)

    print("Using 'secure_archive' to write previous content "
          "to a new file:")
    if result[0]:
        result = secure_archive("vault_copy.txt", "w", result[1])
    print(result)


if __name__ == "__main__":
    main()
