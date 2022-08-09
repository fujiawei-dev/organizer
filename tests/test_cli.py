"""Tests for `organizer` package."""

from click.testing import CliRunner

from organizer import __version__, cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    version_result = runner.invoke(cli.main, ["--version"])
    assert version_result.exit_code == 0
    assert version_result.stdout.strip() == __version__

    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Organize your TV Shows." in help_result.stdout
