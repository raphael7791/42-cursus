"""Prompt building utilities for function calling."""

from src.models import FunctionDefinition


def build_prompt(
    prompt: str,
    functions: list[FunctionDefinition],
) -> str:
    """Build a prompt for the LLM."""
    text = "You are a function calling assistant.\n"
    text += "Select the appropriate function "
    text += "and extract the exact arguments "
    text += "from the user request.\n"
    text += "Extract values literally from the "
    text += "request. Convert descriptions to "
    text += "their symbol (e.g. asterisks -> *).\n\n"
    text += "Available functions:\n"

    for f in functions:
        params = ", ".join(
            f"{k}: {v.type}"
            for k, v in f.parameters.items()
        )
        text += (
            f"- {f.name}({params}): "
            f"{f.description}\n"
        )

    text += f'\nUser request: "{prompt}"\n\n'
    text += "Respond with a JSON object:\n"

    return text
