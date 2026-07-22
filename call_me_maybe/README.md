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
   - `number`: only digit and `.` tokens are allowed, the model chooses values
     via greedy decoding. If no decimal point is generated, `.0` is appended.
   - `integer`: only digit tokens are allowed.
   - `boolean`: constrained to `true`/`false` tokens only.
   - `string`: generated token by token with peek-ahead logic to detect closing
     quotes. A leading-space fix strips BPE artifacts from the first token.
   - `regex`: generated freely using a few-shot prompt with structural
     constraints (digit-first tokens blocked) and post-processing (shorthand
     normalization, bracket rebalancing, regex validation).

### Design Decisions

- **Constrained decoding over prompting**: A 0.6B model cannot reliably produce
  valid JSON through prompting alone. Logit filtering guarantees structural
  correctness while letting the model choose semantically.
- **Peek-ahead for quotes**: When generating strings freely, a peek-ahead
  mechanism checks whether a quote token is a closing quote or part of the
  string content, by simulating the quote and checking if the model predicts
  structural JSON next.
- **Few-shot regex prompting**: Regex parameters use a dedicated few-shot prompt
  with examples that include "trap" scenarios (numbers in the source text but
  abstract regex as the answer). A structural constraint blocks digit-first
  tokens to prevent the model from copying literal numbers from the prompt.
- **Greedy decoding**: At each step, the highest-scoring valid token is selected.
  This is simple and fast, though beam search could improve quality.
- **Pydantic models**: Input/output schemas are validated with Pydantic for type
  safety and error handling.

### Performance

- Model: Qwen/Qwen3-0.6B (~600M parameters)
- Each prompt requires multiple forward passes (one per generated token)
- Typical inference: ~30-60 seconds per prompt on CPU, faster on MPS/CUDA
- Public test results: 10/11 correct function calls
- Known limitation: plural-to-character mapping (e.g. "asterisks" -> `*`) depends
  on model reasoning, which the 0.6B model sometimes fails on

### Challenges

- **Quote ambiguity**: Tokens containing `"` can be either a closing quote or
  part of the string content. The peek-ahead mechanism resolves this by
  simulating the closing and checking the model's next prediction.
- **Small model limitations**: A 0.6B model has limited reasoning ability.
  Few-shot prompting and structural constraints compensate for the model's
  inability to reliably produce abstract patterns (like regex) without copying
  literal values from the prompt.
- **BPE tokenization artifacts**: BPE tokens often include a leading space
  (e.g. ` /home` instead of `/home`). The decoder strips leading spaces from
  the first generated string token to preserve exact values.
- **JSON escaping**: Regex patterns like `\d+` require double-escaping
  (`\\d+`) in JSON strings. Backslashes in generated values are escaped before
  force-injection into the JSON structure.
- **Regex generation**: Balancing abstract pattern generation (e.g. `\d+`) with
  literal word matching (e.g. `cat`) required careful few-shot example design
  and structural constraints rather than hardcoded rules.

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
  models.py                # Pydantic data models
  prompt_utils.py          # Prompt building
  io_utils.py              # JSON I/O utilities
data/
  input/
    functions_definition.json
    function_calling_tests.json
llm_sdk/                   # Provided SDK (Qwen3-0.6B wrapper)
```
