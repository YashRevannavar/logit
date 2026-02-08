from datetime import timedelta


def _format_duration(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:d}h {minutes:02d}m"


def _render_bar(percentage: float, width: int = 20) -> str:
    filled = int(width * percentage)
    return "█" * filled + "░" * (width - filled)
