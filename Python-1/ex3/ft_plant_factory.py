#!/usr/bin/env python3


class Plant:
    """A class representing a plant in the garden."""

    def __init__(self, name: str, height: float, days_old: int) -> None:
        """Initialize a plant with given values."""
        self.name: str = name
        self.height: float = height
        self.days_old: int = days_old
        self.growth_rate: float = 0.8

    def show(self) -> None:
        """Display the plant information."""
        print(f"{self.name}: {self.height}cm, {self.days_old} days old")

    def grow(self) -> None:
        """Make the plant grow by its growth rate."""
        self.height = round(self.height + self.growth_rate, 1)

    def age(self) -> None:
        """Age the plant by one day."""
        self.days_old += 1


def main() -> None:
    """Create multiple plants using the factory pattern."""
    print("=== Plant Factory Output ===")

    plants: list[Plant] = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]

    for plant in plants:
        print("Created: ", end="")
        plant.show()


if __name__ == "__main__":
    main()
