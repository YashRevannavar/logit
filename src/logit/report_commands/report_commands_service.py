import json
from datetime import timedelta, datetime
from collections import defaultdict
import click

from logit.report_commands.report_commands_helper import (
    get_report_entries,
    get_entry_duration,
    get_productivity_metrics,
    FLEXIBLE_DATE,
)
from logit.utilities.models import _entry_to_dict
from logit.utilities.display_utils import format_duration


@click.command()
@click.option(
    "--days",
    "-d",
    default=1,
    help="Number of days to include in the report (default: 1)",
    type=int,
)
@click.option(
    "--date",
    "-dt",
    help="Filter entries for a specific date (DD, DD-MM, or DD-MM-YY)",
    type=FLEXIBLE_DATE,
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output report in JSON format",
)
def report(days: int, date: datetime, json_output: bool):
    """Show a compact time tracking report."""
    target_date = date.date() if date else None
    entries = get_report_entries(days=days, target_date=target_date)

    if json_output:
        data = [_entry_to_dict(e) for e in entries]
        click.echo(json.dumps(data, indent=2))
        return

    if not entries:
        if target_date:
            click.echo(
                f"\nNo tracked time found for {target_date.strftime('%d-%m-%y')}.\n"
            )
        else:
            click.echo(
                f"\nNo tracked time found for the last {days} day{'s' if days > 1 else ''}.\n"
            )
        return

    click.echo("")
    click.secho("📊 Time Tracking Report", fg="blue", bold=True)
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

        project_label = click.style(f"📁 {project_name}", fg="cyan", bold=True)
        duration_label = click.style(format_duration(project_total), bold=True)
        click.echo(f"\n{project_label}  {duration_label}")

        # List tasks
        for i, entry in enumerate(project_entries, 1):
            duration = get_entry_duration(entry)
            date_str = click.style(entry.start_time.strftime("%Y-%m-%d"), dim=True)
            start_str = entry.start_time.strftime("%H:%M")
            end_str = (
                entry.end_time.strftime("%H:%M")
                if entry.end_time
                else click.style("Present", fg="yellow")
            )

            idx = click.style(f"{i}.", fg="green")
            dur_str = click.style(f"({format_duration(duration)})", dim=True)

            task_desc = entry.task or click.style("no task", dim=True)

            click.echo(
                f"   {idx} [{date_str}] {start_str} - {end_str} {dur_str} | {task_desc}"
            )

    total_label = click.style("⏱️  Total:", fg="yellow", bold=True)
    total_val = click.style(format_duration(total_duration_all), bold=True)
    click.echo(f"\n{total_label} {total_val}\n")


@click.command()
@click.option(
    "--days",
    "-d",
    default=1,
    help="Number of days to analyze (default: 1)",
    type=int,
)
@click.option(
    "--date",
    "-dt",
    help="Filter entries for a specific date (DD, DD-MM, or DD-MM-YY)",
    type=FLEXIBLE_DATE,
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output analysis in JSON format",
)
def analyze(days: int, date: datetime, json_output: bool):
    """Analyze productivity and focus quality."""
    target_date = date.date() if date else None
    entries = get_report_entries(days=days, target_date=target_date)
    metrics = get_productivity_metrics(entries)

    if json_output:
        if metrics:
            click.echo(json.dumps(metrics.to_dict(), indent=2))
        else:
            click.echo(json.dumps({}, indent=2))
        return

    if not metrics:
        if target_date:
            click.echo(
                f"\nNo data to analyze for {target_date.strftime('%d-%m-%y')}.\n"
            )
        else:
            click.echo(f"\nNo data to analyze for the last {days} days.\n")
        return

    # Header
    click.echo("")
    header_text = click.style("🧠 Productivity Analysis", fg="yellow", bold=True)
    click.echo(header_text)
    click.echo("═" * 50)
    click.echo("")

    # Focus Quality Section
    click.secho("Focus Quality", fg="blue", bold=True)

    score = metrics.deep_work_score
    score_styled = click.style(f"{score:.1f}%", fg="green", bold=True)
    click.echo(f"Deep Work Score: {' ' * 19}{score_styled}")

    # Progress Bar
    bar_width = 40
    filled_width = int((score / 100) * bar_width)
    bar = click.style("█" * filled_width, fg="green")
    empty = click.style("░" * (bar_width - filled_width), fg="green", dim=True)
    click.echo(f"{bar}{empty}")

    # Avg Session
    avg_str = format_duration(metrics.avg_session)
    avg_styled = click.style(avg_str, bold=True)
    click.echo(f"Avg Session: {' ' * 19}{avg_styled}")

    # Context Switching
    switches = metrics.context_switches
    switches_styled = click.style(
        f"{switches:.1f} projects/day", fg="magenta" if switches > 3 else "cyan"
    )
    click.echo(f"Context Switching: {' ' * 15}{switches_styled}")

    click.echo("")

    # Session Distribution Section
    click.secho("Session Distribution", fg="blue", bold=True)
    dist = metrics.distribution

    counts = [dist.fragmented, dist.flow, dist.deep_focus]
    max_count = max(counts) if any(counts) else 1
    # Scale width based on max count, max bar width 30
    scale = 30 / max_count if max_count > 0 else 1

    categories = [
        ("Fragmented (<15m)", dist.fragmented, "white"),  # dimmed white
        ("Flow (15m-1h)    ", dist.flow, "blue"),
        ("Deep Focus (>1h) ", dist.deep_focus, "green"),
    ]

    for label, count, color in categories:
        bar_len = int(count * scale)
        if label.startswith("Fragmented"):
            bar = click.style("█" * bar_len, fg="white", dim=True)
        else:
            bar = click.style("█" * bar_len, fg=color)

        click.echo(f"{label}  {bar} {click.style(str(count), dim=True)}")

    click.echo("")


@click.command()
@click.option(
    "--days",
    "-d",
    default=1,
    help="Number of days to list entries for (default: 7)",
    type=int,
)
@click.option(
    "--date",
    "-dt",
    help="Filter entries for a specific date (DD, DD-MM, or DD-MM-YY)",
    type=FLEXIBLE_DATE,
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output entries in JSON format",
)
def ls(days: int, date: datetime, json_output: bool):
    """List all tracked time entries."""
    target_date = date.date() if date else None
    entries = get_report_entries(days=days, target_date=target_date)

    if json_output:
        data = [_entry_to_dict(e) for e in entries]
        click.echo(json.dumps(data, indent=2))
        return

    if not entries:
        if target_date:
            click.echo(
                f"\nNo tracked time found for {target_date.strftime('%d-%m-%y')}.\n"
            )
        else:
            click.echo(
                f"\nNo tracked time found for the last {days} day{'s' if days > 1 else ''}.\n"
            )
        return

    click.echo("")
    click.secho("📋 Time Entries", fg="blue", bold=True)
    click.echo("=" * 20)

    for i, entry in enumerate(entries, 1):
        duration = get_entry_duration(entry)
        date_str = click.style(entry.start_time.strftime("%Y-%m-%d"), dim=True)
        start_str = entry.start_time.strftime("%H:%M")
        end_str = (
            entry.end_time.strftime("%H:%M")
            if entry.end_time
            else click.style("Present", fg="yellow")
        )

        idx = click.style(f"{i}.", fg="green")
        dur_str = click.style(f"({format_duration(duration)})", dim=True)

        task_desc = entry.task or click.style("no task", dim=True)

        click.echo(
            f"{idx} [{date_str}] {start_str} - {end_str} {dur_str} | {entry.project} | {task_desc}"
        )

    click.echo("")
