#!/usr/bin/env python3
import random
from typing import Generator


PLAYERS: list[str] = ["alice", "bob", "charlie", "dylan"]
ACTIONS: list[str] = [
    "run", "move", "climb", "swim", "grab",
    "release", "eat", "sleep", "use",
]


def gen_event() -> Generator[tuple[str, str], None, None]:
    """Infinite generator that yields random game events."""
    while True:
        name: str = random.choice(PLAYERS)
        action: str = random.choice(ACTIONS)
        yield (name, action)


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    """Generator that randomly picks and removes events from list."""
    while len(events) > 0:
        idx: int = random.randint(0, len(events) - 1)
        event: tuple[str, str] = events.pop(idx)
        yield event


def main() -> None:
    """Demonstrate generators with game event streams."""
    print("=== Game Data Stream Processor ===")

    stream: Generator[tuple[str, str], None, None] = gen_event()
    for i in range(1000):
        event: tuple[str, str] = next(stream)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    event_list: list[tuple[str, str]] = []
    for _ in range(10):
        event_list.append(next(stream))
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()


# =============================================================================
# NOTES — Exercice 5 : generateurs (yield)
# =============================================================================
#
# GENERATEUR :
#   Fonction qui utilise yield au lieu de return.
#   yield = "produire une valeur puis se mettre en pause"
#   La fonction ne quitte PAS, elle attend la prochaine demande.
#
# yield vs return :
#   return → quitte definitivement, une seule execution
#   yield  → pause, reprend ou elle s'etait arretee
#
# UTILISATION :
#   g = gen_event()   → cree le generateur (PAS encore execute)
#   next(g)           → execute jusqu'au yield, retourne la valeur
#   next(g)           → reprend apres le yield, re-execute, etc.
#   for e in g:       → appelle next() automatiquement a chaque tour
#
# GENERATEUR INFINI (while True + yield) :
#   Ne plante PAS car yield met en pause entre chaque tour.
#   Le while True ne tourne que quand on appelle next().
#   1000 appels = 1000 tours, pas de boucle infinie.
#
# typing.Generator[YieldType, SendType, ReturnType] :
#   Generator[tuple[str, str], None, None]
#   → produit des tuples (str, str), ne recoit rien, ne retourne rien
#
# random.choice(liste) → pioche un element au hasard
# random.randint(a, b) → entier aleatoire entre a et b inclus
# list.pop(idx) → retire et retourne l'element a l'index idx
#
# PARADIGME :
#   Avant (ex0-ex4) : on stocke TOUT puis on traite.
#   Ici : on produit et consomme au fil de l'eau (streaming).
#   Utile pour les flux massifs (logs, evenements temps reel).
# =============================================================================
