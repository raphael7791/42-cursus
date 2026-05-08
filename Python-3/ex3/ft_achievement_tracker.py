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
    players: list[tuple[str, set[str]]] = []

    for name in names:
        achievements: set[str] = gen_player_achievements()
        players.append((name, achievements))
        print(f"Player {name}: {achievements}")

    all_achievements: set[str] = set()
    for name, a in players:
        all_achievements = all_achievements.union(a)
    print(f"All distinct achievements: {all_achievements}")

    common: set[str] = set(ALL_ACHIEVEMENTS)
    for name, a in players:
        common = common.intersection(a)
    print(f"Common achievements: {common}")

    for name, achievements in players:
        others: set[str] = set()
        for other_name, other_a in players:
            if other_name != name:
                others = others.union(other_a)
        unique: set[str] = achievements.difference(others)
        print(f"Only {name} has: {unique}")

    full_set: set[str] = set(ALL_ACHIEVEMENTS)
    for name, achievements in players:
        missing: set[str] = full_set.difference(achievements)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 3 : sets (ensembles) et operations
# =============================================================================
#
# SET :
#   Collection d'elements UNIQUES et NON ORDONNES.
#   Pas de doublons, pas d'index. Accolades {}.
#   {"a", "b", "b"} → {"a", "b"} (doublon supprime)
#
# OPERATIONS SUR LES SETS :
#   union(autre)        → tous les elements des deux (A + B)
#   intersection(autre) → seulement ce qui est dans les deux (A ∩ B)
#   difference(autre)   → ce qui est dans A mais PAS dans B (A - B)
#
# gen_player_achievements() :
#   random.randint(4, 10) → nombre aleatoire entre 4 et 10
#   random.sample(liste, count) → pioche count elements sans repetition
#   set(...) → convertit en ensemble
#
# STOCKAGE DES JOUEURS :
#   On utilise une liste de tuples (nom, set) et PAS un dict,
#   car les dicts ne sont introduits qu'a l'exercice 4.
#   players: list[tuple[str, set[str]]] = []
#   for name, achievements in players: → tuple unpacking
#
# LOGIQUE DES OPERATIONS :
#   Tous distincts : set vide + union de chaque joueur
#   Communs a tous : set complet + intersection de chaque joueur
#   Uniques a un joueur : ses succes - ceux de tous les autres
#   Manquants : tous les succes - ceux du joueur
# =============================================================================
