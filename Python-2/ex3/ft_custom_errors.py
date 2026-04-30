#!/usr/bin/env python3


class GardenError(Exception):
    """Base error for garden problems."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Error for plant-related problems."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    """Error for watering-related problems."""

    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def check_plant(name: str) -> None:
    """Raise PlantError if plant is wilting."""
    raise PlantError(f"The {name} plant is wilting!")


def check_water(level: int) -> None:
    """Raise WaterError if water level is too low."""
    if level < 10:
        raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    """Demonstrate custom garden errors."""
    print("=== Custom Garden Errors Demo ===")

    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("Testing WaterError...")
    try:
        check_water(5)
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("Testing catching all garden errors...")
    try:
        check_plant("tomato")
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    try:
        check_water(5)
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()


# =============================================================================
# NOTES — Exercice 3 : exceptions personnalisees (heritage de classes)
# =============================================================================
#
# POURQUOI CREER SES PROPRES EXCEPTIONS :
# Les exceptions Python (ValueError etc.) sont trop generiques.
# Avec PlantError et WaterError, on sait immediatement d'ou vient
# le probleme. C'est plus precis et plus lisible.
#
# CLASSES :
#   class = un moule pour creer des objets
#   class X(Y) = X herite de Y = X EST un Y
#   __init__ = constructeur, la notice de montage (s'execute a la creation)
#   self = l'objet lui-meme (obligatoire, passe automatiquement par Python)
#   super().__init__() = "execute aussi la notice du parent"
#
# HIERARCHIE :
#   Exception → GardenError → PlantError
#   Exception → GardenError → WaterError
#
# POURQUOI LE __init__ + super() :
#   On reecrit __init__ UNIQUEMENT pour ajouter un message par defaut
#   (= "Unknown plant error"). Sans cette demande du sujet, un simple
#   "pass" aurait suffi.
#   super().__init__(message) passe le message a Exception pour que
#   print(e) fonctionne. Sans ca, le message ne serait jamais stocke.
#
# HERITAGE DANS LES EXCEPT :
#   except PlantError → attrape UNIQUEMENT PlantError
#   except GardenError → attrape GardenError ET PlantError ET WaterError
#   Car PlantError EST un GardenError (par heritage).
#   C'est comme "un chien est un animal" : si tu attrapes tous les
#   animaux, tu attrapes aussi les chiens.
#
# DIFFERENCE AVEC EX2 :
#   Ex2 : on utilise des erreurs que Python a deja creees (ValueError etc.)
#   Ex3 : on CREE nos propres classes d'erreurs et on les lance avec raise
#   Mais le mecanisme est le meme : ce sont toutes des classes qui
#   heritent de Exception.
# =============================================================================
