#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Abstract base class for data processors."""

    def __init__(self) -> None:
        self._data: list[str] = []
        self._total: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Check if data is appropriate for this processor."""
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process and store input data."""
        ...

    def output(self) -> tuple[int, str]:
        """Extract the oldest piece of data with its rank."""
        if not self._data:
            raise ValueError("No data to output")
        rank: int = self._total - len(self._data)
        value: str = self._data.pop(0)
        return (rank, value)


class NumericProcessor(DataProcessor):
    """Processes int, float, and lists of both."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
            self._total += len(data)
        else:
            self._data.append(str(data))
            self._total += 1


class TextProcessor(DataProcessor):
    """Processes str and lists of strings."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._data.append(item)
            self._total += len(data)
        else:
            self._data.append(data)
            self._total += 1


class LogProcessor(DataProcessor):
    """Processes dict of string key-value pairs and lists of dicts."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(
                isinstance(d, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
                for d in data
            )
        return False

    def _dict_to_str(self, d: dict[str, str]) -> str:
        return ": ".join(d.values())

    def ingest(self, data: dict[str, str]
               | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._data.append(self._dict_to_str(item))
            self._total += len(data)
        else:
            self._data.append(self._dict_to_str(data))
            self._total += 1


def main() -> None:
    """Test the data processor architecture."""
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    num: NumericProcessor = NumericProcessor()
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' "
          "without prior validation:")
    try:
        num.ingest("foo")  # type: ignore
    except ValueError as e:
        print(f"Got exception: {e}")
    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for _ in range(3):
        rank: int
        value: str
        rank, value = num.output()
        print(f"Numeric value {rank}: {value}")

    print("Testing Text Processor...")
    txt: TextProcessor = TextProcessor()
    print(f"Trying to validate input '42': {txt.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    txt.ingest(["Hello", "Nexus", "World"])
    print("Extracting 1 value...")
    rank, value = txt.output()
    print(f"Text value {rank}: {value}")

    print("Testing Log Processor...")
    log: LogProcessor = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    logs: list[dict[str, str]] = [
        {"log_level": "NOTICE",
         "log_message": "Connection to server"},
        {"log_level": "ERROR",
         "log_message": "Unauthorized access!!"}
    ]
    print(f"Processing data: {logs}")
    log.ingest(logs)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
