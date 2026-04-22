#!/usr/bin/env python3
import random


ALL_ACHIEVEMENTS: list[str] = [
    "Master Explorer", "Boss Slayer", "Collector Supreme",
    "Speed Runner", "Untouchable", "Crafting Genius",
    "World Savior", "Strategist", "First Steps",
    "Treasure Hunter", "Sharp Mind", "Unstoppable",
    "Survivor", "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    """Generate a random set of achievements for a player."""
    count: int = random.randint(4, 10)
    return set(random.sample(ALL_ACHIEVEMENTS, count))


def main() -> None:
    """Demonstrate set operations with achievement tracking."""
    print("=== Achievement Tracker System ===")

    names: list[str] = ["Alice", "Bob", "Charlie", "Dylan"]
    players: dict[str, set[str]] = {}

    for name in names:
        achievements: set[str] = gen_player_achievements()
        players[name] = achievements
        print(f"Player {name}: {achievements}")

    all_achievements: set[str] = set()
    for a in players.values():
        all_achievements = all_achievements.union(a)
    print(f"All distinct achievements: {all_achievements}")

    common: set[str] = set(ALL_ACHIEVEMENTS)
    for a in players.values():
        common = common.intersection(a)
    print(f"Common achievements: {common}")

    for name in names:
        others: set[str] = set()
        for other_name, a in players.items():
            if other_name != name:
                others = others.union(a)
        unique: set[str] = players[name].difference(others)
        print(f"Only {name} has: {unique}")

    full_set: set[str] = set(ALL_ACHIEVEMENTS)
    for name in names:
        missing: set[str] = full_set.difference(players[name])
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
