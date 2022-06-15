from typing import Dict, List, Optional

import typer

from medicure.cli.base import app
from medicure.cli.types import DataList, Json
from medicure.cli.utils import (
    create_error_message,
    create_param_help,
    create_sub_param_help,
    load_collection_info,
    load_tmdb_info,
)
from medicure.core import Medicure
from medicure.data_structures import DubbingSupplier

treat_app = typer.Typer()
app.add_typer(treat_app, name='treat')


@treat_app.command('media')
def treat_media(
    imdb_id: str = typer.Argument(
        ..., help=create_param_help(': str', 'IMDB id')
    ),
    file_search_pattern_to_id: Dict[str, int] = typer.Argument(
        ...,
        param_type=Json,
        help=create_param_help(
            ': dict[str, int]',
            'Dict of patterns for finding files to file ids',
            'You can pass a json like string for this argument.',
        ),
    ),
    video_language_code: str = typer.Argument(
        ...,
        help=create_param_help(
            ': str',
            '3-letter language code for video track',
            'See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes',
            'for available langauge codes.',
        ),
    ),
    video_source: str = typer.Argument(
        ...,
        help=create_param_help(
            ': str',
            'Source of the video file; name of encoder or the website',
            'which video is downloaded from',
        ),
    ),
    video_release_format: str = typer.Argument(
        ...,
        help=create_param_help(
            ': str',
            'Format of the video file eg: Blu-ray, WEBRip, ...',
            'See https://en.wikipedia.org/wiki/Pirated_movie_release_types',
            'for available formats.',
        ),
    ),
    dubbing_suppliers: List[DubbingSupplier] = typer.Argument(
        ...,
        param_type=DataList(DubbingSupplier),
        help=create_param_help(
            ': list[DubbingSupplier]',
            'List of possible dubbing suppliers ',
            '`DubbingSupplier` is a dataclass which has the following',
            'attributes:',
            create_sub_param_help(
                'name: str',
                'Name of dubbing supplier, if dubbing supplier represents',
                "original audio of movie or TV show this doesn't matter but",
                "should set to `'original'` for better convenience.",
            ),
            create_sub_param_help(
                'file_id: str',
                'The file id which include dubbing supplier tracks',
            ),
            create_sub_param_help(
                'correct_language_code: str',
                'Correct 3-letter language code for dubbing supplier',
            ),
            create_sub_param_help(
                'audio_language_code: str',
                'Current 3-letter language code for audio track',
            ),
            create_sub_param_help(
                'subtitle_language_code: str',
                'Current 3-letter language code for subtitle track',
            ),
            create_sub_param_help(
                'audio_search_pattern: str, optional',
                'The search pattern for finding audio track',
            ),
            create_sub_param_help(
                'subtitle_search_pattern: str, optional',
                'The search pattern for finding subtitle track',
            ),
            create_param_help(
                'You can pass a json like string containing either',
                'list of value lists or list of dict of keyword arguments',
                'for this argument.',
                internal=True,
            ),
        ),
    ),
    season_number: Optional[int] = typer.Argument(
        None,
        help=create_param_help(
            ': int',
            'If `IMDB_ID` is a TV show, season number should be given.',
        ),
    ),
) -> None:
    """
    Fixes video source, audio source, file name and language for
    all tracks.
    """
    medicure = Medicure(load_tmdb_info()['api_key'], **load_collection_info())
    try:
        medicure.treat_media(
            imdb_id,
            file_search_pattern_to_id,
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
def treat_subtitle(
    imdb_id: str = typer.Argument(
        ..., help=create_param_help(': str', 'IMDB id')
    ),
    file_search_pattern_to_id: Dict[str, int] = typer.Argument(
        ...,
        param_type=Json,
        help=create_param_help(
            ': dict[str, int]',
            'Dict of patterns for finding files to file ids',
            'You can pass a json like string for this argument.',
        ),
    ),
    language_code: str = typer.Argument(
        ...,
        help=create_param_help(
            ': str',
            '3-letter language code for subtitle',
            'See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes',
            'for available langauge codes.',
        ),
    ),
    source: Optional[str] = typer.Argument(
        None,
        help=create_param_help(
            ': str',
            'Source of the subtitle file: name of author or the website',
            'which subtitle is downloaded from. This should be given only',
            'when `--include-full-information` flag is set.',
        ),
    ),
    release_format: Optional[str] = typer.Argument(
        None,
        help=create_param_help(
            ': str',
            'Format of the video that the subtitle is sync with eg:',
            'Blu-ray, WEBRip, ...',
            'See https://en.wikipedia.org/wiki/Pirated_movie_release_types',
            'for available formats. This should be given only',
            'when `--include-full-information` flag is set.',
        ),
    ),
    include_full_information: bool = typer.Option(
        False,
        '-ifi',
        '--include-full-information',
        help=create_param_help(
            'If this flag is set, the subtitle will be converted to mks',
            'format inorder to save all subtitle information. If set,',
            '`SOURCE` and `RELEASE_FORMAT` should also be given.',
            internal=True,
            option=True,
        ),
    ),
    season_number: Optional[int] = typer.Argument(
        None,
        help=create_param_help(
            ': int',
            'If `IMDB_ID` is a TV show, season number should be given.',
        ),
    ),
) -> None:
    """
    Fixes subtitle source, file name and language.
    """
    medicure = Medicure(load_tmdb_info()['api_key'], **load_collection_info())
    try:
        medicure.treat_subtitle(
            imdb_id,
            file_search_pattern_to_id,
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
