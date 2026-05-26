"""scope_mysteries.py — Memory Depths: Closures and Scoping."""
from collections.abc import Callable


def mage_counter() -> Callable:
    """Create a counting closure."""
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    """Create a power accumulator closure."""
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return accumulate


def enchantment_factory(
    enchantment_type: str,
) -> Callable:
    """Create enchantment functions via closure."""
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    """Create a memory management system."""
    storage: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        storage[key] = value

    def recall(key: str) -> object:
        return storage.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main() -> None:
    """Demonstrate lexical scoping and closures."""
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"  counter_a call 1: {counter_a()}")
    print(f"  counter_a call 2: {counter_a()}")
    print(f"  counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"  Base 100, add 20: {acc(20)}")
    print(f"  Base 100, add 30: {acc(30)}")

    print("\nTesting enchantment factory...")
    flame = enchantment_factory("Flaming")
    frost = enchantment_factory("Frozen")
    print(f"  {flame('Sword')}")
    print(f"  {frost('Shield')}")

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault['store']('secret', 42)
    print("  Store 'secret' = 42")
    print(
        "  Recall 'secret':"
        f" {vault['recall']('secret')}"
    )
    print(
        "  Recall 'unknown':"
        f" {vault['recall']('unknown')}"
    )


if __name__ == "__main__":
    main()
