"""decorator_mastery.py — Master's Tower: Decorator Mastery."""
import functools
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """Decorator that measures function execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(
            f"Spell completed in {elapsed:.3f} seconds"
        )
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    """Decorator factory that validates power levels."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(
            power: int, *args: Any, **kwargs: Any
        ) -> Any:
            if power < min_power:
                return (
                    "Insufficient power for this spell"
                )
            return func(power, *args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    """Decorator that retries failed spells."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying..."
                            " (attempt"
                            f" {attempt}"
                            f"/{max_attempts})"
                        )
            return (
                "Spell casting failed after"
                f" {max_attempts} attempts"
            )
        return wrapper
    return decorator


class MageGuild:
    """A guild of mages with spell casting abilities."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Check if a mage name is valid."""
        return len(name) >= 3 and all(
            c.isalpha() or c == ' ' for c in name
        )

    def cast_spell(
        self, spell_name: str, power: int
    ) -> str:
        """Cast a spell with validated power level."""
        @power_validator(min_power=10)
        def _cast(power: int) -> str:
            return (
                f"Successfully cast {spell_name}"
                f" with {power} power"
            )
        return str(_cast(power))


def main() -> None:
    """Demonstrate decorator mastery."""
    print("Testing spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.1)
        return "Fireball cast!"

    result = fireball()
    print(f"Result: {result}")

    print("\nTesting retrying spell...")

    @retry_spell(max_attempts=3)
    def unstable() -> str:
        raise ValueError("Spell unstable!")

    print(unstable())

    @retry_spell(max_attempts=3)
    def waaaaaaagh() -> str:
        return "Waaaaaaagh spelled !"

    print(waaaaaaagh())

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(guild.validate_mage_name("Gandalf"))
    print(guild.validate_mage_name("Ab"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
