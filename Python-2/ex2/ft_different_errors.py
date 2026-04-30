#!/usr/bin/env python3


def garden_operations(operation_number: int) -> None:
    """Execute a faulty operation based on operation_number."""
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 42 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        _ = "hello" + 42  # type: ignore


def test_error_types() -> None:
    """Test and catch different types of errors."""
    print("=== Garden Error Types Demo ===")

    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {type(e).__name__}: {e}")

    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()


# =============================================================================
# NOTES — Exercice 2 : differents types d'exceptions
# =============================================================================
#
# Python a des types d'erreurs differents pour chaque situation :
#   ValueError          → valeur invalide (int("abc"))
#   ZeroDivisionError   → division par zero (42 / 0)
#   FileNotFoundError   → fichier inexistant (open("/nope"))
#   TypeError           → types incompatibles ("hello" + 42)
#
# garden_operations(n) :
#   Code volontairement casse. Chaque numero declenche un type d'erreur.
#   Si n >= 4 → aucun if/elif ne matche → pas d'erreur.
#
# Attraper PLUSIEURS types d'un coup :
#   except (ValueError, ZeroDivisionError, FileNotFoundError, TypeError) as e:
#   Le tuple (...) = "attrape n'importe lequel de ces types"
#   Sans tuple, il faudrait 4 blocs except separes.
#
# type(e).__name__ :
#   type(e) → la classe de l'erreur (<class 'ValueError'>)
#   .__name__ → juste le nom en string ("ValueError")
#   Permet d'afficher QUEL type d'erreur on a attrape.
#
# _ = 42 / 0 :
#   _ est une convention = "variable jetable, je m'en fiche du resultat"
#
# # type: ignore :
#   Dit a mypy d'ignorer l'erreur de type volontaire ("hello" + 42)
# =============================================================================
