import json
from pathlib import Path
from typing import List

from logit.utilities.models import LogItEntry, _entry_to_dict, _dict_to_entry


def save_entry(entry: LogItEntry, file_path: Path) -> None:
    """
    Append a LogItEntry to a JSONL file.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("a", encoding="utf-8") as f:
        json.dump(_entry_to_dict(entry), f)
        f.write("\n")


def save_entries(entries: List[LogItEntry], file_path: Path) -> None:
    """
    Overwrite the JSONL file with the provided LogItEntry objects.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            json.dump(_entry_to_dict(entry), f)
            f.write("\n")


def read_entries(file_path: Path) -> List[LogItEntry]:
    """
    Read all LogItEntry objects from a JSONL file.
    """
    if not file_path.exists():
        return []

    entries: List[LogItEntry] = []

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            entries.append(_dict_to_entry(data))

    return entries
