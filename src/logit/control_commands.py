from datetime import datetime, timedelta
from logit.data_store import save_entry, read_entries, save_entries
from logit.models import user_config, LogItEntry, LogItStatus


def start_command(entry: LogItEntry) -> bool:
    try:
        save_entry(entry=entry, file_path=user_config.store_data_at_path)
        return True
    except Exception as e:
        print(f"Error saving entry: {e}")
        return False


def stop_command(
    project: str | None = None, task: str | None = None
) -> LogItEntry | None:
    try:
        entries = read_entries(user_config.store_data_at_path)
        stopped_entry = None

        for entry in entries:
            if entry.status == LogItStatus.RUNNING:
                if project and entry.project != project:
                    continue
                if task and entry.task != task:
                    continue

                # Found the first matching running entry (FIFO)
                entry.status = LogItStatus.FINISHED
                entry.end_time = datetime.now()
                stopped_entry = entry
                break

        if stopped_entry:
            save_entries(entries, user_config.store_data_at_path)
            return stopped_entry

        return None
    except Exception as e:
        print(f"Error stopping activity: {e}")
        return None


def get_report_data(days: int = 1):
    try:
        entries = read_entries(user_config.store_data_at_path)
        today = datetime.now().date()
        start_date = today - timedelta(days=days - 1)

        # project_name -> total_duration
        project_totals = {}

        for entry in entries:
            # We filter by the date of start_time
            if entry.start_time.date() >= start_date:
                duration = entry.duration
                if entry.status == LogItStatus.RUNNING:
                    duration = datetime.now() - entry.start_time

                if duration:
                    project = entry.project
                    if project not in project_totals:
                        project_totals[project] = timedelta()
                    project_totals[project] += duration

        return project_totals
    except Exception as e:
        print(f"Error generating report: {e}")
        return {}
