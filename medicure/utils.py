import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import tmdbsimple as tmdb


def extract_episode_number(file_name: Path) -> int:
    """
    Extracts episode number from file name
    """
    match = re.search(r'(?<=[eE])\d{2}', str(file_name))
    if match is not None:
        episode_number = int(match.group())
        return episode_number

    raise ValueError('File name did not match with episode number pattern.')


def get_movie_name(
    tmdb_find_info: Optional[Dict[str, Any]] = None,
    imdb_id: Optional[str] = None,
) -> str:
    """
    Gets correct movie name
    """
    tmdb_find_info = _validate_tmdb_info(tmdb_find_info, imdb_id)
    movie = tmdb_find_info['movie_results'][0]
    title = _escape_nonpath_characters(movie['title'])
    release_year = movie['release_date'][:4]
    return f'{title} - {release_year}'


def get_tvshow_info(
    season_number: int,
    tmdb_find_info: Optional[Dict[str, Any]] = None,
    imdb_id: Optional[str] = None,
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Gets correct TV show info
    """
    tmdb_find_info = _validate_tmdb_info(tmdb_find_info, imdb_id)
    tvshow = tmdb_find_info['tv_results'][0]
    name = _escape_nonpath_characters(tvshow['name'])
    season = tmdb.TV_Seasons(tvshow['id'], season_number).info()
    season_name = _escape_nonpath_characters(season['name'])
    for episode in season['episodes']:
        episode['name'] = _escape_nonpath_characters(episode['name'])

    return name, season_name, season


def _validate_tmdb_info(
    tmdb_find_info: Optional[Dict[str, Any]],
    imdb_id: Optional[str],
) -> Dict[str, Any]:
    assert (
        tmdb_find_info is not None or imdb_id is not None
    ), 'Both `tmdb_find_info` and `imdb_id` cannot ne `None`.'

    if tmdb_find_info is None:
        tmdb_find_info = tmdb.Find(imdb_id).info(external_source='imdb_id')

    return tmdb_find_info


def _escape_nonpath_characters(string: str) -> str:
    return string.translate(str.maketrans(':/', '  '))
