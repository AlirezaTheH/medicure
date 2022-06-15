from dataclasses import fields
from pathlib import Path
from typing import List

from pymediainfo import MediaInfo

from medicure.utils import get_movie_name, get_tvshow_info
from tests.data_structures import Track


def _validate_destination_directory(source_directory: Path) -> Path:
    destination_directory = Path(f'{source_directory} Edited')
    assert destination_directory.exists()
    return destination_directory


def validate_movie_media_file(
    imdb_id: str,
    correct_tracks: List[Track],
    movies_directory: Path,
) -> None:
    movie_name = get_movie_name(imdb_id=imdb_id)
    destination_directory = _validate_destination_directory(
        movies_directory / movie_name
    )
    treated_movie_file_path = destination_directory / f'{movie_name}.mkv'
    assert treated_movie_file_path.exists()

    media_info = MediaInfo.parse(treated_movie_file_path)
    for i, track in enumerate(media_info.tracks[1:]):
        correct_track = correct_tracks[i]
        for field in fields(correct_track):
            a = getattr(track, field.name)
            b = getattr(correct_track, field.name)
            assert getattr(track, field.name) == getattr(
                correct_track, field.name
            )


def validate_tvshow_media_files(
    imdb_id: str,
    season_number: int,
    available_episode_count: int,
    correct_tracks: List[Track],
    tvshows_directory: Path,
) -> None:
    name, season_name, season = get_tvshow_info(season_number, imdb_id=imdb_id)
    destination_directory = _validate_destination_directory(
        tvshows_directory / name / season_name
    )
    for episode in season['episodes'][:available_episode_count]:
        ename = episode['name']
        enumber = episode['episode_number']

        treated_episode_file_path = destination_directory.joinpath(
            f'{name} - S{season_number:02d}E{enumber:02d} - {ename}.mkv',
        )
        assert treated_episode_file_path.exists()

        media_info = MediaInfo.parse(treated_episode_file_path)
        for i, track in enumerate(media_info.tracks[1:]):
            correct_track = correct_tracks[i]
            for field in fields(correct_track):
                assert getattr(track, field.name) == getattr(
                    correct_track, field.name
                )


def validate_movie_subtitle_file(
    imdb_id: str,
    language_code: str,
    suffix: str,
    include_full_information: bool,
    correct_track: Track,
    movies_directory: Path,
) -> None:
    movie_name = get_movie_name(imdb_id=imdb_id)
    destination_directory = _validate_destination_directory(
        movies_directory / movie_name
    )
    treated_movie_subtitle_file_path = destination_directory.joinpath(
        f'{movie_name}.{language_code}{suffix}'
    )
    assert treated_movie_subtitle_file_path.exists()
    if include_full_information:
        media_info = MediaInfo.parse(treated_movie_subtitle_file_path)
        for field in fields(correct_track):
            assert getattr(media_info.text_tracks[0], field.name) == getattr(
                correct_track, field.name
            )


def validate_tvshow_subtitle_files(
    imdb_id: str,
    season_number: int,
    available_episode_count: int,
    language_code: str,
    suffix: str,
    include_full_information: bool,
    correct_track: Track,
    tvshows_directory: Path,
) -> None:
    name, season_name, season = get_tvshow_info(season_number, imdb_id=imdb_id)
    season_directory = tvshows_directory / name / season_name
    destination_directory = Path(f'{season_directory} Edited')
    assert destination_directory.exists()

    for episode in season['episodes'][:available_episode_count]:
        ename = episode['name']
        enumber = episode['episode_number']

        treated_episode_subtitle_file_path = destination_directory.joinpath(
            f'{name} - S{season_number:02d}E{enumber:02d} - {ename}'
            f'.{language_code}{suffix}',
        )
        assert treated_episode_subtitle_file_path.exists()

        if include_full_information:
            media_info = MediaInfo.parse(treated_episode_subtitle_file_path)
            for field in fields(correct_track):
                assert getattr(
                    media_info.text_tracks[0], field.name
                ) == getattr(correct_track, field.name)
