import click
from datetime import datetime


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """logit — a terminal-first time tracking tool."""


@cli.command()
@click.argument("activity")
@click.option(
    "--tags",
    "-t",
    multiple=True,
    help="Tags for the activity (can be used multiple times)",
)
def start(activity: str, tags: tuple[str, ...]):
    """Start tracking an activity."""
    now = datetime.now().isoformat(timespec="seconds")

    click.echo("▶ START")
    click.echo(f"  Activity : {activity}")
    click.echo(f"  Tags     : {', '.join(tags) if tags else '-'}")
    click.echo(f"  Time     : {now}")


@cli.command()
def stop():
    """Stop the current activity."""
    now = datetime.now().isoformat(timespec="seconds")

    click.echo("■ STOP")
    click.echo(f"  Time     : {now}")


@cli.command()
@click.argument(
    "period",
    type=click.Choice(["day", "week", "month"], case_sensitive=False),
)
def report(period: str):
    """Show a time report."""
    click.echo(f"📊 REPORT ({period.upper()})")
    click.echo("  (not implemented yet)")
