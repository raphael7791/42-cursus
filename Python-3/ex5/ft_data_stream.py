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
