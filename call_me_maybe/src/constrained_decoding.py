"""Constrained decoding using logit filtering."""

import re
from typing import Any


class ConstrainedDecoder:
    """Constrained decoder using logit filtering."""

    def __init__(
        self, model: Any
    ) -> None:
        self.model = model

        # Mapping token_id -> texte réel via decode()
        all_ids = list(range(self._vocab_size()))
        self.id_to_text: dict[int, str] = {}
        for tid in all_ids:
            self.id_to_text[tid] = model.decode([tid])

        # Mapping inverse texte -> liste de token_ids
        self.text_to_ids: dict[str, list[int]] = {}
        for tid, txt in self.id_to_text.items():
            if txt not in self.text_to_ids:
                self.text_to_ids[txt] = []
            self.text_to_ids[txt].append(tid)

        # Cache standalone quote token id for peek-ahead
        self._quote_id: int = 0
        for tid, txt in self.id_to_text.items():
            if txt == '"':
                self._quote_id = tid
                break

    def _vocab_size(self) -> int:
        """Get vocabulary size from model logits."""
        logits = self.model.get_logits_from_input_ids([0])
        return len(logits)

    def _force_string(
        self, input_ids: list[int], text: str
    ) -> list[int]:
        """Force generation of exact text."""
        ids = self.model.encode(text)[0].tolist()
        input_ids.extend(ids)
        return input_ids

    def _generate_func_name(
        self, input_ids: list[int], names: list[str]
    ) -> list[int]:
        """Generate a valid function name."""
        generated = ""
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            valid = [
                tid
                for tid, txt in self.id_to_text.items()
                if txt and any(
                    n.startswith(generated + txt)
                    for n in names
                )
            ]
            if not valid:
                break
            if generated in names:
                valid.append(self._quote_id)
            best_id = max(valid, key=lambda i: logits[i])
            if best_id == self._quote_id:
                break
            generated += self.id_to_text[best_id]
            input_ids.append(best_id)
        return input_ids

    def _generate_number(
        self, input_ids: list[int]
    ) -> list[int]:
        """Generate a float number."""
        generated = ""
        has_dot = False
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            num_ids = [
                tid
                for tid, txt in self.id_to_text.items()
                if txt.isdigit()
                or (txt == "." and not has_dot)
            ]
            best_all = max(
                range(len(logits)),
                key=lambda i: logits[i],
            )
            if generated and best_all not in num_ids:
                break
            best_num = max(
                num_ids, key=lambda i: logits[i]
            )
            txt = self.id_to_text[best_num]
            if txt == ".":
                has_dot = True
            generated += txt
            input_ids.append(best_num)
        if not has_dot:
            input_ids = self._force_string(
                input_ids, ".0"
            )
        return input_ids

    def _generate_integer(
        self, input_ids: list[int]
    ) -> list[int]:
        """Generate an integer (digits only, no dot)."""
        generated = ""
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            digit_ids = [
                tid
                for tid, txt in self.id_to_text.items()
                if txt.isdigit()
            ]
            best_all = max(
                range(len(logits)),
                key=lambda i: logits[i],
            )
            if generated and best_all not in digit_ids:
                break
            best_digit = max(
                digit_ids, key=lambda i: logits[i]
            )
            generated += self.id_to_text[best_digit]
            input_ids.append(best_digit)
        return input_ids

    def _generate_boolean(
        self, input_ids: list[int]
    ) -> list[int]:
        """Generate true or false."""
        targets = ["true", "false"]
        generated = ""
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            valid = [
                tid
                for tid, txt in self.id_to_text.items()
                if txt and any(
                    t.startswith(generated + txt)
                    for t in targets
                )
            ]
            if not valid:
                break
            best_id = max(valid, key=lambda i: logits[i])
            generated += self.id_to_text[best_id]
            input_ids.append(best_id)
            if generated in targets:
                break
        return input_ids

    def _generate_free(
        self,
        prompt: str,
        max_tokens: int = 60,
        no_digit_start: bool = False,
    ) -> str:
        """Generate text freely without constraints.

        Used for regex patterns where constrained
        decoding would interfere with special chars.
        """
        input_ids = self.model.encode(
            prompt
        )[0].tolist()
        generated: list[int] = []
        for _ in range(max_tokens):
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            best = max(
                range(len(logits)),
                key=lambda i: logits[i],
            )
            txt = self.id_to_text.get(best, "")
            if not txt or txt.isspace():
                break
            if '"' in txt or "\n" in txt:
                break
            if (
                no_digit_start
                and not generated
                and txt[0].isdigit()
            ):
                valid = [
                    t
                    for t in range(len(logits))
                    if self.id_to_text.get(t, "")
                    and not self.id_to_text[t][0]
                    .isdigit()
                    and '"'
                    not in self.id_to_text.get(
                        t, ""
                    )
                    and "\n"
                    not in self.id_to_text.get(
                        t, ""
                    )
                    and not self.id_to_text[t]
                    .isspace()
                ]
                if valid:
                    best = max(
                        valid,
                        key=lambda i: logits[i],
                    )
                    txt = self.id_to_text[best]
                else:
                    break
            input_ids.append(best)
            generated.append(best)
        result: str = str(
            self.model.decode(generated)
        ).strip()
        # Normalize lone shorthand to quantified
        shorthands = (
            "\\d", "\\s", "\\w",
            "\\D", "\\S", "\\W",
        )
        if result in shorthands:
            result += "+"
        # Rebalance unclosed brackets
        open_b = result.count("[") - result.count(
            "]"
        )
        if open_b > 0:
            result += "]" * open_b
        try:
            re.compile(result)
        except re.error:
            result = result.rstrip('+*?}])\\')
        return result

    def _is_closing_quote(
        self, input_ids: list[int]
    ) -> bool:
        """Peek ahead to check if quote closes string.

        Simulates adding a closing quote, then checks
        if the model predicts structural JSON next.
        """
        peek_ids = input_ids + [self._quote_id]
        peek_logits = (
            self.model.get_logits_from_input_ids(
                peek_ids
            )
        )
        peek_best = max(
            range(len(peek_logits)),
            key=lambda i: peek_logits[i],
        )
        peek_txt = self.id_to_text.get(
            peek_best, ""
        ).lstrip()
        if not peek_txt:
            return True
        return peek_txt[0] in ",}]"

    def _generate_string_content(
        self, input_ids: list[int]
    ) -> list[int]:
        """Generate string content until closing quote.

        Content tokens (no quote) and closer tokens
        (starting with quote) compete in the same set.
        When the model picks a closer, peek-ahead
        verifies it is truly a closing quote. If not,
        an escaped quote is injected as content.
        """
        content_ids = [
            tid
            for tid, txt in self.id_to_text.items()
            if txt and '"' not in txt
        ]
        closer_ids = [
            tid
            for tid, txt in self.id_to_text.items()
            if txt and txt.startswith('"')
        ]
        valid = content_ids + closer_ids
        if not valid:
            return input_ids

        first = True
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            best_id = max(
                valid, key=lambda i: logits[i]
            )
            best_txt = self.id_to_text[best_id]
            if best_txt.startswith('"'):
                if self._is_closing_quote(input_ids):
                    break
                input_ids = self._force_string(
                    input_ids, '\\"'
                )
                first = False
                continue
            if first and best_txt.startswith(" "):
                clean = best_txt.lstrip(" ")
                if clean:
                    input_ids = self._force_string(
                        input_ids, clean
                    )
                first = False
                continue
            input_ids.append(best_id)
            first = False
        return input_ids

    def generate(
        self,
        input_ids: list[int],
        func_definitions: dict[str, dict[str, str]],
        prompt: str = "",
    ) -> list[int]:
        """Generate constrained JSON function call."""
        names = list(func_definitions.keys())

        # Force: {"name": "
        input_ids = self._force_string(
            input_ids, '{"name": "'
        )

        # Generate function name (model chooses)
        start = len(input_ids)
        input_ids = self._generate_func_name(
            input_ids, names
        )
        func_name = self.model.decode(
            input_ids[start:]
        )

        # Force: ", "parameters": {
        params = func_definitions[func_name]
        input_ids = self._force_string(
            input_ids, '", "parameters": {'
        )

        # Generate each parameter value
        for i, (pname, ptype) in enumerate(
            params.items()
        ):
            if i > 0:
                input_ids = self._force_string(
                    input_ids, ", "
                )
            input_ids = self._force_string(
                input_ids, f'"{pname}": '
            )
            if ptype == "number":
                input_ids = self._generate_number(
                    input_ids
                )
            elif ptype == "integer":
                input_ids = self._generate_integer(
                    input_ids
                )
            elif ptype == "boolean":
                input_ids = self._generate_boolean(
                    input_ids
                )
            elif "regex" in pname.lower():
                regex_prompt = (
                    "Regex pattern:\n\n"
                    "User: Replace all numbers"
                    " in 'room 7 floor 12'"
                    " with X\n"
                    "Regex: \\d+\n\n"
                    "User: Replace all vowels"
                    " in 'hello' with X\n"
                    "Regex: [aeiouAEIOU]\n\n"
                    "User: Substitute the word"
                    " 'sun' with 'moon' in"
                    " 'sun is bright'\n"
                    "Regex: sun\n\n"
                    "User: " + prompt + "\n"
                    "Regex: "
                )
                val = self._generate_free(
                    regex_prompt,
                    no_digit_start=True,
                )
                escaped = val.replace(
                    "\\", "\\\\"
                )
                input_ids = self._force_string(
                    input_ids, f'"{escaped}"'
                )
            else:
                input_ids = self._force_string(
                    input_ids, '"'
                )
                input_ids = (
                    self._generate_string_content(
                        input_ids
                    )
                )
                input_ids = self._force_string(
                    input_ids, '"'
                )

        # Force: }}
        input_ids = self._force_string(input_ids, "}}")
        return input_ids
