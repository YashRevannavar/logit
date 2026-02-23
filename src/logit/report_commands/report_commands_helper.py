from datetime import datetime, timedelta, date
from collections import defaultdict
from typing import Optional
from logit.data_storage.data_store import read_entries
from logit.utilities.models import (
    user_config,
    LogItStatus,
    LogItEntry,
    ProductivityMetrics,
    SessionDistribution,
)


def get_report_entries(
    days: Optional[int] = None, target_date: Optional[date] = None
) -> list[LogItEntry]:
    """Get all entries, either for the last n days or for a specific date."""
    try:
        entries = read_entries(user_config.store_data_at_path)
        if target_date:
            filtered_list = [
                entry for entry in entries if entry.start_time.date() == target_date
            ]
        else:
            days = days or 1
            today = datetime.now().date()
            start_date = today - timedelta(days=days - 1)
            filtered_list = [
                entry for entry in entries if entry.start_time.date() >= start_date
            ]
        return filtered_list[::-1]
    except Exception as e:
        print(f"Error fetching report entries: {e}")
        return []


def get_entry_duration(entry) -> timedelta:
    """Calculate duration, accounting for running tasks."""
    if entry.status == LogItStatus.RUNNING:
        return datetime.now() - entry.start_time
    # handle None duration
    if entry.duration:
        return entry.duration
    return timedelta()


def calculate_deep_work_score(entries: list[LogItEntry]) -> float:
    """
    Calculate the Deep Work Score as a percentage of total work time.

    Calculation Logic:
    1. A session is classified as 'Deep Work' if its duration is >= 45 minutes.
       This is based on the principle that it takes roughly 20-30 minutes to
       reach a state of 'flow' or deep focus.
    2. Total Deep Work Time = Sum of durations of all Deep Work sessions.
    3. Total Work Time = Sum of durations of all tracked sessions.
    4. Deep Work Score = (Total Deep Work Time / Total Work Time) * 100.

    Returns:
        float: The score from 0.0 to 100.0. Returns 0.0 if no work was tracked.
    """
    total_time = timedelta()
    deep_work_time = timedelta()

    for entry in entries:
        duration = get_entry_duration(entry)
        total_time += duration
        # Threshold: 45 minutes
        if duration.total_seconds() >= 45 * 60:
            deep_work_time += duration

    if total_time.total_seconds() == 0:
        return 0.0

    return (deep_work_time.total_seconds() / total_time.total_seconds()) * 100


def get_productivity_metrics(
    entries: list[LogItEntry],
) -> Optional[ProductivityMetrics]:
    """Calculate deep work score, average session length, context switching, and session distribution."""
    if not entries:
        return None

    deep_work_score = calculate_deep_work_score(entries)

    total_duration = timedelta()
    sessions_count = 0
    projects_per_day = defaultdict(set)

    # Session distribution categories
    distribution = SessionDistribution()

    for entry in entries:
        duration = get_entry_duration(entry)
        seconds = duration.total_seconds()

        if seconds > 0:
            total_duration += duration
            sessions_count += 1
            day = entry.start_time.date()
            projects_per_day[day].add(entry.project)

            # Categorize session
            if seconds < 15 * 60:
                distribution.fragmented += 1
            elif seconds < 60 * 60:
                distribution.flow += 1
            else:
                distribution.deep_focus += 1

    if total_duration.total_seconds() == 0:
        return None

    avg_session = total_duration / sessions_count if sessions_count > 0 else timedelta()

    total_days = len(projects_per_day)
    context_switches = (
        sum(len(p) for p in projects_per_day.values()) / total_days
        if total_days > 0
        else 0
    )

    return ProductivityMetrics(
        deep_work_score=deep_work_score,
        avg_session=avg_session,
        total_time=total_duration,
        session_count=sessions_count,
        context_switches=context_switches,
        distribution=distribution,
    )
