#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    """Convert a string to a temperature integer."""
    return int(temp_str)


def test_temperature() -> None:
    """Test input_temperature with valid and invalid inputs."""
    print("=== Garden Temperature ===")

    temp_str: str = "25"
    print(f"Input data is '{temp_str}'")
    try:
        temp: int = input_temperature(temp_str)
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    temp_str = "abc"
    print(f"Input data is '{temp_str}'")
    try:
        temp = input_temperature(temp_str)
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()


# =============================================================================
# NOTES — Exercice 0 : try / except (attraper une erreur)
# =============================================================================
#
# CONTEXTE :
# Un capteur de temperature envoie des donnees sous forme de texte.
# Parfois "25" (OK), parfois "abc" (capteur defaillant).
# Sans try/except, int("abc") fait crasher le programme.
#
# input_temperature(temp_str) :
#   - Fonction volontairement simple : elle fait juste int(temp_str)
#   - Elle ne gere AUCUNE erreur elle-meme
#   - Si temp_str est invalide, int() leve un ValueError automatiquement
#   - L'erreur REMONTE a la fonction qui a appele input_temperature
#   - C'est comme une patate chaude : elle la relance vers le haut
#
# test_temperature() :
#   - C'est ICI qu'on attrape l'erreur avec try/except
#   - try: on met le code risque dedans
#   - except ValueError as e: si un ValueError se produit, on l'attrape dans "e"
#   - "as e" permet de lire le message d'erreur (sans ca, on attrape mais on
#     ne peut pas afficher le message)
#   - Le code APRES le except continue normalement = le programme ne crashe pas
#
# Avec "25" :
#   1. try → input_temperature("25") → int("25") → 25 → OK
#   2. print("Temperature is now 25°C") → s'affiche
#   3. except IGNORE (pas d'erreur)
#
# Avec "abc" :
#   1. try → input_temperature("abc") → int("abc") → BOOM ValueError
#   2. Le print juste en dessous n'est JAMAIS atteint
#   3. Python saute directement au except
#   4. e contient : "invalid literal for int() with base 10: 'abc'"
#   5. On affiche le message, le programme continue
#
# Chaine de remontee de l'erreur :
#   int("abc")           → ValueError cree ici
#   input_temperature()  → pas de try/except → l'erreur remonte
#   test_temperature()   → try/except → ATTRAPE ici
#
# Type hints (temp_str: str, -> int) :
#   Ne changent rien a l'execution. C'est de la documentation dans le code.
#   L'outil mypy verifie qu'on respecte ses propres annotations.
#
# if __name__ == "__main__" :
#   S'execute uniquement quand on lance le fichier directement
#   (python3 ft_first_exception.py). Pas quand on l'importe.
# =============================================================================
