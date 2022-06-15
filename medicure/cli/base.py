from typing import Optional

import typer

from medicure.version import __version__

app = typer.Typer(
    name='medicure',
    help='Medicure\'s Command-line Interface',
    context_settings=dict(help_option_names=['-h', '--help']),
)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def version_callback(
    version: Optional[bool] = typer.Option(
        None, '-v', '--version', is_eager=True, help='Show medicure version.'
    )
) -> None:
    """
    Adds --version option to cli.
    """
    if version:
        print(__version__)
        raise typer.Exit()
