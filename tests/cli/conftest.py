import shutil

import pytest
from typer.testing import CliRunner

from medicure.cli.utils import get_base_path


@pytest.fixture(scope='session', autouse=True)
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True)
def clear_base_path() -> None:
    yield

    base_path = get_base_path()
    if base_path.exists():
        shutil.rmtree(base_path)
