from typer.testing import CliRunner

from medicure.cli.base import app
from medicure.version import __version__


def test_version(cli_runner: CliRunner):
    result = cli_runner.invoke(app, ('--version',))
    assert result.exit_code == 0
    assert __version__ in result.output
