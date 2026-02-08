from datetime import timedelta
from collections import defaultdict
import click

from logit.display_format_helper import _format_duration
from logit.report_commands.report_commands_helper import (
    get_report_entries,
    get_entry_duration,
)


@click.command()
@click.option(
    "--days",
    "-d",
    default=1,
    help="Number of days to include in the report (default: 1)",
    type=int,
)
def report(days: int):
    """Show a compact time tracking report."""
    entries = get_report_entries(days=days)

    if not entries:
        click.echo(
            f"\nNo tracked time found for the last {days} day{'s' if days > 1 else ''}.\n"
        )
        return

    click.echo("\n📊 Time Tracking Report")
    click.echo("=" * 24)

    # Group by project
    project_groups = defaultdict(list)
    for entry in entries:
        project_groups[entry.project].append(entry)

    total_duration_all = timedelta()

    # Sort projects by name
    for project_name in sorted(project_groups.keys()):
        project_entries = project_groups[project_name]

        # Calculate total for this project
        project_total = timedelta()
        for entry in project_entries:
            project_total += get_entry_duration(entry)

        total_duration_all += project_total

        click.echo(f"\n📁 {project_name}: {_format_duration(project_total)}")

        # List tasks
        for i, entry in enumerate(project_entries, 1):
            duration = get_entry_duration(entry)
            date_str = entry.start_time.strftime("%Y-%m-%d")
            start_str = entry.start_time.strftime("%H:%M")
            end_str = entry.end_time.strftime("%H:%M") if entry.end_time else "Present"

            click.echo(
                f"   {i:02d}. [{date_str}] {start_str} - {end_str} ({_format_duration(duration)}) | {entry.task or 'no task'}"
            )

    click.echo(f"\n⏱️  Total: {_format_duration(total_duration_all)}\n")
