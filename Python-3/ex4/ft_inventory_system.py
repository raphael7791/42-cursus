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

    for item, qty in inventory.items():
        pct: float = round(qty / total * 100, 1)
        print(f"Item {item} represents {pct}%")

    most_name: str = ""
    most_qty: int = -1
    least_name: str = ""
    least_qty: int = -1
    for item, qty in inventory.items():
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
