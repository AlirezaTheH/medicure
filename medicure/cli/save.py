import json
from os import path

import typer

from medicure.cli.base import app
from medicure.cli.utils import get_base_path

save_app = typer.Typer()
app.add_typer(save_app, name='save')


@save_app.command('tmdb-info')
def save_tmdb_info(api_key: str) -> None:
    """
    Saves TMDB info on disk.

    Parameters
    ----------
    api_key: str
        The TMDB api key
    """
    info_path = path.join(get_base_path(), 'tmdb_info.json')
    info = {
        'api_key': api_key,
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4, sort_keys=True, ensure_ascii=False)


@save_app.command('collection-info')
def save_collection_info(
    movies_directory: str,
    tvshows_directory: str,
) -> None:
    """
    Saves collection info on disk.

    tvshows_directory: str
        Directory of your tv shows

    movies_directory: str
        Directory of your movies
    """
    if not path.isdir(movies_directory):
        raise NotADirectoryError(f'{movies_directory} is not a directory.')
    if not path.isdir(tvshows_directory):
        raise NotADirectoryError(f'{tvshows_directory} is not a directory.')

    info_path = path.join(get_base_path(), 'collection_info.json')
    info = {
        'movies_directory': movies_directory,
        'tvshows_directory': tvshows_directory,
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4, sort_keys=True, ensure_ascii=False)
