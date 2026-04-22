#!/usr/bin/env python3


def garden_operations(operation_number: int) -> None:
    """Execute a faulty operation based on operation_number."""
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 42 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        _ = "hello" + 42  # type: ignore


def test_error_types() -> None:
    """Test and catch different types of errors."""
    print("=== Garden Error Types Demo ===")

    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {type(e).__name__}: {e}")

    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
