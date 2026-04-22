#!/usr/bin/env python3


class Plant:
    """A class representing a plant in the garden."""

    def __init__(self) -> None:
        """Initialize a plant with default values."""
        self.name: str = ""
        self.height: float = 0.0
        self.days_old: int = 0
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
    """Simulate a week of plant growth."""
    print("=== Garden Plant Growth ===")

    rose: Plant = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.days_old = 30
    rose.growth_rate = 0.8

    initial_height: float = rose.height
    rose.show()

    for day in range(1, 8):
        rose.grow()
        rose.age()
        print(f"=== Day {day} ===")
        rose.show()

    growth: float = round(rose.height - initial_height, 1)
    print(f"Growth this week: {growth}cm")


if __name__ == "__main__":
    main()
