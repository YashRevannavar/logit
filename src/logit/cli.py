import click
from logit.models import LogItEntry, LogItStatus
from logit.control_commands import start_command, stop_command


# TODO: Implement stop_command / Update operation
# TODO: Implement list command / Read operation
# TODO: Implement report command / Read operation
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
        # Format duration to HH:MM:SS
        total_seconds = int(
            entry.duration.total_seconds()
        )  # TODO: handle the printing in different .py file later
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        click.echo(f"  Duration : {duration_str}")


@cli.command()
@click.argument(
    "period",
    type=click.Choice(["day", "week", "month"], case_sensitive=False),
)
def report(period: str):
    """Show a time report."""
    click.echo(f"📊 REPORT ({period.upper()})")
    click.echo("  (not implemented yet)")
