from datetime import timedelta


def format_duration(td: timedelta) -> str:
    """Format duration as 'Xh YYm'."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:d}h {minutes:02d}m"
