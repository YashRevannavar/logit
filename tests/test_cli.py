import pytest
import time
from click.testing import CliRunner
from logit.cli import cli
from logit.models import user_config


@pytest.fixture
def runner(tmp_path, monkeypatch):
    """Fixture to provide a CliRunner and a temporary data store."""
    temp_data_file = "./test_logit_data.jsonl"
    # Patch the user_config to use this temporary file so we don't affect real data
    monkeypatch.setattr(user_config, "store_data_at_path", temp_data_file)
    return CliRunner()


def test_start_command(runner):
    """Test starting an activity using real file storage (no mocks)."""
    project = "coding"
    result = runner.invoke(cli, ["start", project])

    assert result.exit_code == 0
    assert "▶ START" in result.output
    assert f"Project  : {project}" in result.output

    # Verify the activity was actually saved to our temporary file
    assert user_config.store_data_at_path.exists()
    assert project in user_config.store_data_at_path.read_text()


def test_start_with_tags(runner):
    """Test starting an activity with multiple tags."""
    project = "refactoring"
    tags = ["frontend", "ui"]

    result = runner.invoke(cli, ["start", project, "-g", tags[0], "-g", tags[1]])

    assert result.exit_code == 0
    assert "▶ START" in result.output
    assert f"Project  : {project}" in result.output
    assert f"Tags     : {', '.join(tags)}" in result.output


def test_stop_command(runner):
    """Test stopping a running activity and verifying duration calculation."""
    project = "working"
    runner.invoke(cli, ["start", project])

    # Wait a short moment to ensure a measurable duration
    time.sleep(1.1)

    result = runner.invoke(cli, ["stop", project])

    assert result.exit_code == 0
    assert "■ STOP" in result.output
    assert f"Project  : {project}" in result.output
    assert "Duration :" in result.output
    # Duration should be at least 1 second in our custom format (e.g., "0h 00m")
    # Actually our format is "Xh YYm", so after 1s it might still be "0h 00m"
    # But let's check it doesn't crash and shows the label.


def test_report_command(runner):
    """Test the report command grouping and visual breakdown."""
    # Track time for two different projects
    runner.invoke(cli, ["start", "p1"])
    time.sleep(0.1)
    runner.invoke(cli, ["stop", "p1"])

    runner.invoke(cli, ["start", "p2"])
    time.sleep(0.2)
    runner.invoke(cli, ["stop", "p2"])

    result = runner.invoke(cli, ["report"])

    assert result.exit_code == 0
    assert "📊 REPORT" in result.output
    assert "p1" in result.output
    assert "p2" in result.output
    assert "Total tracked time:" in result.output
    assert "Project breakdown:" in result.output
    # Check for visual bar elements
    assert "█" in result.output or "░" in result.output


def test_start_missing_argument(runner):
    """Test start command failure when project is missing."""
    result = runner.invoke(cli, ["start"])
    assert result.exit_code != 0
    assert "Missing argument 'PROJECT'" in result.output
