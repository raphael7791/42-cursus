"""Prompt building utilities for function calling."""

from src.models import FunctionDefinition


def _has_regex_function(
    functions: list[FunctionDefinition],
) -> bool:
    """Check if any function uses regex parameters."""
    for f in functions:
        if "regex" in f.name.lower():
            return True
        for pname in f.parameters:
            if "regex" in pname.lower():
                return True
    return False


def _regex_annex() -> str:
    """Build few-shot examples for regex functions."""
    text = "\nExamples:\n\n"
    text += "User request: \"Replace all numbers in "
    text += "'Test 42 and 99' with X\"\n"
    text += '{"name": "fn_substitute_string_with_regex",'
    text += ' "parameters": {'
    text += '"source_string": "Test 42 and 99",'
    text += ' "regex": "\\\\d+",'
    text += ' "replacement": "X"}}\n\n'
    text += "User request: \"Replace all vowels in "
    text += "'Hello World' with stars\"\n"
    text += '{"name": "fn_substitute_string_with_regex",'
    text += ' "parameters": {'
    text += '"source_string": "Hello World",'
    text += ' "regex": "[aeiouAEIOU]",'
    text += ' "replacement": "*"}}\n\n'
    text += "User request: \"Substitute the word "
    text += "'foo' with 'bar' in 'foo is foo'\"\n"
    text += '{"name": "fn_substitute_string_with_regex",'
    text += ' "parameters": {'
    text += '"source_string": "foo is foo",'
    text += ' "regex": "foo",'
    text += ' "replacement": "bar"}}\n\n'
    return text


def build_prompt(
    prompt: str,
    functions: list[FunctionDefinition],
) -> str:
    """Build a prompt for the LLM using ChatML."""
    system = "You are a function calling assistant. "
    system += "Select the appropriate function "
    system += "and extract the exact arguments "
    system += "from the user request.\n"
    system += "Extract values literally from the "
    system += "request. A plural word describes "
    system += "ONE character (asterisks -> *, "
    system += "dots -> ., dashes -> -).\n\n"
    system += "Available functions:\n"

    for f in functions:
        params = ", ".join(
            f"{k}: {v.type}"
            for k, v in f.parameters.items()
        )
        system += (
            f"- {f.name}({params}): "
            f"{f.description}\n"
        )

    if _has_regex_function(functions):
        system += _regex_annex()

    text = "<|im_start|>system\n"
    text += system
    text += "<|im_end|>\n"
    text += "<|im_start|>user\n"
    text += prompt + "\n"
    text += "<|im_end|>\n"
    text += "<|im_start|>assistant\n"

    return text
