"""Entry point for the function calling module."""

import argparse
import json
import os
import sys
from src.io_utils import load_functions, load_prompts
from src.io_utils import save_results
from src.prompt_utils import build_prompt
from src.models import Output
from src.constrained_decoding import ConstrainedDecoder
from llm_sdk import Small_LLM_Model  # type: ignore


def main() -> None:
    """Run function calling pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.functions_definition):
        print(
            f"Error: {args.functions_definition} "
            "not found",
            file=sys.stderr,
        )
        sys.exit(1)
    if not os.path.isfile(args.input):
        print(
            f"Error: {args.input} not found",
            file=sys.stderr,
        )
        sys.exit(1)

    functions = load_functions(args.functions_definition)
    prompts = load_prompts(args.input)

    if not functions:
        print(
            "Error: no functions defined",
            file=sys.stderr,
        )
        sys.exit(1)
    if not prompts:
        print(
            "Error: no prompts to process",
            file=sys.stderr,
        )
        sys.exit(1)

    model = Small_LLM_Model()
    decoder = ConstrainedDecoder(model)

    func_definitions = {
        f.name: {
            k: v.type
            for k, v in f.parameters.items()
        }
        for f in functions
    }

    os.makedirs(
        os.path.dirname(args.output), exist_ok=True
    )

    results = []
    total = len(prompts)
    for idx, p in enumerate(prompts, 1):
        print(
            f"[{idx}/{total}] {p.prompt}",
            flush=True,
        )
        text = build_prompt(p.prompt, functions)
        input_ids = model.encode(text)[0].tolist()
        start = len(input_ids)
        output_ids = decoder.generate(
            input_ids, func_definitions, p.prompt
        )
        generated = model.decode(output_ids[start:])
        result = json.loads(generated)
        results.append(Output(
            prompt=p.prompt,
            name=result["name"],
            parameters=result["parameters"],
        ))
        print(f"  -> {result['name']}({result['parameters']})")

    save_results(args.output, results)
    print(f"\nDone: {total} results saved to {args.output}")


if __name__ == "__main__":
    main()
