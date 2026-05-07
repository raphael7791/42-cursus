#!/usr/bin/env python3
import sys


def main() -> None:
    """Display command-line arguments information."""
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    arg_count: int = len(sys.argv) - 1
    if arg_count == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {arg_count}")
        i: int = 1
        for arg in sys.argv[1:]:
            print(f"Argument {i}: {arg}")
            i += 1

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 0 : sys.argv et les listes
# =============================================================================
#
# NOTION CLE : sys.argv
#   Quand on tape "python3 script.py hello world", Python stocke tout
#   dans une liste : sys.argv = ["script.py", "hello", "world"]
#   - sys.argv[0] → nom du programme (toujours)
#   - sys.argv[1:] → les arguments (slicing = tout sauf le premier)
#   - len(sys.argv) → nombre total (programme + arguments)
#
# C'EST QUOI UNE LISTE :
#   Collection ordonnee d'elements. Chaque element a un index (position).
#   ma_liste[0] → premier element
#   ma_liste[1:] → du 2eme jusqu'a la fin (slicing)
#   len(ma_liste) → nombre d'elements
#
# import sys :
#   Charge le module sys pour acceder a sys.argv.
#   "import" = charger une boite a outils.
#
# sys.argv[1:] (slicing) :
#   Prend tout a partir de l'index 1 → exclut le nom du programme.
#   On boucle dessus avec for arg in sys.argv[1:]
# =============================================================================
