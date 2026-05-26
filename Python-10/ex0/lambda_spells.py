"""lambda_spells.py — Lambda Sanctum: Anonymous Functions."""


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort magical artifacts by power level descending."""
    return sorted(
        artifacts, key=lambda a: a['power'], reverse=True
    )


def power_filter(
    mages: list[dict], min_power: int
) -> list[dict]:
    """Filter mages by minimum power level."""
    return list(filter(
        lambda m: m['power'] >= min_power, mages
    ))


def spell_transformer(spells: list[str]) -> list[str]:
    """Transform spell names with magical formatting."""
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Calculate mage power statistics using lambdas."""
    return {
        'max_power': max(
            mages, key=lambda m: m['power']
        )['power'],
        'min_power': min(
            mages, key=lambda m: m['power']
        )['power'],
        'avg_power': round(
            sum(map(lambda m: m['power'], mages))
            / len(mages), 2
        ),
    }


def main() -> None:
    """Demonstrate lambda expression mastery."""
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85,
         'type': 'divination'},
        {'name': 'Fire Staff', 'power': 92,
         'type': 'combat'},
        {'name': 'Healing Stone', 'power': 60,
         'type': 'restoration'},
    ]

    print("Testing artifact sorter...")
    sorted_arts = artifact_sorter(artifacts)
    print(
        f"{sorted_arts[0]['name']}"
        f" ({sorted_arts[0]['power']} power)"
        f" comes before {sorted_arts[1]['name']}"
        f" ({sorted_arts[1]['power']} power)"
    )

    mages = [
        {'name': 'Gandalf', 'power': 95,
         'element': 'fire'},
        {'name': 'Merlin', 'power': 88,
         'element': 'arcane'},
        {'name': 'Novice', 'power': 20,
         'element': 'water'},
    ]

    print("\nTesting power filter...")
    powerful = power_filter(mages, 50)
    for mage in powerful:
        print(
            f"  {mage['name']} (power: {mage['power']})"
        )

    print("\nTesting spell transformer...")
    spells = ['fireball', 'heal', 'shield']
    transformed = spell_transformer(spells)
    print(' '.join(transformed))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"  Max power: {stats['max_power']}")
    print(f"  Min power: {stats['min_power']}")
    print(f"  Avg power: {stats['avg_power']}")


if __name__ == "__main__":
    main()
