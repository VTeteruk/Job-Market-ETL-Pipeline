from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class JobType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"
    FREELANCE = "freelance"
    UNKNOWN = "unknown"


class WorkplaceType(Enum):
    ON_SITE = "on_site"
    REMOTE = "remote"
    HYBRID = "hybrid"


class ExperienceLevel(Enum):
    INTERNSHIP = "internship"
    ENTRY_LEVEL = "entry_level"
    ASSOCIATE = "associate"
    MID_SENIOR = "mid_senior"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


@dataclass
class Vacancy:
    job_id: int
    url: str
    source: str
    title: str
    company: str
    location: str

    job_type: JobType = JobType.FULL_TIME
    workplace_type: WorkplaceType = WorkplaceType.ON_SITE
    experience_level: ExperienceLevel = None

    # Description
    description: Optional[str] = None

    # Compensation
    salary: Optional[str] = None

    # Metadata
    posted_date: Optional[str] = None

    # Engagement metrics
    applicant_count: Optional[int] = None
    view_count: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert the Vacancy instance to a dictionary with enum values as strings."""
        result = {}

        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, Enum):
                # Convert enum to its string value
                result[field_name] = field_value.value
            else:
                # Keep other values as-is
                if field_name == "posted_date":
                    result[field_name] = self._format_date(field_value)
                else:
                    result[field_name] = field_value

        return result

    def _format_date(self, date_str: str) -> datetime.strptime:
        """Convert dates like '17.6.2025' to '2025-06-17'"""
        try:
            return datetime.strptime(date_str.strip(), "%d.%m.%Y").strftime("%Y-%m-%d")
        except Exception as e:
            # Log or handle fallback (e.g. return None or original string)
            print(f"⚠️ Date parse error: {date_str} → {e}")
            return None

