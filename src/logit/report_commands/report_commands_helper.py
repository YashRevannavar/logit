from datetime import datetime, timedelta
from logit.data_store import read_entries
from logit.models import user_config, LogItStatus, LogItEntry


def get_report_entries(days: int = 1) -> list[LogItEntry]:
    """Get all entries from the last n days."""
    try:
        entries = read_entries(user_config.store_data_at_path)
        today = datetime.now().date()
        start_date = today - timedelta(days=days - 1)

        # Filter entries by start_time date
        return [entry for entry in entries if entry.start_time.date() >= start_date]
    except Exception as e:
        print(f"Error fetching report entries: {e}")
        return []


def get_entry_duration(entry) -> timedelta:
    """Calculate duration, accounting for running tasks."""
    if entry.status == LogItStatus.RUNNING:
        return datetime.now() - entry.start_time
    return entry.duration
