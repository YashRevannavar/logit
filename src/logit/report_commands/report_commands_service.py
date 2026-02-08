import click

from logit.cli import cli
from logit.control_commands.control_commands_helper import get_report_data
from logit.display_format_helper import _format_duration, _render_bar


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
