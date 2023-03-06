from typing import List, Optional

import rich_click.typer as typer

from medicure.cli.base import app
from medicure.cli.types import DataList, StringList
from medicure.cli.utils import (
    create_error_message,
    create_helps_from,
    load_collection_info,
    load_tmdb_info,
)
from medicure.core import Medicure
from medicure.data_structures import DubbingSupplier

treat_app = typer.Typer()
app.add_typer(treat_app, name='treat')


@treat_app.command('media')
@create_helps_from(Medicure.treat_media)
def treat_media(
    imdb_id: str = typer.Argument(...),
    file_search_patterns: List[str] = typer.Argument(
        ...,
        param_type=StringList,
        help=', you can pass a json like string for this argument.',
    ),
    video_language_code: str = typer.Argument(...),
    video_source: str = typer.Argument(...),
    video_release_format: str = typer.Argument(...),
    dubbing_suppliers: List[DubbingSupplier] = typer.Argument(
        ...,
        param_type=DataList(DubbingSupplier),
        help=(
            ', you can pass a json like string containing either list of value'
            ' lists or list of dicts of keyword arguments for this argument.'
        ),
    ),
    season_number: Optional[int] = typer.Argument(None),
) -> None:
    """
    Fixes video source, audio source, file name and language for
    all tracks.
    """
    medicure = Medicure(load_tmdb_info()['api_key'], **load_collection_info())
    try:
        medicure.treat_media(
            imdb_id,
            file_search_patterns,
            video_language_code,
            video_source,
            video_release_format,
            dubbing_suppliers,
            season_number,
        )
    except Exception as e:
        typer.secho(
            f'Error: {create_error_message(str(e))}', err=True, fg='red'
        )
        raise typer.Exit(code=1)


@treat_app.command('subtitle')
@create_helps_from(Medicure.treat_subtitle)
def treat_subtitle(
    imdb_id: str = typer.Argument(...),
    file_search_patterns: List[str] = typer.Argument(
        ..., param_type=StringList
    ),
    language_code: str = typer.Argument(...),
    source: Optional[str] = typer.Argument(None),
    release_format: Optional[str] = typer.Argument(None),
    include_full_information: bool = typer.Option(
        False,
        '-i',
        '--include-full-information',
    ),
    season_number: Optional[int] = typer.Argument(None),
) -> None:
    """
    Fixes subtitle source, file name and language.
    """
    medicure = Medicure(load_tmdb_info()['api_key'], **load_collection_info())
    try:
        medicure.treat_subtitle(
            imdb_id,
            file_search_patterns,
            language_code,
            source,
            release_format,
            include_full_information,
            season_number,
        )
    except Exception as e:
        typer.secho(
            f'Error: {create_error_message(str(e))}', err=True, fg='red'
        )
        raise typer.Exit(code=1)
