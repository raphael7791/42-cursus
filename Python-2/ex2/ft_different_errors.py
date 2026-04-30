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
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except TypeError as e:
            print(f"Caught TypeError: {e}")

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
# Attraper PLUSIEURS types avec un seul try :
#   On met plusieurs "except" a la suite dans le meme bloc try.
#   Chaque except attrape un type precis → on sait lequel c'est
#   sans avoir besoin d'appeler type() (qui est INTERDIT par le sujet).
#
# ATTENTION : type() est dans les fonctions NON autorisees.
#   On ne peut PAS faire type(e).__name__. A la place, on utilise
#   des except separes pour chaque type d'erreur.
#
# _ = 42 / 0 :
#   _ est une convention = "variable jetable, je m'en fiche du resultat"
#
# # type: ignore :
#   Dit a mypy d'ignorer l'erreur de type volontaire ("hello" + 42)
# =============================================================================
