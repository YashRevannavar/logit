from datetime import datetime, timedelta
from logit.data_storage.data_store import read_entries
from logit.utilities.models import user_config, LogItStatus, LogItEntry


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


def _format_duration(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:d}h {minutes:02d}m"
