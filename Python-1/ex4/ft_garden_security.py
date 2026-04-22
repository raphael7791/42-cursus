#!/usr/bin/env python3


class Plant:
    """A class representing a plant with protected data."""

    def __init__(self, name: str, height: float, age: int) -> None:
        """Initialize a plant with validated values."""
        self._name: str = name
        if height < 0:
            print(f"{name}: Error, height can't be negative")
            self._height: float = 0.0
        else:
            self._height = height
        if age < 0:
            print(f"{name}: Error, age can't be negative")
            self._age: int = 0
        else:
            self._age = age
        self._growth_rate: float = 0.8

    def get_height(self) -> float:
        """Return the plant height."""
        return self._height

    def get_age(self) -> int:
        """Return the plant age."""
        return self._age

    def set_height(self, height: float) -> None:
        """Set the plant height if valid."""
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height

    def set_age(self, age: int) -> None:
        """Set the plant age if valid."""
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age

    def show(self) -> None:
        """Display the plant information."""
        print(f"{self._name}: {self._height}cm, {self._age} days old")

    def grow(self) -> None:
        """Make the plant grow by its growth rate."""
        self._height = round(self._height + self._growth_rate, 1)

    def age(self) -> None:
        """Age the plant by one day."""
        self._age += 1


def main() -> None:
    """Demonstrate the garden security system."""
    print("=== Garden Security System ===")

    rose: Plant = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()

    rose.set_height(25.0)
    print("Height updated: 25cm")

    rose.set_age(30)
    print("Age updated: 30 days")

    rose.set_height(-5.0)
    rose.set_age(-10)

    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
