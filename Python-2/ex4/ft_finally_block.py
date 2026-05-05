#!/usr/bin/env python3


class GardenError(Exception):
    """Base error for garden problems."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Error for plant-related problems."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    """Water a plant. Raises PlantError if name is not capitalized."""
    if plant_name != plant_name.capitalize():
        raise PlantError(
            f"Invalid plant name to water: '{plant_name}'"
        )
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str]) -> None:
    """Test the watering system with a list of plants."""
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


def main() -> None:
    """Demonstrate the finally block with the watering system."""
    print("=== Garden Watering System ===")

    print("Testing valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])

    print("\nTesting invalid plants...")
    test_watering_system(["Tomato", "lettuce", "Carrots"])

    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 4 : finally (nettoyage garanti)
# =============================================================================
#
# CONTEXTE :
# On ouvre une vanne d'arrosage. Si le programme plante, il faut
# quand meme la fermer. finally garantit que ca arrive TOUJOURS.
#
# water_plant(plant_name) :
#   Verifie si le nom est capitalise avec capitalize().
#   "lettuce".capitalize() → "Lettuce" → different → raise PlantError
#   "Tomato".capitalize() → "Tomato" → identique → on arrose
#
# test_watering_system(plants) :
#   Structure complete : try / except / finally
#   - try : arrose chaque plante dans une boucle
#   - except : si PlantError, affiche l'erreur et fait return
#   - finally : ferme le systeme QUOI QU'IL ARRIVE
#
# ORDRE D'EXECUTION en cas d'erreur :
#   1. try → code s'execute jusqu'a l'erreur
#   2. except → attrape l'erreur, affiche le message
#   3. finally → s'execute AVANT le return
#   4. return → maintenant on quitte la fonction
#
# POINT CLE : finally gagne toujours.
#   - Pas d'erreur → try puis finally
#   - Erreur attrapee → try puis except puis finally
#   - Erreur + return → try puis except puis finally PUIS return
#
# Sans finally, un simple print a la fin de la fonction ne
# s'executerait jamais en cas de return dans le except.
#
# Cas d'usage reel : fermer un fichier, une connexion base de
# donnees, liberer un verrou, couper un moteur...
# =============================================================================
