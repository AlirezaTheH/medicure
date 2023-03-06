from typing import Optional

import rich_click.typer as typer

from medicure.version import __version__

typer.rich_click.SHOW_ARGUMENTS = True
typer.rich_click.USE_MARKDOWN = True
typer.rich_click.GROUP_ARGUMENTS_OPTIONS = False

app = typer.Typer(
    name='medicure',
    help='Medicure\'s Command-line Interface',
    no_args_is_help=True,
    context_settings=dict(help_option_names=['-h', '--help']),
)


@app.callback(invoke_without_command=True)
def version_callback(
    version: Optional[bool] = typer.Option(
        None, '-v', '--version', is_eager=True, help='Show medicure version.'
    )
) -> None:
    """
    Adds --version option to cli.
    """
    if version:
        typer.echo(__version__)
        raise typer.Exit()
