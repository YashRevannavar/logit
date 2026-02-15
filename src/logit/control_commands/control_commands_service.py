import click
from logit.control_commands.control_commands_helper import start_command, stop_command
from logit.utilities.display_utils import format_duration

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
        raise click.ClickException("Error starting activity. Please try again.")

    click.secho("▶ START", fg="green", bold=True)
    click.echo(f"  Project  : {click.style(project, bold=True)}")
    if task:
        click.echo(f"  Task     : {task}")
    if tags:
        click.echo(f"  Tags     : {', '.join(tags)}")
    click.echo(f"  Time     : {entry.start_time.strftime('%H:%M:%S')}")


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
        raise click.ClickException("No running activity found.")

    click.secho("■ STOP", fg="red", bold=True)
    click.echo(f"  Project  : {click.style(entry.project, bold=True)}")
    if entry.task:
        click.echo(f"  Task     : {entry.task}")
    if entry.tags:
        click.echo(f"  Tags     : {', '.join(entry.tags)}")

    click.echo(f"  Start    : {entry.start_time.strftime('%H:%M:%S')}")
    if entry.end_time:
        click.echo(f"  End      : {entry.end_time.strftime('%H:%M:%S')}")

    if entry.duration:
        duration_str = format_duration(entry.duration)
        click.echo(f"  Duration : {click.style(duration_str, bold=True)}")
