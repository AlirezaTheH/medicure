import json
from pathlib import Path
from typing import Optional

import typer

from medicure.cli.base import app
from medicure.cli.utils import create_param_help, get_base_path

save_app = typer.Typer()
app.add_typer(save_app, name='save')


@save_app.command('tmdb-info')
def save_tmdb_info(
    api_key: str = typer.Argument(
        ..., help=create_param_help(': str', 'The TMDB API key')
    ),
) -> None:
    """
    Saves TMDB info on disk.
    """
    info_path = get_base_path() / 'tmdb_info.json'
    info = {
        'api_key': api_key,
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4, sort_keys=True, ensure_ascii=False)

    typer.secho('Your TMDB info has been saved successfully.', fg='green')


@save_app.command('collection-info')
def save_collection_info(
    movies_directory: Optional[Path] = typer.Option(
        None,
        '-md',
        '--movies-directory',
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        allow_dash=True,
        help=create_param_help(
            'Directory of your movies, must be given if',
            '`--tvshows-directory` has been not given.',
            internal=True,
            option=True,
        ),
    ),
    tvshows_directory: Optional[Path] = typer.Option(
        None,
        '-td',
        '--tvshows-directory',
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        allow_dash=True,
        help=create_param_help(
            'Directory of your TV shows, must be given if',
            '`--movies-directory` has been not given.',
            internal=True,
            option=True,
        ),
    ),
) -> None:
    """
    Saves collection info on disk.
    """
    if movies_directory is None and tvshows_directory is None:
        typer.secho(
            'Error: At least one of the `--movies-directory` '
            'and `--tvshows-directory` should be given.',
            err=True,
            fg='red',
        )
        raise typer.Exit(code=1)

    info_path = get_base_path() / 'collection_info.json'
    info = {
        'movies_directory': str(movies_directory),
        'tvshows_directory': str(tvshows_directory),
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4, sort_keys=True, ensure_ascii=False)

    typer.secho(
        'Your collection info has been saved successfully.', fg='green'
    )
