"""space_station.py — Space Station Data Validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Model for a space station with validated fields."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    """Demonstrate valid and invalid station creation."""
    print("Space Station Data Validation")
    print("=" * 40)
    print("Valid station created:")

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15),
        is_operational=True,
    )

    print(f"  ID: {station.station_id}")
    print(f"  Name: {station.name}")
    print(f"  Crew: {station.crew_size} people")
    print(f"  Power: {station.power_level}%")
    print(f"  Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Offline"
    print(f"  Status: {status}")

    print("=" * 40)
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS002",
            name="Test Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime(2024, 1, 1),
        )
    except ValidationError as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
