#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Abstract base class for data processors."""

    name: str = "DataProcessor"

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

    def remaining(self) -> int:
        """Return number of items remaining."""
        return len(self._data)


class NumericProcessor(DataProcessor):
    """Processes int, float, and lists of both."""

    name: str = "Numeric Processor"

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

    name: str = "Text Processor"

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

    name: str = "Log Processor"

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


class DataStream:
    """Routes data elements to appropriate processors."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Register a new data processor."""
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        """Route each element to the appropriate processor."""
        for element in stream:
            processed: bool = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    processed = True
                    break
            if not processed:
                print("DataStream error - Can't process "
                      f"element in stream: {element}")

    def print_processors_stats(self) -> None:
        """Print statistics for all registered processors."""
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(f"{proc.name}: total {proc._total} items "
                  f"processed, remaining {proc.remaining()} "
                  "on processor")


def main() -> None:
    """Test data stream with polymorphic processing."""
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    ds: DataStream = DataStream()
    ds.print_processors_stats()

    print("Registering Numeric Processor")
    num: NumericProcessor = NumericProcessor()
    ds.register_processor(num)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
          "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"]
    ]
    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("Registering other data processors")
    txt: TextProcessor = TextProcessor()
    log: LogProcessor = LogProcessor()
    ds.register_processor(txt)
    ds.register_processor(log)

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        txt.output()
    log.output()
    ds.print_processors_stats()


if __name__ == "__main__":
    main()
