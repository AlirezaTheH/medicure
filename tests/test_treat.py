from pathlib import Path
from typing import Any, Dict, List

import pytest
from pymediainfo import MediaInfo

from medicure.core import Medicure
from medicure.data_structures import DubbingSupplier
from medicure.utils import get_movie_name, get_tvshow_info


@pytest.mark.parametrize(
    'file_search_pattern_to_id, dubbing_suppliers, correct_tracks_info',
    [
        # Single file with a dummy dubbing supplier
        (
            {r'\.mkv': 0},
            [
                # Dummy, won't match with any track.
                DubbingSupplier(
                    name='original',
                    file_id=0,
                    correct_language_code='eng',
                ),
                DubbingSupplier(
                    name='original',
                    file_id=0,
                    correct_language_code='eng',
                    audio_language_code='eng',
                    subtitle_language_code='eng',
                ),
            ],
            [
                {
                    'track_id': 1,
                    'track_type': 'Video',
                    'title': 'PSA WEB-DL',
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 2,
                    'track_type': 'Audio',
                    'title': None,
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 3,
                    'track_type': 'Text',
                    'title': None,
                    'language': 'en',
                    'default': 'No',
                    'forced': 'No',
                },
            ],
        ),
        # An extra audio file with a dummy dubbing supplier
        (
            {r'\.mkv': 0, r'\.mka': 1},
            [
                DubbingSupplier(
                    name='original',
                    file_id=0,
                    correct_language_code='eng',
                    audio_language_code='eng',
                    subtitle_language_code='eng',
                ),
                # Dummy, won't match with any track.
                DubbingSupplier(
                    name='TinyMoviez',
                    file_id=1,
                    correct_language_code='per',
                ),
                DubbingSupplier(
                    name='TinyMoviez',
                    file_id=1,
                    correct_language_code='per',
                    audio_search_pattern=r'TinyMoviez\.co',
                ),
            ],
            [
                {
                    'track_id': 1,
                    'track_type': 'Video',
                    'title': 'PSA WEB-DL',
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 2,
                    'track_type': 'Audio',
                    'title': None,
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 3,
                    'track_type': 'Audio',
                    'title': 'TinyMoviez',
                    'language': 'fa',
                    'default': 'No',
                    'forced': 'No',
                },
                {
                    'track_id': 4,
                    'track_type': 'Text',
                    'title': None,
                    'language': 'en',
                    'default': 'No',
                    'forced': 'No',
                },
            ],
        ),
        # An extra subtitle file
        (
            {r'\.mkv': 0, r'\.srt': 1},
            [
                DubbingSupplier(
                    name='original',
                    file_id=0,
                    correct_language_code='eng',
                    audio_language_code='eng',
                    subtitle_language_code='eng',
                ),
                DubbingSupplier(
                    name='TinyMoviez',
                    file_id=1,
                    correct_language_code='per',
                ),
            ],
            [
                {
                    'track_id': 1,
                    'track_type': 'Video',
                    'title': 'PSA WEB-DL',
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 2,
                    'track_type': 'Audio',
                    'title': None,
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 3,
                    'track_type': 'Text',
                    'title': None,
                    'language': 'en',
                    'default': 'No',
                    'forced': 'No',
                },
                {
                    'track_id': 4,
                    'track_type': 'Text',
                    'title': 'TinyMoviez',
                    'language': 'fa',
                    'default': 'No',
                    'forced': 'No',
                },
            ],
        ),
        # Extra audio and subtitle files
        (
            {r'\.mkv': 0, r'\.mka': 1, r'\.srt': 2},
            [
                DubbingSupplier(
                    name='original',
                    file_id=0,
                    correct_language_code='eng',
                    audio_language_code='eng',
                    subtitle_language_code='eng',
                ),
                DubbingSupplier(
                    name='TinyMoviez',
                    file_id=1,
                    correct_language_code='per',
                    audio_search_pattern=r'TinyMoviez\.co',
                ),
                DubbingSupplier(
                    name='TinyMoviez',
                    file_id=2,
                    correct_language_code='per',
                ),
            ],
            [
                {
                    'track_id': 1,
                    'track_type': 'Video',
                    'title': 'PSA WEB-DL',
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 2,
                    'track_type': 'Audio',
                    'title': None,
                    'language': 'en',
                    'default': 'Yes',
                    'forced': 'No',
                },
                {
                    'track_id': 3,
                    'track_type': 'Audio',
                    'title': 'TinyMoviez',
                    'language': 'fa',
                    'default': 'No',
                    'forced': 'No',
                },
                {
                    'track_id': 4,
                    'track_type': 'Text',
                    'title': None,
                    'language': 'en',
                    'default': 'No',
                    'forced': 'No',
                },
                {
                    'track_id': 5,
                    'track_type': 'Text',
                    'title': 'TinyMoviez',
                    'language': 'fa',
                    'default': 'No',
                    'forced': 'No',
                },
            ],
        ),
    ],
)
def test_treat_media(
    tmdb_api_key: str,
    movies_directory: Path,
    tvshows_directory: Path,
    file_search_pattern_to_id: Dict[str, int],
    dubbing_suppliers: List[DubbingSupplier],
    correct_tracks_info: List[Dict[str, Any]],
) -> None:
    medicure = Medicure(tmdb_api_key, movies_directory, tvshows_directory)
    video_language_code = 'eng'
    video_source = 'PSA'
    video_release_format = 'WEB-DL'

    # Movie
    imdb_id = 'tt1877830'
    medicure.treat_media(
        imdb_id,
        file_search_pattern_to_id,
        video_language_code,
        video_source,
        video_release_format,
        dubbing_suppliers,
    )

    movie_name = get_movie_name(imdb_id=imdb_id)
    movie_directory = movies_directory / movie_name
    destination_directory = Path(f'{movie_directory} Edited')
    assert destination_directory.exists()

    treated_movie_file_path = destination_directory / f'{movie_name}.mkv'
    assert treated_movie_file_path.exists()

    media_info = MediaInfo.parse(treated_movie_file_path)
    for i, track in enumerate(media_info.tracks[1:]):
        for attribute, value in correct_tracks_info[i].items():
            assert getattr(track, attribute) == value

    # TV Show
    imdb_id = 'tt2442560'
    for season_number, available_episode_count in {5: 1, 6: 6}.items():
        medicure.treat_media(
            imdb_id,
            file_search_pattern_to_id,
            video_language_code,
            video_source,
            video_release_format,
            dubbing_suppliers,
            season_number,
        )
        name, season_name, season = get_tvshow_info(
            season_number, imdb_id=imdb_id
        )
        season_directory = tvshows_directory / name / season_name
        destination_directory = Path(f'{season_directory} Edited')
        assert destination_directory.exists()

        for episode in season['episodes'][:available_episode_count]:
            ename = episode['name']
            enumber = episode['episode_number']

            treated_episode_file_path = destination_directory.joinpath(
                f'{name} - S{season_number:02d}E{enumber:02d} - {ename}.mkv',
            )
            assert treated_episode_file_path.exists()

            media_info = MediaInfo.parse(treated_episode_file_path)
            for i, track in enumerate(media_info.tracks[1:]):
                for attribute, value in correct_tracks_info[i].items():
                    assert getattr(track, attribute) == value


@pytest.mark.parametrize('include_full_information', [True, False])
def test_treat_subtitle(
    tmdb_api_key: str,
    movies_directory: Path,
    tvshows_directory: Path,
    include_full_information: bool,
):
    medicure = Medicure(tmdb_api_key, movies_directory, tvshows_directory)
    language_code = 'per'
    source = 'TinyMoviez'
    release_format = 'WEB-DL'
    suffix = '.mks' if include_full_information else '.srt'
    correct_track_info = {
        'track_id': 1,
        'track_type': 'Text',
        'title': f'{source} {release_format}',
        'language': 'fa',
        'default': 'Yes',
        'forced': 'No',
    }

    # Movie
    imdb_id = 'tt1877830'
    medicure.treat_subtitle(
        imdb_id,
        {r'\.srt': 0},
        language_code,
        source,
        release_format,
        include_full_information,
    )

    movie_name = get_movie_name(imdb_id=imdb_id)
    movie_directory = movies_directory / f'{movie_name}'
    destination_directory = Path(f'{movie_directory} Edited')
    assert destination_directory.exists()

    treated_movie_subtitle_file_path = destination_directory.joinpath(
        f'{movie_name}.{language_code}{suffix}'
    )
    assert treated_movie_subtitle_file_path.exists()
    if include_full_information:
        media_info = MediaInfo.parse(treated_movie_subtitle_file_path)
        for attribute, value in correct_track_info.items():
            assert getattr(media_info.text_tracks[0], attribute) == value

    # TV Show
    imdb_id = 'tt2442560'
    for season_number, available_episode_count in {5: 1, 6: 6}.items():
        medicure.treat_subtitle(
            imdb_id,
            {r'\.srt': 0},
            language_code,
            source,
            release_format,
            include_full_information,
            season_number,
        )

        name, season_name, season = get_tvshow_info(
            season_number, imdb_id=imdb_id
        )
        season_directory = tvshows_directory / name / season_name
        destination_directory = Path(f'{season_directory} Edited')
        assert destination_directory.exists()

        for episode in season['episodes'][:available_episode_count]:
            ename = episode['name']
            enumber = episode['episode_number']

            treated_episode_subtitle_file_path = (
                destination_directory.joinpath(
                    f'{name} - S{season_number:02d}E{enumber:02d} - {ename}'
                    f'.{language_code}{suffix}',
                )
            )
            assert treated_episode_subtitle_file_path.exists()

            if include_full_information:
                media_info = MediaInfo.parse(
                    treated_episode_subtitle_file_path
                )
                subtitle_track = media_info.text_tracks[0]
                for attribute, value in correct_track_info.items():
                    assert getattr(subtitle_track, attribute) == value


def test_treat_fail_extract_episode_number(
    tmdb_api_key: str,
    tvshows_directory: Path,
) -> None:
    imdb_id = 'tt2442560'
    language_code = 'per'
    source = 'TinyMoviez'
    release_format = 'WEB-DL'
    season_number = 4
    match = r'File name did not match with episode number pattern\.'
    medicure = Medicure(tmdb_api_key, tvshows_directory=tvshows_directory)
    with pytest.raises(ValueError, match=match):
        medicure.treat_media(
            imdb_id,
            {r'\.mkv': 0},
            language_code,
            source,
            release_format,
            [],
            season_number,
        )
    with pytest.raises(ValueError, match=match):
        medicure.treat_subtitle(
            imdb_id,
            {r'\.mkv': 0},
            language_code,
            source,
            release_format,
            season_number=season_number,
        )
