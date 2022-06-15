import subprocess
import sys

import pytest

from medicure.typer_patch.core import get_typer_path, patch_param_type


@pytest.fixture(autouse=True)
def reinstall_typer() -> None:
    subprocess.run(
        f'{sys.executable} -m pip install --ignore-installed typer', shell=True
    )


def test_patch_param_type() -> None:
    patch_param_type()
    with open(get_typer_path() / '__init__.py') as f:
        assert '_patched_by_medicure = True' in f.read()
