import site
from pathlib import Path

import patch


def patch_param_type() -> None:
    typer_path = Path(site.getsitepackages()[0]) / 'typer'
    with open(typer_path / '__init__.py') as f:
        if '_patched_by_medicure = True' in f.read():
            return
    p = patch.fromfile(Path(__file__).parent / 'param_type.patch')
    p.apply(root=typer_path)
