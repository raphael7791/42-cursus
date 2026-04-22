#!/usr/bin/env python3


class Plant:
    """A class representing a plant with protected data and stats."""

    class Stats:
        """Nested class tracking plant statistics."""

        def __init__(self) -> None:
            """Initialize all counters to zero."""
            self._grow_count: int = 0
            self._age_count: int = 0
            self._show_count: int = 0

        def inc_grow(self) -> None:
            """Increment grow counter."""
            self._grow_count += 1

        def inc_age(self) -> None:
            """Increment age counter."""
            self._age_count += 1

        def inc_show(self) -> None:
            """Increment show counter."""
            self._show_count += 1

        def display(self) -> None:
            """Display the statistics."""
            print(
                f"Stats: {self._grow_count} grow, "
                f"{self._age_count} age, "
                f"{self._show_count} show"
            )

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
        self._stats: Plant.Stats = Plant.Stats()

    def get_height(self) -> float:
        """Return the plant height."""
        return self._height

    def get_age(self) -> int:
        """Return the plant age."""
        return self._age

    def get_stats(self) -> 'Plant.Stats':
        """Return the plant stats object."""
        return self._stats

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
        self._stats.inc_show()
        print(f"{self._name}: {self._height}cm, {self._age} days old")

    def grow(self) -> None:
        """Make the plant grow by its growth rate."""
        self._stats.inc_grow()
        self._height = round(self._height + self._growth_rate, 1)

    def age(self) -> None:
        """Age the plant by its age increment."""
        self._stats.inc_age()
        self._age += self._age_increment

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        """Check if the given age is more than a year (365 days)."""
        return age > 365

    @classmethod
    def create_anonymous(cls) -> 'Plant':
        """Create an anonymous plant with default values."""
        return cls("Unknown plant", 0.0, 0)


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

    class Stats(Plant.Stats):
        """Extended stats for trees with shade tracking."""

        def __init__(self) -> None:
            """Initialize tree stats."""
            super().__init__()
            self._shade_count: int = 0

        def inc_shade(self) -> None:
            """Increment shade counter."""
            self._shade_count += 1

        def display(self) -> None:
            """Display tree statistics including shade."""
            super().display()
            print(f"  {self._shade_count} shade")

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        """Initialize a tree with trunk diameter."""
        super().__init__(name, height, age)
        self._trunk_diameter: float = trunk_diameter
        self._stats: Tree.Stats = Tree.Stats()

    def produce_shade(self) -> None:
        """Produce shade based on height and trunk diameter."""
        self._stats.inc_shade()
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

    def grow(self) -> None:
        """Grow the vegetable and increase nutritional value."""
        super().grow()
        self._nutritional_value += 1

    def show(self) -> None:
        """Display vegetable information."""
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


class Seed(Flower):
    """A seed that inherits from Flower."""

    def __init__(self, name: str, height: float, age: int,
                 color: str) -> None:
        """Initialize a seed."""
        super().__init__(name, height, age, color)
        self._seeds: int = 0

    def bloom(self) -> None:
        """Make the seed bloom and produce seeds."""
        super().bloom()
        self._seeds = 42

    def show(self) -> None:
        """Display seed information."""
        super().show()
        print(f"Seeds: {self._seeds}")


def display_statistics(plant: Plant) -> None:
    """Display statistics for any kind of plant."""
    plant.get_stats().display()


def main() -> None:
    """Demonstrate garden analytics."""
    print("=== Garden statistics ===")

    print("\n=== Check year-old")
    print(f"Is 30 days more than a year? -> "
          f"{Plant.is_older_than_a_year(30)}")
    print(f"Is 400 days more than a year? -> "
          f"{Plant.is_older_than_a_year(400)}")

    print("\n=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, "red")
    rose._growth_rate = 8.0
    rose.show()
    print("[statistics for Rose]")
    display_statistics(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_statistics(rose)

    print("\n=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[statistics for Oak]")
    display_statistics(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_statistics(oak)

    print("\n=== Seed")
    sunflower: Seed = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower._growth_rate = 30.0
    sunflower._age_increment = 20
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_statistics(sunflower)

    print("\n=== Anonymous")
    anon: Plant = Plant.create_anonymous()
    anon.show()
    print("[statistics for Unknown plant]")
    display_statistics(anon)


if __name__ == "__main__":
    main()
