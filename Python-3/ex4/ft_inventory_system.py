#!/usr/bin/env python3
import sys


def main() -> None:
    """Parse command-line inventory and perform analysis."""
    print("=== Inventory System Analysis ===")

    inventory: dict[str, int] = {}

    for arg in sys.argv[1:]:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        parts: list[str] = arg.split(":", 1)
        item_name: str = parts[0]
        quantity_str: str = parts[1]
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue
        try:
            quantity: int = int(quantity_str)
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")
            continue
        inventory[item_name] = quantity

    if len(inventory) == 0:
        print("Inventory is empty!")
        return

    print(f"Got inventory: {inventory}")

    item_list: list[str] = list(inventory.keys())
    print(f"Item list: {item_list}")

    total: int = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")

    for item in inventory.keys():
        qty: int = inventory[item]
        pct: float = round(qty / total * 100, 1)
        print(f"Item {item} represents {pct}%")

    most_name: str = ""
    most_qty: int = -1
    least_name: str = ""
    least_qty: int = -1
    for item in inventory.keys():
        qty = inventory[item]
        if most_qty == -1 or qty > most_qty:
            most_name = item
            most_qty = qty
        if least_qty == -1 or qty < least_qty:
            least_name = item
            least_qty = qty

    print(f"Item most abundant: {most_name} with quantity {most_qty}")
    print(f"Item least abundant: {least_name} "
          f"with quantity {least_qty}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 4 : dictionnaires (inventaire)
# =============================================================================
#
# DICTIONNAIRE :
#   Collection de paires cle:valeur. Acces direct par cle.
#   inventaire = {}              → dict vide
#   inventaire["sword"] = 1     → ajouter une paire
#   inventaire["sword"]         → acceder a la valeur (1)
#   "sword" in inventaire       → verifier si la cle existe
#
# METHODES UTILISEES :
#   dict.keys()    → retourne les cles (noms des objets)
#   dict.values()  → retourne les valeurs (quantites)
#   dict.update()  → ajoute/modifie des paires
#   ⚠ dict.items() n'est PAS autorise dans cet exercice
#
# PARSING DES ARGUMENTS :
#   arg.split(":", 1) → coupe "sword:1" en ["sword", "1"]
#   Le 1 en argument = coupe au premier ":" seulement
#   3 cas d'erreur :
#     - pas de ":" dans l'argument → format invalide
#     - quantite pas convertible en int → ValueError
#     - cle deja dans le dict → doublon
#   A chaque erreur → print message + continue (passe au suivant)
#
# STATS SUR LE DICT :
#   sum(dict.values())      → total de toutes les quantites
#   round(qty/total*100, 1) → pourcentage arrondi a 1 decimale
#
# MAX / MIN :
#   On parcourt avec for + comparaison manuelle (> et <)
#   ⚠ Utiliser > strict (pas >=) pour garder le PREMIER en cas
#   d'egalite (Python 3.7+ respecte l'ordre d'insertion)
#
# POURQUOI UN DICT ET PAS UNE LISTE :
#   Avec une liste de tuples [("sword",1), ...], chercher un objet
#   demande de tout parcourir. Avec un dict, inventaire["sword"]
#   donne la valeur immediatement (acces direct par cle).
# =============================================================================
