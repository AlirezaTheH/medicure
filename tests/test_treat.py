from typing import Any, List, Tuple

import pytest

from medicure.core import Medicure
from tests.parameterize import *
from tests.utils import (
    validate_movie_media_file,
    validate_movie_subtitle_file,
    validate_tvshow_media_files,
    validate_tvshow_subtitle_files,
)


@pytest.mark.parametrize(*treat_media_args)
def test_treat_movie_media(
    file_search_patterns: List[str],
    dubbing_suppliers: List[DubbingSupplier],
    correct_tracks: List[Track],
) -> None:
    medicure = Medicure(tmdb_api_key, movies_directory)
    medicure.treat_media(
        movie_imdb_id,
        file_search_patterns,
        video_language_code,
        video_source,
        video_release_format,
        dubbing_suppliers,
    )
    validate_movie_media_file(movie_imdb_id, correct_tracks, movies_directory)


@pytest.mark.parametrize(*season_info_args)
@pytest.mark.parametrize(*treat_media_args)
def test_treat_tvshow_media(
    season_number: int,
    available_episode_count: int,
    file_search_patterns: List[str],
    dubbing_suppliers: List[DubbingSupplier],
    correct_tracks: List[Track],
) -> None:
    medicure = Medicure(tmdb_api_key, tvshows_directory=tvshows_directory)
    medicure.treat_media(
        tvshow_imdb_id,
        file_search_patterns,
        video_language_code,
        video_source,
        video_release_format,
        dubbing_suppliers,
        season_number,
    )
    validate_tvshow_media_files(
        tvshow_imdb_id,
        season_number,
        available_episode_count,
        correct_tracks,
        tvshows_directory,
    )


@pytest.mark.parametrize(*treat_subtitle_args)
def test_treat_movie_subtitle(
    include_full_information: bool,
    suffix: str,
):
    medicure = Medicure(tmdb_api_key, movies_directory)
    medicure.treat_subtitle(
        movie_imdb_id,
        subtitle_file_search_patterns,
        subtitle_language_code,
        subtitle_source,
        subtitle_release_format,
        include_full_information,
    )
    validate_movie_subtitle_file(
        movie_imdb_id,
        subtitle_language_code,
        suffix,
        include_full_information,
        subtitle_correct_track,
        movies_directory,
    )


@pytest.mark.parametrize(*season_info_args)
@pytest.mark.parametrize(*treat_subtitle_args)
def test_treat_tvshow_subtitle(
    season_number: int,
    available_episode_count: int,
    include_full_information: bool,
    suffix: str,
):
    medicure = Medicure(tmdb_api_key, tvshows_directory=tvshows_directory)
    medicure.treat_subtitle(
        tvshow_imdb_id,
        subtitle_file_search_patterns,
        subtitle_language_code,
        subtitle_source,
        subtitle_release_format,
        include_full_information,
        season_number,
    )
    validate_tvshow_subtitle_files(
        tvshow_imdb_id,
        season_number,
        available_episode_count,
        subtitle_language_code,
        suffix,
        include_full_information,
        subtitle_correct_track,
        tvshows_directory,
    )


@pytest.mark.parametrize(
    'imdb_id, match_format_args',
    [
        (movie_imdb_id, ('Movie', 'movie')),
        (tvshow_imdb_id, ('TV show', 'TV show')),
    ],
)
@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ([],)), ('subtitle', ())]
)
def test_treat_with_no_collection_info(
    imdb_id: str,
    match_format_args: Tuple[str, str],
    treat_kind: str,
    extra_treat_args: Tuple[Any, ...],
) -> None:
    medicure = Medicure(tmdb_api_key)
    with pytest.raises(
        AssertionError,
        match='{0}s directory has been not given for a {1}.'.format(
            *match_format_args
        ),
    ):
        getattr(medicure, f'treat_{treat_kind}')(
            imdb_id, [], '', '', '', *extra_treat_args
        )


@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ([],)), ('subtitle', ())]
)
def test_treat_tvshow_with_no_season_number(
    treat_kind: str,
    extra_treat_args: Tuple[Any, ...],
) -> None:
    medicure = Medicure(tmdb_api_key, tvshows_directory=tvshows_directory)
    with pytest.raises(
        AssertionError,
        match='`season_number` has not been given for a TV show.',
    ):
        getattr(medicure, f'treat_{treat_kind}')(
            tvshow_imdb_id, [], '', '', '', *extra_treat_args
        )


@pytest.mark.parametrize('imdb_id', [movie_imdb_id, tvshow_imdb_id])
def test_treat_subtitle_with_include_full_information_and_no_information(
    imdb_id: str,
) -> None:
    medicure = Medicure(tmdb_api_key, movies_directory, tvshows_directory)
    with pytest.raises(
        AssertionError,
        match=(
            'When `include_full_information` is `True`, '
            '`source` and `release_format` should be given.'
        ),
    ):
        medicure.treat_subtitle(imdb_id, [], '', None, None, True)


@pytest.mark.parametrize(
    'imdb_id, extra_treat_args', [(movie_imdb_id, ()), (tvshow_imdb_id, (5,))]
)
def test_treat_sub_file_with_include_full_information(
    imdb_id: str,
    extra_treat_args: Tuple[Any, ...],
) -> None:
    medicure = Medicure(tmdb_api_key, movies_directory, tvshows_directory)
    with pytest.raises(
        AssertionError,
        match='Files with .sub suffix does not contain any information.',
    ):
        medicure.treat_subtitle(
            imdb_id, {r'\.sub': 0}, '', '', '', True, *extra_treat_args
        )


@pytest.mark.parametrize(
    'treat_kind, file_search_patterns, extra_treat_args',
    [
        ('media', media_file_search_patterns, ([],)),
        ('subtitle', subtitle_file_search_patterns, (False,)),
    ],
)
def test_treat_tvshow_with_invalid_file_names(
    treat_kind: str,
    file_search_patterns: List[str],
    extra_treat_args: Tuple[Any, ...],
) -> None:
    medicure = Medicure(tmdb_api_key, tvshows_directory=tvshows_directory)
    with pytest.raises(
        ValueError,
        match='File name did not match with episode number pattern.',
    ):
        getattr(medicure, f'treat_{treat_kind}')(
            tvshow_imdb_id,
            file_search_patterns,
            '',
            '',
            '',
            *extra_treat_args,
            4,
        )
