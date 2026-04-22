#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    """Convert a string to a temperature and validate range."""
    temp: int = int(temp_str)
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    return temp


def test_temperature() -> None:
    """Test input_temperature with valid, invalid, and extreme inputs."""
    print("=== Garden Temperature Checker ===")

    test_values: list[str] = ["25", "abc", "100", "-50"]

    for temp_str in test_values:
        print(f"Input data is '{temp_str}'")
        try:
            temp: int = input_temperature(temp_str)
            print(f"Temperature is now {temp}°C")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
