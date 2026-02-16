from datetime import datetime

import click
from logit.control_commands.control_commands_helper import (
    start_command,
    stop_command,
    edit_entry,
)
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


@click.command()
@click.argument("index", type=int, default=1)
@click.option("--project", "-p", help="Update project name")
@click.option("--task", "-t", help="Update task description")
@click.option("--start", help="Update start time (HH:MM)")
@click.option("--end", help="Update end time (HH:MM)")
def edit(
    index: int,
    project: str | None,
    task: str | None,
    start: str | None,
    end: str | None,
):
    """Edit a tracked time entry by index (from `logit ls`)."""

    if not any([project, task, start, end]):
        raise click.ClickException(
            "Please provide at least one field to update (--project, --task, --start, --end)."
        )

    try:
        start_time = None
        end_time = None

        # Parse time inputs (keep same date as original entry)
        if start:
            start_time = datetime.strptime(start, "%H:%M")
        if end:
            end_time = datetime.strptime(end, "%H:%M")

        entry = edit_entry(
            index=index,
            project=project,
            task=task,
            start_time=start_time,
            end_time=end_time,
        )

    except IndexError:
        raise click.ClickException("Entry index out of range.")
    except ValueError:
        raise click.ClickException("Invalid time format. Use HH:MM.")
    except Exception as e:
        raise click.ClickException(f"Failed to edit entry: {e}")

    # ✅ Success Output (consistent with your style)
    click.echo("")
    click.secho("✏ EDITED ENTRY", fg="yellow", bold=True)
    click.echo(f"  Index    : {click.style(str(index), bold=True)}")
    click.echo(f"  Project  : {click.style(entry.project, bold=True)}")

    if entry.task:
        click.echo(f"  Task     : {entry.task}")

    click.echo(f"  Start    : {entry.start_time.strftime('%H:%M')}")
    if entry.end_time:
        click.echo(f"  End      : {entry.end_time.strftime('%H:%M')}")

    if entry.duration:
        duration_str = format_duration(entry.duration)
        click.echo(f"  Duration : {click.style(duration_str, bold=True)}")

    click.echo("")
