import click
from logit.control_commands.control_commands_helper import start_command, stop_command
from logit.report_commands.report_commands_helper import _format_duration
from logit.utilities.models import LogItEntry, LogItStatus


@click.command()
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
def start(project: str, task: str | None, tag: tuple[str]):
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


@click.command()
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
