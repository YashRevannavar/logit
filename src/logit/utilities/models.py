from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, Dict


class LogItStatus(Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"


@dataclass
class LogItEntry:
    project: str
    task: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    status: LogItStatus = field(default=LogItStatus.CREATED)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default=None)

    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


# ---------- Serialization helpers ----------


def _entry_to_dict(entry: LogItEntry) -> dict:
    data = asdict(entry)
    data["status"] = entry.status.value
    data["start_time"] = entry.start_time.isoformat()
    data["end_time"] = entry.end_time.isoformat() if entry.end_time else None
    return data


def _dict_to_entry(data: dict) -> LogItEntry:
    return LogItEntry(
        project=data["project"],
        task=data.get("task"),
        tags=data.get("tags", []),
        status=LogItStatus(data["status"]),
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=(
            datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        ),
    )


@dataclass
class UserConfig:
    time_format: str
    store_data_at_path: Path

    def __post_init__(self):
        if self.time_format not in ["12h", "24h"]:
            raise ValueError("time_format must be either '12h' or '24h'")


@dataclass
class SessionDistribution:
    fragmented: int = 0
    flow: int = 0
    deep_focus: int = 0

    def as_dict(self) -> Dict[str, int]:
        return asdict(self)


@dataclass
class ProductivityMetrics:
    deep_work_score: float
    avg_session: timedelta
    total_time: timedelta
    session_count: int
    context_switches: float
    distribution: SessionDistribution


user_config = UserConfig(
    time_format="24h",
    store_data_at_path=Path.home() / ".logit_data.jsonl",
)
