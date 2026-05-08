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


# =============================================================================
# NOTES — Exercice 6 : comprehensions (list & dict)
# =============================================================================
#
# LIST COMPREHENSION :
#   Sucre syntaxique = meme resultat qu'une boucle, en une ligne.
#
#   Sans : resultat = []
#          for n in players: resultat.append(n.capitalize())
#
#   Avec : resultat = [n.capitalize() for n in players]
#
#   Structure : [expression for element in liste]
#
# AVEC FILTRE (if) :
#   [n for n in players if n[0].isupper()]
#   → garde seulement les noms deja capitalises
#   Structure : [expression for element in liste if condition]
#
# DICT COMPREHENSION :
#   Meme principe, avec accolades et cle:valeur
#   {name: random.randint(50, 950) for name in all_capitalized}
#   Structure : {cle: valeur for element in liste}
#
#   Avec filtre :
#   {name: score for name, score in scores.items() if score > avg}
#
# OUTILS :
#   .capitalize()   → "bob" → "Bob" (1ere lettre majuscule)
#   .isupper()      → True si le caractere est majuscule
#   n[0]            → premier caractere d'une string
#   scores.items()  → paires (cle, valeur) d'un dict
#   sum() / len()   → pour calculer la moyenne
#
# QUAND UTILISER :
#   Comprehension = ideal si la logique est simple (1 expression).
#   Si trop complexe → boucle classique plus lisible.
#   Doit tenir sur une ligne (ou couper proprement pour flake8).
# =============================================================================
