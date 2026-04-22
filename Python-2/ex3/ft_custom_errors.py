#!/usr/bin/env python3


class GardenError(Exception):
    """Base error for garden problems."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Error for plant-related problems."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    """Error for watering-related problems."""

    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def check_plant(name: str) -> None:
    """Raise PlantError if plant is wilting."""
    raise PlantError(f"The {name} plant is wilting!")


def check_water(level: int) -> None:
    """Raise WaterError if water level is too low."""
    if level < 10:
        raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    """Demonstrate custom garden errors."""
    print("=== Custom Garden Errors Demo ===")

    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("Testing WaterError...")
    try:
        check_water(5)
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("Testing catching all garden errors...")
    try:
        check_plant("tomato")
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    try:
        check_water(5)
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
