import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """logit — a terminal-first time tracking tool."""


# Import and register commands from other services
from logit.control_commands.control_commands_service import start, stop  # noqa
from logit.report_commands.report_commands_service import (  # noqa
    report,
    analyze,
    ls,
)

cli.add_command(cmd=start)
cli.add_command(cmd=stop)
cli.add_command(cmd=report)
cli.add_command(cmd=analyze)
cli.add_command(cmd=ls)
