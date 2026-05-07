#!/usr/bin/env python3
import sys


def main() -> None:
    """Process game scores from command-line arguments."""
    print("=== Player Score Analytics ===")

    if len(sys.argv) < 2:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
        return

    scores: list[int] = []
    for arg in sys.argv[1:]:
        try:
            scores.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")

    if len(scores) == 0:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
        return

    total: int = sum(scores)
    average: float = total / len(scores)

    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {average}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 1 : construire et analyser une liste
# =============================================================================
#
# CONSTRUIRE UNE LISTE :
#   scores: list[int] = []     → liste vide
#   scores.append(42)          → ajoute 42 a la fin
#
# FILTRER LES MAUVAISES DONNEES :
#   try: scores.append(int(arg))   → si ca marche, on ajoute
#   except ValueError:             → si "ab", on affiche l'erreur
#   La boucle CONTINUE avec l'argument suivant (pas de crash).
#
# DEUX VERIFICATIONS :
#   1. len(sys.argv) < 2 → aucun argument du tout
#   2. len(scores) == 0  → des arguments mais TOUS invalides
#   Les deux cas affichent le meme message d'usage.
#
# FONCTIONS DE STATS SUR LES LISTES :
#   sum(scores)  → additionne tout
#   max(scores)  → le plus grand
#   min(scores)  → le plus petit
#   len(scores)  → combien d'elements
#
# MOYENNE :
#   average = total / len(scores)
#   La division / retourne toujours un float en Python.
# =============================================================================
