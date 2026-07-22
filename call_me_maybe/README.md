*This project has been created as part of the 42 curriculum by rbriguet.*

# Call Me Maybe

Introduction to function calling in LLMs with constrained decoding.

## Description

This project translates natural language prompts into structured JSON function
calls using the **Qwen/Qwen3-0.6B** language model. Instead of relying on
prompting alone, it uses **constrained decoding** (logit filtering) to guarantee
100% valid JSON output.

### Algorithm

The constrained decoder works by restricting the model's token vocabulary at
each generation step:

1. **Force structural tokens** (`{"name": "`, `", "parameters": {`, `}}`) —
   exact tokens are injected to guarantee valid JSON structure.
2. **Function name selection** — tokens are filtered to valid prefixes of
   known function names. The model's logits determine which function is chosen.
3. **Parameter value generation** — depends on type:
   - `number`: pre-extracted from the prompt, forced as floats.
   - `integer`: pre-extracted from the prompt, forced as ints.
   - `boolean`: constrained to `true`/`false` tokens only.
   - `string`: pre-extracted from the prompt when possible (quoted strings,
     file paths, encodings, etc.), otherwise generated freely with
     peek-ahead logic to detect closing quotes.

A **prompt pre-extraction** step (`extract.py`) parses the user prompt to find
candidate values (numbers, quoted strings, paths, encodings, etc.) before
generation. This ensures exact values are preserved instead of relying on the
small model to reproduce them token by token.

### Design Decisions

- **Constrained decoding over prompting**: A 0.6B model cannot reliably produce
  valid JSON through prompting alone. Logit filtering guarantees structural
  correctness while letting the model choose semantically.
- **Pre-extraction of values**: String and number values are extracted directly
  from the prompt using regex patterns, then force-injected into the JSON.
  This compensates for the small model's limited ability to reproduce exact
  values during free generation.
- **Peek-ahead for quotes**: When generating strings freely, a peek-ahead
  mechanism checks whether a quote token is a closing quote or part of the
  string content, by simulating the quote and checking if the model predicts
  structural JSON next.
- **Greedy decoding**: At each step, the highest-scoring valid token is selected.
  This is simple and fast, though beam search could improve quality.
- **Pydantic models**: Input/output schemas are validated with Pydantic for type
  safety and error handling.

### Performance

- Model: Qwen/Qwen3-0.6B (~600M parameters)
- Each prompt requires multiple forward passes (one per generated token)
- Typical inference: ~30-60 seconds per prompt on CPU, faster on MPS/CUDA

### Challenges

- **Quote ambiguity**: Tokens containing `"` can be either a closing quote or
  part of the string content. The peek-ahead mechanism resolves this by
  simulating the closing and checking the model's next prediction.
- **Small model limitations**: A 0.6B model has limited reasoning ability.
  Pre-extracting values from the prompt compensates for the model's inability
  to reliably reproduce exact strings, numbers, and special characters.
- **JSON escaping**: Regex patterns like `\d+` require double-escaping
  (`\\d+`) in JSON strings. Backslashes and quotes in extracted values must
  be properly escaped before force-injection.

## Instructions

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
make install
```

### Usage

```bash
make run        # Run function calling on test prompts
make debug      # Run with Python debugger (pdb)
make lint       # Run flake8 + mypy
make clean      # Remove caches and output
```

Custom input/output:
```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Testing

```bash
make run
cat data/output/function_calling_results.json
```

Expected output for the 3 test prompts:
- `"What is the sum of 2 and 3?"` -> `fn_add_numbers(a=2.0, b=3.0)`
- `"Greet shrek"` -> `fn_greet(name="shrek")`
- `"Reverse the string 'hello'"` -> `fn_reverse_string(s="hello")`

## Resources

- [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) — Language model
- [Constrained Decoding](https://arxiv.org/abs/2307.09702) — Guided generation
- [GPT-2 BPE](https://github.com/openai/gpt-2) — Byte-to-unicode tokenization

### AI Usage

AI (Claude) was used as a development assistant for:
- Debugging the BPE byte-to-unicode encoding mismatch
- Implementing the constrained decoding logic
- Writing boilerplate code (Makefile, Pydantic models, I/O utilities)
- Code review and flake8/mypy compliance

The core algorithm design and architecture decisions were made by the student.

## Project Structure

```
src/
  __init__.py
  __main__.py              # Entry point and orchestration
  constrained_decoding.py  # Core constrained decoder
  extract.py               # Prompt value pre-extraction
  models.py                # Pydantic data models
  prompt_utils.py          # Prompt building
  io_utils.py              # JSON I/O utilities
data/
  input/
    functions_definition.json
    function_calling_tests.json
llm_sdk/                   # Provided SDK (Qwen3-0.6B wrapper)
```
