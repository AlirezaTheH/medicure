import json
from typing import Any, List, Tuple

import pytest
from typer.testing import CliRunner
from varname import nameof

from medicure.cli.base import app
from tests.cli.utils import get_flag_args
from tests.parameterize import *
from tests.utils import (
    validate_movie_media_file,
    validate_movie_subtitle_file,
    validate_tvshow_media_files,
    validate_tvshow_subtitle_files,
)


@pytest.fixture(autouse=True)
def save_all_info(
    request: pytest.FixtureRequest, cli_runner: CliRunner
) -> None:
    if 'save_no_tmdb_info' not in request.keywords:
        cli_runner.invoke(app, ('save', 'tmdb-info', tmdb_api_key))

    if 'save_no_collection_info' not in request.keywords:
        cli_runner.invoke(
            app,
            (
                'save',
                'collection-info',
                '--movies-directory',
                str(movies_directory),
                '--tvshows-directory',
                str(tvshows_directory),
            ),
        )


@pytest.mark.parametrize(*treat_media_args)
@pytest.mark.parametrize('ds_json_kind', ['list', 'dict'])
def test_treat_movie_media(
    file_search_patterns: List[str],
    dubbing_suppliers: List[DubbingSupplier],
    ds_json_kind: str,
    correct_tracks: List[Track],
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            'media',
            movie_imdb_id,
            json.dumps(file_search_patterns),
            video_language_code,
            video_source,
            video_release_format,
            json.dumps(
                [
                    getattr(ds, f'to_{ds_json_kind}')()
                    for ds in dubbing_suppliers
                ]
            ),
        ),
    )
    assert result.exit_code == 0
    validate_movie_media_file(movie_imdb_id, correct_tracks, movies_directory)


@pytest.mark.parametrize(*season_info_args)
@pytest.mark.parametrize(*treat_media_args)
@pytest.mark.parametrize('ds_json_kind', ['list'])
def test_treat_tvshow_media(
    season_number: int,
    available_episode_count: int,
    file_search_patterns: List[str],
    dubbing_suppliers: List[DubbingSupplier],
    ds_json_kind: str,
    correct_tracks: List[Track],
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            'media',
            tvshow_imdb_id,
            json.dumps(file_search_patterns),
            video_language_code,
            video_source,
            video_release_format,
            json.dumps(
                [
                    getattr(ds, f'to_{ds_json_kind}')()
                    for ds in dubbing_suppliers
                ]
            ),
            str(season_number),
        ),
    )
    assert result.exit_code == 0
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
    cli_runner: CliRunner,
):
    result = cli_runner.invoke(
        app,
        (
            'treat',
            'subtitle',
            movie_imdb_id,
            json.dumps(subtitle_file_search_patterns),
            subtitle_language_code,
            subtitle_source,
            subtitle_release_format,
            *get_flag_args(
                include_full_information, nameof(include_full_information)
            ),
        ),
    )
    assert result.exit_code == 0
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
    cli_runner: CliRunner,
):
    result = cli_runner.invoke(
        app,
        (
            'treat',
            'subtitle',
            tvshow_imdb_id,
            json.dumps(subtitle_file_search_patterns),
            subtitle_language_code,
            subtitle_source,
            subtitle_release_format,
            str(season_number),
            *get_flag_args(
                include_full_information, nameof(include_full_information)
            ),
        ),
    )
    assert result.exit_code == 0
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


@pytest.mark.save_no_tmdb_info
@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ('[]',)), ('subtitle', ())]
)
def test_treat_before_save_tmdb_info(
    cli_runner: CliRunner, treat_kind: str, extra_treat_args: Tuple[Any, ...]
) -> None:
    result = cli_runner.invoke(
        app, ('treat', treat_kind, '', '[]', '', '', '', *extra_treat_args)
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert 'Error: No TMDB info found.' in result.output


@pytest.mark.save_no_collection_info
@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ('[]',)), ('subtitle', ())]
)
def test_treat_before_save_collection_info(
    cli_runner: CliRunner, treat_kind: str, extra_treat_args: Tuple[Any, ...]
) -> None:
    result = cli_runner.invoke(
        app, ('treat', treat_kind, '', '[]', '', '', '', *extra_treat_args)
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert 'Error: No collection info found.' in result.output


@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ('[]',)), ('subtitle', ())]
)
def test_treat_tvshow_with_no_season_number(
    treat_kind: str,
    extra_treat_args: Tuple[Any, ...],
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            treat_kind,
            tvshow_imdb_id,
            '[]',
            '',
            '',
            '',
            *extra_treat_args,
        ),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert (
        'Error: `SEASON_NUMBER` has not been given for a TV show.'
        in result.output
    )


@pytest.mark.parametrize('imdb_id', [movie_imdb_id, tvshow_imdb_id])
def test_treat_subtitle_with_include_full_information_and_no_information(
    imdb_id: str, cli_runner: CliRunner
) -> None:
    result = cli_runner.invoke(
        app,
        ('treat', 'subtitle', imdb_id, '[]', '', '--include-full-information'),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert (
        'When `--include-full-information` flag is set, '
        '`SOURCE` and `RELEASE_FORMAT` should be given.'
    ) in result.output


@pytest.mark.parametrize(
    'imdb_id, extra_treat_args',
    [(movie_imdb_id, ()), (tvshow_imdb_id, ('5',))],
)
def test_treat_sub_file_with_include_full_information(
    imdb_id: str, extra_treat_args: Tuple[Any, ...], cli_runner: CliRunner
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            'subtitle',
            imdb_id,
            str(([r'\.sub'])),
            '',
            '',
            '',
            *extra_treat_args,
            '--include-full-information',
        ),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert (
        'Error: Files with .sub suffix does not contain any information.'
        in result.output
    )


@pytest.mark.parametrize(
    'treat_kind, file_search_patterns, extra_treat_args',
    [
        ('media', media_file_search_patterns, ('[]',)),
        ('subtitle', subtitle_file_search_patterns, ()),
    ],
)
def test_treat_tvshow_with_invalid_file_names(
    treat_kind: str,
    file_search_patterns: List[str],
    extra_treat_args: Tuple[Any, ...],
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            treat_kind,
            tvshow_imdb_id,
            json.dumps(file_search_patterns),
            '',
            '',
            '',
            *extra_treat_args,
            '4',
        ),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert (
        'Error: File name did not match with episode number pattern.'
        in result.output
    )


@pytest.mark.parametrize(
    'treat_kind, extra_treat_args', [('media', ('[]',)), ('subtitle', ())]
)
@pytest.mark.parametrize(
    'file_search_patterns, output',
    [
        (
            '{}',
            'Error: Bad JSON value for `FILE_SEARCH_PATTERNS`. '
            "`'{}'` is not a JSON list.",
        ),
        (
            '',
            'Error: Bad JSON value for `FILE_SEARCH_PATTERNS`. '
            'Expecting value:',
        ),
    ],
)
def test_treat_with_invalid_file_search_patterns(
    treat_kind: str,
    extra_treat_args: Tuple[Any, ...],
    file_search_patterns: str,
    output: str,
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        (
            'treat',
            treat_kind,
            '',
            file_search_patterns,
            '',
            '',
            '',
            *extra_treat_args,
        ),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert output in result.output


@pytest.mark.parametrize(
    'dubbing_suppliers, output',
    [
        (
            '{}',
            'Error: Bad JSON value for `DUBBING_SUPPLIERS`. '
            "`'{}'` is not a JSON list.",
        ),
        (
            '',
            'Error: Bad JSON value for `DUBBING_SUPPLIERS`. Expecting value:',
        ),
    ],
)
def test_treat_media_with_invalid_dubbing_suppliers(
    dubbing_suppliers: str, output: str, cli_runner: CliRunner
) -> None:
    result = cli_runner.invoke(
        app,
        ('treat', 'media', '', '[]', '', '', '', dubbing_suppliers),
    )
    # rich-click affects the exit codes
    assert result.exit_code == 0
    assert output in result.output
