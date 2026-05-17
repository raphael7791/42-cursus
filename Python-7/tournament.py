"""Tournament test script for ex2 — Abstract Strategy."""
from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    """Run a tournament between opponents."""
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]
    try:
        for i in range(len(creatures)):
            for j in range(i + 1, len(creatures)):
                c1, s1 = creatures[i]
                c2, s2 = creatures[j]
                print("* Battle *")
                print(c1.describe())
                print("vs.")
                print(c2.describe())
                print("now fight!")
                s1.act(c1)
                s2.act(c2)
    except InvalidStrategyError as e:
        print(f"Battle error, aborting tournament: {e}")


print("Tournament 0 (basic)")
print("[ (Flameling+Normal), (Healing+Defensive) ]")
battle([
    (FlameFactory(), NormalStrategy()),
    (HealingCreatureFactory(), DefensiveStrategy()),
])

print()
print("Tournament 1 (error)")
print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
battle([
    (FlameFactory(), AggressiveStrategy()),
    (HealingCreatureFactory(), DefensiveStrategy()),
])

print()
print("Tournament 2 (multiple)")
print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
battle([
    (AquaFactory(), NormalStrategy()),
    (HealingCreatureFactory(), DefensiveStrategy()),
    (TransformCreatureFactory(), AggressiveStrategy()),
])
