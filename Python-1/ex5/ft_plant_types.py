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
        self._age_increment: int = 1

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
        """Age the plant by its age increment."""
        self._age += self._age_increment


class Flower(Plant):
    """A flower plant with color and bloom ability."""

    def __init__(self, name: str, height: float, age: int,
                 color: str) -> None:
        """Initialize a flower with color."""
        super().__init__(name, height, age)
        self._color: str = color
        self._is_blooming: bool = False

    def bloom(self) -> None:
        """Make the flower bloom."""
        self._is_blooming = True

    def show(self) -> None:
        """Display flower information."""
        super().show()
        print(f"Color: {self._color}")
        if self._is_blooming:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    """A tree plant with trunk diameter and shade production."""

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        """Initialize a tree with trunk diameter."""
        super().__init__(name, height, age)
        self._trunk_diameter: float = trunk_diameter

    def produce_shade(self) -> None:
        """Produce shade based on height and trunk diameter."""
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height}cm long and {self._trunk_diameter}cm wide."
        )

    def show(self) -> None:
        """Display tree information."""
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter}cm")


class Vegetable(Plant):
    """A vegetable plant with harvest season and nutritional value."""

    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str) -> None:
        """Initialize a vegetable with harvest season."""
        super().__init__(name, height, age)
        self._harvest_season: str = harvest_season
        self._nutritional_value: int = 0
        self._growth_rate = 2.1

    def grow(self) -> None:
        """Grow the vegetable and increase nutritional value."""
        super().grow()
        self._nutritional_value += 1

    def show(self) -> None:
        """Display vegetable information."""
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


def main() -> None:
    """Demonstrate specialized plant types."""
    print("=== Garden Plant Types ===")

    print("\n=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("\n=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n=== Vegetable")
    tomato: Vegetable = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()


if __name__ == "__main__":
    main()
