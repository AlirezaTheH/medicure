import site
from pathlib import Path

import patch


def get_typer_path() -> Path:
    """
    Gets correct Typer path for all platforms.

    Returns
    -------
    path: Path
        The Typer path
    """
    for path in site.getsitepackages():
        if path.endswith('site-packages'):
            return Path(path) / 'typer'


def patch_param_type() -> None:
    """
    Patches Typer with Click's ParamTypes.
    """

    typer_path = get_typer_path()
    with open(typer_path / '__init__.py') as f:
        if '_patched_by_medicure = True' in f.read():
            return
    p = patch.fromfile(Path(__file__).parent / 'param_type.patch')
    p.apply(root=typer_path)
