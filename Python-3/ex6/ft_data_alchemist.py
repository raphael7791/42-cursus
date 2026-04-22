#!/usr/bin/env python3
import random


def main() -> None:
    """Demonstrate list and dict comprehensions."""
    print("=== Game Data Alchemist ===")

    players: list[str] = [
        "Alice", "bob", "Charlie", "dylan", "Emma",
        "Gregory", "john", "kevin", "Liam",
    ]
    print(f"Initial list of players: {players}")

    all_capitalized: list[str] = [n.capitalize() for n in players]
    print(f"New list with all names capitalized: {all_capitalized}")

    only_capitalized: list[str] = [n for n in players if n[0].isupper()]
    print(f"New list of capitalized names only: {only_capitalized}")

    scores: dict[str, int] = {
        name: random.randint(50, 950) for name in all_capitalized
    }
    print(f"Score dict: {scores}")

    average: float = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average}")

    high_scores: dict[str, int] = {
        name: score for name, score in scores.items()
        if score > average
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
