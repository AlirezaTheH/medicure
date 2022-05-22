from importlib import reload
from inspect import getsourcefile

import typer


def patched() -> bool:
    """
    If Typer is patched by medicure
    """
    return getattr(typer, 'patched_by_medicure', False)


def patch_param_type() -> None:
    """
    Patches Typer with Click's ParamTypes.
    """
    # Patch typer.models and typer.params
    mp_patches = [
        {
            'after': 'autocompletion: Optional[Callable[..., Any]] = None,',
            'insert': 'param_type: Optional[click.ParamType] = None,',
        },
        {
            'after': 'self.autocompletion = autocompletion',
            'insert': 'self.param_type = param_type',
        },
        {
            'after': 'autocompletion=autocompletion,',
            'insert': 'param_type=param_type,',
        },
    ]
    for module in ('models', 'params'):
        module_source_path = getsourcefile(getattr(typer, module))
        with open(module_source_path) as f:
            module_source = ''
            for line in f:
                module_source += line
                for patch in mp_patches:
                    if patch['after'] in line:
                        line_indent = line[: line.index(patch['after'])]
                        module_source += f'{line_indent}{patch["insert"]}\n'
                        break

        with open(module_source_path, 'w') as f:
            f.write(module_source)

        reload(getattr(typer, module))

    # Patch typer.main
    main_patch = {
        'replace': 'if origin is not None:',
        'with': (
            '\tif parameter_info.param_type:\n'
            '\t\tparameter_type = parameter_info.param_type\n'
            '\tif parameter_type is None and origin is not None:\n'
        ),
    }
    main_source_path = getsourcefile(typer.main)
    with open(main_source_path) as f:
        main_source = ''
        for line in f:
            if main_patch['replace'] in line:
                main_source += main_patch['with'].replace('\t', ' ' * 4)
            else:
                main_source += line

    with open(main_source_path, 'w') as f:
        f.write(main_source)

    reload(typer.main)

    # Mark typer as patched
    init_source_path = getsourcefile(typer)
    with open(init_source_path) as f:
        init_source = f.read()
        init_source += '\npatched_by_medicure = True\n'

    with open(init_source_path, 'w') as f:
        f.write(init_source)

    reload(typer)
