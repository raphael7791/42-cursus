#!/usr/bin/env python3


class GardenError(Exception):
    """Base error for garden problems."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Error for plant-related problems."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    """Water a plant. Raises PlantError if name is not capitalized."""
    if plant_name != plant_name.capitalize():
        raise PlantError(
            f"Invalid plant name to water: '{plant_name}'"
        )
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str]) -> None:
    """Test the watering system with a list of plants."""
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


def main() -> None:
    """Demonstrate the finally block with the watering system."""
    print("=== Garden Watering System ===")

    print("Testing valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])

    print("\nTesting invalid plants...")
    test_watering_system(["Tomato", "lettuce", "Carrots"])

    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()
