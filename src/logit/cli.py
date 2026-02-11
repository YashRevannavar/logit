import click


# TODO: Implement stop_command / Update operation
# TODO: Implement list command / Read operation
# TODO: Implement specific entry editing commands / Update operation


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """logit — a terminal-first time tracking tool."""


# Import and register commands from other services
from logit.control_commands.control_commands_service import start, stop  # noqa
from logit.report_commands.report_commands_service import report, analyze  # noqa

cli.add_command(cmd=start)
cli.add_command(cmd=stop)
cli.add_command(cmd=report)
cli.add_command(cmd=analyze)
