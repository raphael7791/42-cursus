"""functools_artifacts.py — Ancient Library: Functools Treasures."""
import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(
    spells: list[int], operation: str
) -> int:
    """Reduce spell powers using specified operation."""
    if not spells:
        return 0
    ops: dict[str, Callable] = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': max,
        'min': min,
    }
    if operation not in ops:
        raise ValueError(
            f"Unknown operation: {operation}"
        )
    return functools.reduce(ops[operation], spells)


def partial_enchanter(
    base_enchantment: Callable,
) -> dict[str, Callable]:
    """Create partial applications of enchantment."""
    return {
        'fire': functools.partial(
            base_enchantment, 50, "fire"
        ),
        'ice': functools.partial(
            base_enchantment, 50, "ice"
        ),
        'lightning': functools.partial(
            base_enchantment, 50, "lightning"
        ),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number with memoization."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return (
        memoized_fibonacci(n - 1)
        + memoized_fibonacci(n - 2)
    )


def spell_dispatcher() -> Callable[[Any], str]:
    """Create a single dispatch spell system."""
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register(int)
    def _int_spell(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register(str)
    def _str_spell(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register(list)
    def _list_spell(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    _ = (_int_spell, _str_spell, _list_spell)
    return cast


def main() -> None:
    """Demonstrate functools mastery."""
    spells = [10, 20, 30, 40]

    print("Testing spell reducer...")
    print(f"  Sum: {spell_reducer(spells, 'add')}")
    print(
        "  Product:"
        f" {spell_reducer(spells, 'multiply')}"
    )
    print(f"  Max: {spell_reducer(spells, 'max')}")

    print("\nTesting partial enchanter...")

    def enchant(
        power: int, element: str, target: str
    ) -> str:
        return (
            f"{element.title()} enchantment"
            f" ({power}) on {target}"
        )

    enchantments = partial_enchanter(enchant)
    print(f"  {enchantments['fire']('Sword')}")
    print(f"  {enchantments['ice']('Shield')}")
    print(f"  {enchantments['lightning']('Staff')}")

    print("\nTesting memoized fibonacci...")
    print(f"  Fib(0): {memoized_fibonacci(0)}")
    print(f"  Fib(1): {memoized_fibonacci(1)}")
    print(f"  Fib(10): {memoized_fibonacci(10)}")
    print(f"  Fib(15): {memoized_fibonacci(15)}")
    print(
        "  Cache:"
        f" {memoized_fibonacci.cache_info()}"
    )

    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(f"  {cast(42)}")
    print(f"  {cast('fireball')}")
    print(f"  {cast([1, 2, 3])}")
    print(f"  {cast(3.14)}")


if __name__ == "__main__":
    main()
