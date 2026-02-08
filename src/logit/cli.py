import click
from logit.models import LogItEntry, LogItStatus
from logit.control_commands import start_command, stop_command, get_report_data

from logit.display_format_helper import _format_duration

from logit.display_format_helper import _render_bar


# TODO: Implement stop_command / Update operation
# TODO: Implement list command / Read operation
# TODO: Implement specific entry editing commands / Update operation


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """logit — a terminal-first time tracking tool."""


@cli.command()
@click.argument("project")
@click.option(
    "--task",
    "-t",
    help="Task description for the project",
)
@click.option(
    "--tag",
    "-g",
    multiple=True,
    help="Tag for the activity (can be used multiple times)",
)
def start(project: str, task: str | None, tag: tuple[str, ...]):
    """Start tracking an activity."""
    tags = list(tag)

    entry = LogItEntry(
        project=project,
        task=task,
        tags=tags,
        status=LogItStatus.RUNNING,
    )

    if not start_command(entry=entry):
        click.echo("Error starting activity. Please try again.")
        return

    click.echo("▶ START")
    click.echo(f"  Project  : {project}")
    if task:
        click.echo(f"  Task     : {task}")
    if tags:
        click.echo(f"  Tags     : {', '.join(tags)}")
    click.echo(f"  Time     : {entry.start_time.isoformat(timespec='seconds')}")


@cli.command()
@click.argument("project", required=False)
@click.option(
    "--task",
    "-t",
    help="Task description for the project",
)
def stop(project: str | None, task: str | None):
    """Stop the current activity."""
    entry = stop_command(project=project, task=task)

    if not entry:
        click.echo("No running activity found.")
        return

    click.echo("■ STOP")
    click.echo(f"  Project  : {entry.project}")
    if entry.task:
        click.echo(f"  Task     : {entry.task}")
    if entry.tags:
        click.echo(f"  Tags     : {', '.join(entry.tags)}")

    click.echo(f"  Start    : {entry.start_time.isoformat(timespec='seconds')}")
    click.echo(f"  End      : {entry.end_time.isoformat(timespec='seconds')}")

    if entry.duration:
        duration_str = _format_duration(entry.duration)
        click.echo(f"  Duration : {duration_str}")


@cli.command()
@click.option(
    "--days",
    "-d",
    default=1,
    help="Number of days to include in the report (default: 1)",
    type=int,
)
def report(days: int):
    """Show a time report."""
    click.echo(f"\n📊 REPORT (last {days} day{'s' if days > 1 else ''})")
    click.echo("─" * 50)

    report_data = get_report_data(days=days)

    total_time = report_data["total"]
    projects = report_data["projects"]

    if not projects or total_time.total_seconds() == 0:
        click.echo("No tracked time found for this period.\n")
        return

    click.echo(f"Total tracked time: {_format_duration(total_time)}\n")
    click.echo("Project breakdown:")
    click.echo("─" * 50)
    click.echo(f"{'PROJECT':<10}  {'ACTIVITY':<19}  {'SHARE':>4}  {'TIME':>4}")
    click.echo(f"{'-' * 10}  {'-' * 19}  {'-' * 5}  {'-' * 6}")
    for project, duration in projects:
        ratio = duration / total_time
        bar = _render_bar(ratio)
        percent = int(ratio * 100)
        duration_str = _format_duration(duration)
        click.echo(f"{project:<10} {bar}  {percent:>3}%  {duration_str}")

    click.echo("")
