"""space_crew.py — Space Mission Crew Validation."""
from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Ranks available for crew members."""

    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    """Model for a crew member with validated fields."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """Model for a space mission with nested crew validation."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_mission_rules(self) -> 'SpaceMission':
        """Validate business rules for space missions."""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew
                if member.years_experience >= 5
            )
            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions need 50% experienced crew"
                    " (5+ years)"
                )

        inactive = [
            member.name for member in self.crew
            if not member.is_active
        ]
        if inactive:
            raise ValueError(
                f"All crew must be active. Inactive: {inactive}"
            )

        return self


def main() -> None:
    """Demonstrate valid and invalid mission creation."""
    print("Space Mission Crew Validation")
    print("=" * 40)
    print("Valid mission created:")

    commander = CrewMember(
        member_id="CMD001",
        name="Sarah Connor",
        rank=Rank.commander,
        age=45,
        specialization="Mission Command",
        years_experience=20,
    )

    lieutenant = CrewMember(
        member_id="LT002",
        name="John Smith",
        rank=Rank.lieutenant,
        age=35,
        specialization="Navigation",
        years_experience=10,
    )

    officer = CrewMember(
        member_id="OF003",
        name="Alice Johnson",
        rank=Rank.officer,
        age=28,
        specialization="Engineering",
        years_experience=6,
    )

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 12, 1),
        duration_days=900,
        crew=[commander, lieutenant, officer],
        budget_millions=2500.0,
    )

    print(f"  Mission: {mission.mission_name}")
    print(f"  ID: {mission.mission_id}")
    print(f"  Destination: {mission.destination}")
    print(f"  Duration: {mission.duration_days} days")
    print(f"  Budget: ${mission.budget_millions}M")
    print(f"  Crew size: {len(mission.crew)}")
    print("  Crew members:")
    for member in mission.crew:
        print(
            f"    - {member.name} ({member.rank.value})"
            f" - {member.specialization}"
        )

    print("=" * 40)
    print("Expected validation error:")
    try:
        cadet = CrewMember(
            member_id="CAD004",
            name="Bob Junior",
            rank=Rank.cadet,
            age=19,
            specialization="Maintenance",
            years_experience=0,
        )
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime(2024, 6, 1),
            duration_days=30,
            crew=[cadet],
            budget_millions=100.0,
        )
    except ValidationError as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
