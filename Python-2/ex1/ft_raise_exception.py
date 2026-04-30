#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    """Convert a string to a temperature and validate range."""
    temp: int = int(temp_str)
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    return temp


def test_temperature() -> None:
    """Test input_temperature with valid, invalid, and extreme inputs."""
    print("=== Garden Temperature Checker ===")

    test_values: list[str] = ["25", "abc", "100", "-50"]

    for temp_str in test_values:
        print(f"Input data is '{temp_str}'")
        try:
            temp: int = input_temperature(temp_str)
            print(f"Temperature is now {temp}°C")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()


# =============================================================================
# NOTES — Exercice 1 : raise (lancer une erreur volontairement)
# =============================================================================
#
# DIFFERENCE AVEC EX0 :
# Ex0 : c'est PYTHON qui lance l'erreur (int("abc") echoue tout seul)
# Ex1 : c'est TOI qui lances l'erreur avec "raise" quand la valeur
#        ne respecte pas tes regles metier (0-40°C pour les plantes)
#
# "raise" :
#   - C'est un MOT-CLE du langage (comme if, for, return), PAS une fonction
#   - raise ValueError("message") = "STOP, y'a un probleme"
#   - La fonction s'arrete immediatement, pas de return
#   - L'erreur remonte au try/except qui l'entoure
#
# input_temperature (version amelioree) :
#   1. int(temp_str) → si "abc" → ValueError AUTOMATIQUE (Python)
#   2. if temp > 40 → raise ValueError → erreur VOLONTAIRE (toi)
#   3. if temp < 0  → raise ValueError → erreur VOLONTAIRE (toi)
#   4. return temp  → seulement si tout va bien
#
# Le type hint "-> int" :
#   C'est une promesse : "si la fonction REUSSIT, elle retourne un int"
#   Si elle echoue (raise), elle ne retourne rien du tout.
#   Les erreurs ne font pas partie du type de retour.
#
# Les deux types d'erreurs (auto vs volontaire) sont toutes les deux
# des ValueError → le meme "except ValueError" les attrape.
#
# La boucle :
#   Au lieu de copier-coller 4 blocs try/except, on boucle sur une liste.
#   Chaque passage est independant : si "abc" plante, la boucle continue.
# =============================================================================
