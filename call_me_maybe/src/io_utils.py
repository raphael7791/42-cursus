"""I/O utilities for loading and saving JSON data."""

import json
import sys
from src.models import FunctionDefinition, FunctionCalling, Output


def load_functions(path: str) -> list[FunctionDefinition]:
    """Load function definitions from a JSON file."""
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(
            f"Error: invalid JSON in {path}",
            file=sys.stderr,
        )
        sys.exit(1)
    return [FunctionDefinition(**x) for x in data]


def load_prompts(path: str) -> list[FunctionCalling]:
    """Load prompts from a JSON file."""
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(
            f"Error: invalid JSON in {path}",
            file=sys.stderr,
        )
        sys.exit(1)
    return [FunctionCalling(**x) for x in data]


def save_results(
    path: str, results: list[Output]
) -> None:
    """Save function calling results to a JSON file."""
    data = [obj.model_dump() for obj in results]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
