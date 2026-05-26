"""higher_magic.py — Higher Realm: Higher-Order Functions."""
from collections.abc import Callable


def spell_combiner(
    spell1: Callable, spell2: Callable
) -> Callable:
    """Combine two spells into one."""
    def combined(
        target: str, power: int
    ) -> tuple[str, str]:
        return (
            spell1(target, power),
            spell2(target, power),
        )
    return combined


def power_amplifier(
    base_spell: Callable, multiplier: int
) -> Callable:
    """Amplify a spell's power by a multiplier."""
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(
    condition: Callable, spell: Callable
) -> Callable:
    """Cast spell only if condition is met."""
    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return caster


def spell_sequence(
    spells: list[Callable]
) -> Callable:
    """Create a sequence of spells cast in order."""
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def main() -> None:
    """Demonstrate higher-order function mastery."""
    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target} for {power} damage"

    def heal(target: str, power: int) -> str:
        return (
            f"Heal restores {target} for {power} HP"
        )

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 50)
    print(f"  Combined: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    mega = power_amplifier(fireball, 3)
    print(f"  Original: {fireball('Dragon', 10)}")
    print(f"  Amplified: {mega('Dragon', 10)}")

    print("\nTesting conditional caster...")
    strong_only = conditional_caster(
        lambda t, p: p >= 30, fireball
    )
    print(f"  Power 50: {strong_only('Dragon', 50)}")
    print(f"  Power 10: {strong_only('Dragon', 10)}")

    print("\nTesting spell sequence...")
    seq = spell_sequence([fireball, heal])
    results = seq("Dragon", 25)
    for r in results:
        print(f"  {r}")

    print("\nCallable checks...")
    print(f"  fireball callable: {callable(fireball)}")
    print(f"  42 callable: {callable(42)}")


if __name__ == "__main__":
    main()
