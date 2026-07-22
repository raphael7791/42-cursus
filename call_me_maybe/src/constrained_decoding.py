"""Constrained decoding using logit filtering."""

from typing import Any
from src.extract import extract_string_value
from src.extract import extract_numbers


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
            best_id = max(valid, key=lambda i: logits[i])
            generated += self.id_to_text[best_id]
            input_ids.append(best_id)
            if generated in names:
                can_extend = any(
                    n.startswith(generated)
                    and n != generated
                    for n in names
                )
                if not can_extend:
                    break
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

    def _is_closing_quote(
        self, input_ids: list[int]
    ) -> bool:
        """Peek ahead to check if quote closes string.

        Uses the standalone quote token to simulate
        closing, then checks if the model predicts
        structural JSON next (, or } or ]).
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
        """Generate string content until quote.

        Uses peek-ahead to distinguish closing quotes
        from quotes that are part of string content.
        Tracks bracket/paren balance to avoid
        generating structurally broken strings.
        """
        open_parens = 0
        open_brackets = 0
        while True:
            logits = self.model.get_logits_from_input_ids(
                input_ids
            )
            best_all = max(
                range(len(logits)),
                key=lambda i: logits[i],
            )
            best_txt = self.id_to_text.get(best_all, "")
            if (
                '"' in best_txt
                and open_parens <= 0
                and open_brackets <= 0
            ):
                idx = best_txt.index('"')
                after = best_txt[idx + 1:].lstrip()
                if after and after[0] in ",}]":
                    break
                if not after and best_txt.strip() != '"':
                    break
                if best_txt.strip() == '"':
                    if self._is_closing_quote(
                        input_ids
                    ):
                        break
                input_ids = self._force_string(
                    input_ids, '\\"'
                )
                continue
            valid = [
                tid
                for tid, txt in self.id_to_text.items()
                if txt and '"' not in txt
            ]
            if not valid:
                break
            best_id = max(
                valid, key=lambda i: logits[i]
            )
            txt = self.id_to_text[best_id]
            open_parens += txt.count(
                "("
            ) - txt.count(")")
            open_brackets += txt.count(
                "["
            ) - txt.count("]")
            input_ids.append(best_id)
        close = "]" * max(0, open_brackets)
        close += ")" * max(0, open_parens)
        if close:
            input_ids = self._force_string(
                input_ids, close
            )
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

        # Pre-extract numbers from prompt
        prompt_numbers = extract_numbers(prompt)
        num_idx = 0

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
                if num_idx < len(prompt_numbers):
                    val = prompt_numbers[num_idx]
                    num_idx += 1
                    if "." not in val:
                        val += ".0"
                    input_ids = self._force_string(
                        input_ids, val
                    )
                else:
                    input_ids = self._generate_number(
                        input_ids
                    )
            elif ptype == "integer":
                if num_idx < len(prompt_numbers):
                    val = prompt_numbers[num_idx]
                    num_idx += 1
                    val = val.split(".")[0]
                    input_ids = self._force_string(
                        input_ids, val
                    )
                else:
                    input_ids = self._generate_integer(
                        input_ids
                    )
            elif ptype == "boolean":
                input_ids = self._generate_boolean(
                    input_ids
                )
            else:
                candidate = extract_string_value(
                    prompt, pname, func_name
                )
                if candidate is not None:
                    escaped = candidate.replace(
                        '\\', '\\\\'
                    ).replace('"', '\\"')
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
