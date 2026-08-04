"""Parser for drone simulation map files."""

import re
from typing import Optional

from flying.models.zone import Zone, ZoneType
from flying.models.connection import Connection
from flying.models.graph import Graph


class ParseError(Exception):
    """Error raised when parsing fails."""

    def __init__(self, line_num: int, message: str) -> None:
        """Initialize ParseError.

        Args:
            line_num: Line number where error occurred.
            message: Description of the error.
        """
        self.line_num: int = line_num
        super().__init__(f"Line {line_num}: {message}")


class Parser:
    """Parser for drone simulation map files.

    Parses the input file format into a Graph and drone count.
    """

    VALID_ZONE_TYPES: set[str] = {
        "normal", "blocked", "restricted", "priority"
    }

    @staticmethod
    def parse(filepath: str) -> tuple[Graph, int]:
        """Parse a map file into a Graph and drone count.

        Args:
            filepath: Path to the map file.

        Returns:
            Tuple of (Graph, number of drones).

        Raises:
            ParseError: If the file format is invalid.
        """
        graph = Graph()
        nb_drones: Optional[int] = None
        has_start = False
        has_end = False

        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ParseError(0, f"File not found: {filepath}")
        except IOError as e:
            raise ParseError(0, f"Cannot read file: {e}")

        for line_num, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("nb_drones:"):
                if nb_drones is not None:
                    raise ParseError(
                        line_num, "Duplicate nb_drones definition"
                    )
                nb_drones = Parser._parse_nb_drones(
                    line, line_num
                )

            elif line.startswith("start_hub:"):
                if has_start:
                    raise ParseError(
                        line_num, "Duplicate start_hub definition"
                    )
                zone = Parser._parse_zone(
                    line, line_num, is_start=True
                )
                graph.add_zone(zone)
                has_start = True

            elif line.startswith("end_hub:"):
                if has_end:
                    raise ParseError(
                        line_num, "Duplicate end_hub definition"
                    )
                zone = Parser._parse_zone(
                    line, line_num, is_end=True
                )
                graph.add_zone(zone)
                has_end = True

            elif line.startswith("hub:"):
                zone = Parser._parse_zone(line, line_num)
                try:
                    graph.add_zone(zone)
                except ValueError as e:
                    raise ParseError(line_num, str(e))

            elif line.startswith("connection:"):
                conn = Parser._parse_connection(line, line_num)
                try:
                    graph.add_connection(conn)
                except ValueError as e:
                    raise ParseError(line_num, str(e))
            else:
                raise ParseError(
                    line_num, f"Unknown directive: {line}"
                )

        if nb_drones is None:
            raise ParseError(0, "Missing nb_drones definition")
        if not has_start:
            raise ParseError(0, "Missing start_hub definition")
        if not has_end:
            raise ParseError(0, "Missing end_hub definition")

        return graph, nb_drones

    @staticmethod
    def _parse_nb_drones(line: str, line_num: int) -> int:
        """Parse the nb_drones line.

        Args:
            line: The line to parse.
            line_num: Line number for error reporting.

        Returns:
            Number of drones.

        Raises:
            ParseError: If format is invalid.
        """
        parts = line.split(":", 1)
        value = parts[1].strip()
        try:
            nb = int(value)
        except ValueError:
            raise ParseError(
                line_num,
                f"Invalid nb_drones value: '{value}'"
            )
        if nb <= 0:
            raise ParseError(
                line_num,
                "nb_drones must be a positive integer"
            )
        return nb

    @staticmethod
    def _parse_zone(
        line: str,
        line_num: int,
        is_start: bool = False,
        is_end: bool = False,
    ) -> Zone:
        """Parse a zone definition line.

        Args:
            line: The line to parse.
            line_num: Line number for error reporting.
            is_start: Whether this is a start hub.
            is_end: Whether this is an end hub.

        Returns:
            A Zone object.

        Raises:
            ParseError: If format is invalid.
        """
        metadata_str: Optional[str] = None
        bracket_match = re.search(r"\[(.+?)\]", line)
        if bracket_match:
            metadata_str = bracket_match.group(1)
            line_no_meta = (
                line[: bracket_match.start()]
                + line[bracket_match.end():]
            )
        else:
            line_no_meta = line

        parts = line_no_meta.split(":", 1)
        tokens = parts[1].strip().split()

        if len(tokens) < 3:
            raise ParseError(
                line_num,
                "Zone requires: name x y"
            )

        name = tokens[0]
        if "-" in name:
            raise ParseError(
                line_num,
                f"Zone name cannot contain dashes: '{name}'"
            )
        if " " in name:
            raise ParseError(
                line_num,
                f"Zone name cannot contain spaces: '{name}'"
            )

        try:
            x = int(tokens[1])
            y = int(tokens[2])
        except ValueError:
            raise ParseError(
                line_num,
                f"Invalid coordinates: {tokens[1]} {tokens[2]}"
            )

        zone_type = ZoneType.NORMAL
        color: Optional[str] = None
        max_drones = 1

        if metadata_str:
            meta_items = metadata_str.split()
            for item in meta_items:
                if "=" not in item:
                    raise ParseError(
                        line_num,
                        f"Invalid metadata format: '{item}'"
                    )
                key, value = item.split("=", 1)

                if key == "zone":
                    if value not in Parser.VALID_ZONE_TYPES:
                        raise ParseError(
                            line_num,
                            f"Invalid zone type: '{value}'"
                        )
                    zone_type = ZoneType(value)
                elif key == "color":
                    color = value
                elif key == "max_drones":
                    try:
                        max_drones = int(value)
                    except ValueError:
                        raise ParseError(
                            line_num,
                            f"Invalid max_drones: '{value}'"
                        )
                    if max_drones <= 0:
                        raise ParseError(
                            line_num,
                            "max_drones must be positive"
                        )
                else:
                    raise ParseError(
                        line_num,
                        f"Unknown metadata key: '{key}'"
                    )

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=is_start,
            is_end=is_end,
        )

    @staticmethod
    def _parse_connection(
        line: str, line_num: int
    ) -> Connection:
        """Parse a connection definition line.

        Args:
            line: The line to parse.
            line_num: Line number for error reporting.

        Returns:
            A Connection object.

        Raises:
            ParseError: If format is invalid.
        """
        metadata_str: Optional[str] = None
        bracket_match = re.search(r"\[(.+?)\]", line)
        if bracket_match:
            metadata_str = bracket_match.group(1)
            line_no_meta = (
                line[: bracket_match.start()]
                + line[bracket_match.end():]
            )
        else:
            line_no_meta = line

        parts = line_no_meta.split(":", 1)
        conn_str = parts[1].strip()

        if "-" not in conn_str:
            raise ParseError(
                line_num,
                f"Invalid connection format: '{conn_str}'"
            )

        zone_names = conn_str.split("-", 1)
        zone_a = zone_names[0].strip()
        zone_b = zone_names[1].strip()

        if not zone_a or not zone_b:
            raise ParseError(
                line_num,
                "Connection requires two zone names"
            )

        max_link_capacity = 1
        if metadata_str:
            meta_items = metadata_str.split()
            for item in meta_items:
                if "=" not in item:
                    raise ParseError(
                        line_num,
                        f"Invalid metadata format: '{item}'"
                    )
                key, value = item.split("=", 1)
                if key == "max_link_capacity":
                    try:
                        max_link_capacity = int(value)
                    except ValueError:
                        raise ParseError(
                            line_num,
                            f"Invalid max_link_capacity: '{value}'"
                        )
                    if max_link_capacity <= 0:
                        raise ParseError(
                            line_num,
                            "max_link_capacity must be positive"
                        )
                else:
                    raise ParseError(
                        line_num,
                        f"Unknown connection metadata: '{key}'"
                    )

        return Connection(
            zone_a=zone_a,
            zone_b=zone_b,
            max_link_capacity=max_link_capacity,
        )
