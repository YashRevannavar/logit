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


def replace_entry(
    index: int,
    updated_entry: LogItEntry,
    file_path: Path,
) -> None:
    """
    Replace a single LogItEntry in a JSONL file by index (1-based, latest-first).
    """

    if not file_path.exists():
        raise FileNotFoundError("Log file does not exist")

    entries = read_entries(file_path)

    if index < 1 or index > len(entries):
        raise IndexError("Entry index out of range")

    real_index = len(entries) - index

    entries[real_index] = updated_entry

    with file_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            json.dump(_entry_to_dict(entry), f)
            f.write("\n")
