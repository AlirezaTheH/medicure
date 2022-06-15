from typer.testing import CliRunner

from medicure.cli.base import app
from medicure.cli.utils import load_collection_info, load_tmdb_info
from tests.parameterize import *


def test_save_tmdb_info(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ('save', 'tmdb-info', tmdb_api_key))
    assert result.exit_code == 0
    assert 'Your TMDB info has been saved successfully.' in result.output
    tmdb_info = load_tmdb_info()
    assert tmdb_info['api_key'] == tmdb_api_key


def test_save_collection_info(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
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
    assert result.exit_code == 0
    assert 'Your collection info has been saved successfully.' in result.output
    collection_info = load_collection_info()
    assert collection_info['movies_directory'] == movies_directory
    assert collection_info['tvshows_directory'] == tvshows_directory


def test_save_collection_info_with_no_options(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ('save', 'collection-info'))
    assert result.exit_code == 1
    assert (
        'Error: At least one of the `--movies-directory` '
        'and `--tvshows-directory` should be given.'
    ) in result.output
