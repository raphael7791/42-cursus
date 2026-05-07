#!/usr/bin/env python3
import math


def get_player_pos() -> tuple[float, float, float]:
    """Ask user for 3D coordinates and return as tuple."""
    while True:
        raw: str = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )
        parts: list[str] = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            coords: list[float] = []
            for p in parts:
                stripped: str = p.strip()
                coords.append(float(stripped))
            return (coords[0], coords[1], coords[2])
        except ValueError as e:
            bad: str = ""
            for p in parts:
                stripped = p.strip()
                try:
                    float(stripped)
                except ValueError:
                    bad = stripped
                    break
            print(f"Error on parameter '{bad}': {e}")


def distance(p1: tuple[float, float, float],
             p2: tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt(
        (p2[0] - p1[0]) ** 2
        + (p2[1] - p1[1]) ** 2
        + (p2[2] - p1[2]) ** 2
    )


def main() -> None:
    """Demonstrate 3D coordinate system with tuples."""
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    dist_center: float = distance(pos1, (0.0, 0.0, 0.0))
    print(f"Distance to center: {round(dist_center, 4)}")

    print("Get a second set of coordinates")
    pos2: tuple[float, float, float] = get_player_pos()
    dist_between: float = distance(pos1, pos2)
    print(f"Distance between the 2 sets of coordinates: "
          f"{round(dist_between, 4)}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 2 : tuples et coordonnees 3D
# =============================================================================
#
# TUPLE :
#   Comme une liste mais IMMUTABLE (pas modifiable apres creation).
#   Parentheses () au lieu de crochets [].
#   pos = (1.0, 2.5, 3.0)
#   pos[0] → 1.0 (x), pos[1] → 2.5 (y), pos[2] → 3.0 (z)
#   Ideal pour des coordonnees : une position ne doit pas changer.
#
# get_player_pos() :
#   while True → boucle infinie, on sort uniquement avec return
#   input() → demande une saisie utilisateur, retourne une string
#   split(",") → coupe la string a chaque virgule
#   strip() → enleve les espaces autour (" 2.5 " → "2.5")
#   float() → convertit en nombre decimal
#   Si format invalide → "Invalid syntax" + continue (relance la boucle)
#   Si valeur invalide → "Error on parameter" + continue
#   Si tout OK → return (coords) → sort de la boucle
#
# distance() :
#   Theoreme de Pythagore en 3D.
#   ** 2 = au carre, math.sqrt() = racine carree (le symbole √)
#   round(valeur, 4) = arrondir a 4 decimales
#
# OBJECTIF DE L'EXERCICE :
#   Pretexte pour apprendre les tuples. On stocke des positions 3D
#   dans des tuples car une position ne doit pas etre modifiee.
# =============================================================================
