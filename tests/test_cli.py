import pytest
from click.testing import CliRunner
from logit.cli import cli
from unittest.mock import patch
from logit.models import LogItEntry, LogItStatus


@pytest.fixture
def runner():
    return CliRunner()


def test_start_command_success(runner):
    """Test starting an activity successfully."""
    activity_name = "coding"

    with patch("logit.cli.start_command") as mock_start:
        mock_start.return_value = True

        result = runner.invoke(cli, ["start", activity_name])

        assert result.exit_code == 0
        assert "▶ START" in result.output
        assert f"Project  : {activity_name}" in result.output
        assert "Time     :" in result.output

        # Verify start_command was called with a LogItEntry
        mock_start.assert_called_once()
        args, kwargs = mock_start.call_args
        entry = kwargs["entry"]
        assert isinstance(entry, LogItEntry)
        assert entry.project == activity_name
        assert entry.status == LogItStatus.RUNNING


def test_start_command_with_tags(runner):
    """Test starting an activity with tags."""
    activity_name = "refactoring"
    tags = ["frontend", "ui"]

    with patch("logit.cli.start_command") as mock_start:
        mock_start.return_value = True

        # Using -t multiple times as supported by the CLI
        result = runner.invoke(
            cli, ["start", activity_name, "-g", tags[0], "-g", tags[1]]
        )

        assert result.exit_code == 0
        assert "▶ START" in result.output
        assert f"Project  : {activity_name}" in result.output
        assert f"Tags     : {', '.join(tags)}" in result.output

        # Verify entry has correct tags
        args, kwargs = mock_start.call_args
        entry = kwargs["entry"]
        assert entry.tags == tags


def test_start_command_failure(runner):
    """Test handling of start_command failure."""
    with patch("logit.cli.start_command") as mock_start:
        mock_start.return_value = False

        result = runner.invoke(cli, ["start", "failed_activity"])

        assert (
            result.exit_code == 0
        )  # click commands usually return 0 unless an exception is raised
        assert "Error starting activity. Please try again." in result.output
        assert "▶ START" not in result.output


def test_start_missing_argument(runner):
    """Test start command without required activity argument."""
    result = runner.invoke(cli, ["start"])
    assert result.exit_code != 0
    assert "Missing argument 'PROJECT'" in result.output
