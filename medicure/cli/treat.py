from typing import Dict, List, Optional

import tmdbsimple as tmdb
import typer

from medicure.cli.base import app
from medicure.cli.utils import load_collection_info, load_tmdb_info
from medicure.data_structures import DubbingSupplier
from medicure.media import Medicure
from medicure.subtitle import Subcure

treat_app = typer.Typer()
app.add_typer(treat_app, name='treat')
tmdb.API_KEY = load_tmdb_info()['api_key']


@treat_app.command('media')
def treat_media(
    imdb_id: str,
    file_search_pattern_to_id: Dict[str, int],
    video_language_code: str,
    video_source: str,
    video_release_format: str,
    dubbing_suppliers: List[DubbingSupplier],
    season_number: Optional[int] = None,
) -> None:
    """
    Fixes video source, audio source, file name and language for
    all tracks.

    Parameters
    ----------
    imdb_id: str
        IMDB id

    file_search_pattern_to_id: dict[str, int]
        Dict of patterns for finding files to file ids

    video_language_code: str
        3-letter language code for video track
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    video_source: str
        Source of the video file; name of encoder or the website
        which video is downloaded from

    video_release_format: str
        Format of the video file eg: Blu-ray, WEBRip, ...
        See https://en.wikipedia.org/wiki/Pirated_movie_release_types
        for available formats.

    dubbing_suppliers: list[DubbingSupplier]
        List of possible dubbing suppliers

    season_number: int, optional
        If imdb_id is a tv show, season number should be given.
    """
    medicure = Medicure(**load_collection_info())
    medicure.treat(
        imdb_id,
        file_search_pattern_to_id,
        video_language_code,
        video_source,
        video_release_format,
        dubbing_suppliers,
        season_number,
    )


@treat_app.command('subtitle')
def treat_subtitle(
    imdb_id: str,
    file_search_pattern: str,
    language_code: str,
    source: Optional[str] = None,
    release_format: Optional[str] = None,
    include_full_information: bool = False,
    season_number: Optional[int] = None,
) -> None:
    """
    Fixes subtitle source, file name and language.

    Parameters
    ----------
    imdb_id: str
        IMDB id

    file_search_pattern: str
        Pattern for finding files

    language_code: str
        3-letter language code for subtitle
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    source: str, optional
        Source of the subtitle file: name of author or the website
        which subtitle is downloaded from. This should be given only
        when `include_full_information` is `True`.

    release_format: str, optional
        Format of the video that the subtitle is sync with eg:
        Blu-ray, WEBRip, ...
        See https://en.wikipedia.org/wiki/Pirated_movie_release_types
        for available formats. This should be given only
        when `include_full_information` is `True`.

    include_full_information: bool
        If set to `True` the subtitle will be converted to mks
        format inorder to save all subtitle information. If set to
        `True`, `subtitle_source` and `subtitle_release_format`
        should also be given.

    season_number: int, optional
        If imdb_id is a tv show season number should be given.
    """
    subcure = Subcure(**load_collection_info())
    subcure.treat(
        imdb_id,
        file_search_pattern,
        language_code,
        source,
        release_format,
        include_full_information,
        season_number,
    )
