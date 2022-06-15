from functools import partial
from pathlib import Path

from medicure.data_structures import DubbingSupplier
from tests.data_structures import Track

# The Batman - 2022
movie_imdb_id = 'tt1877830'
# Peaky Blinders
tvshow_imdb_id = 'tt2442560'

tmdb_api_key = None

_collection_directory = Path(__file__).parent / 'data'
movies_directory = _collection_directory / 'Movies'
tvshows_directory = _collection_directory / 'TV Shows'

_language_code = 'eng'
_language_code_two = 'en'
_extra_language_code = 'per'
_extra_language_code_two = 'fa'
_original_source = 'PSA'
_extra_source = 'TinyMoviez'
_release_format = 'WEB-DL'

video_language_code = _language_code
video_source = _original_source
video_release_format = _release_format

_subtitle_file_search_pattern = r'\.srt'
subtitle_file_search_pattern_to_id = {_subtitle_file_search_pattern: 0}
subtitle_language_code = _extra_language_code
subtitle_source = _extra_source
subtitle_release_format = _release_format
subtitle_correct_track = Track(
    1,
    'Text',
    f'{_extra_source} {_release_format}',
    _extra_language_code_two,
    'Yes',
    'No',
)

media_file_search_pattern_to_id = {r'\.mkv': 0}
_extra_media_file_search_pattern_to_id = {r'\.mka': 1}

_original_ds_name = 'original'
_original_ds_args = (
    _original_ds_name,
    0,
    _language_code,
    _language_code,
    _language_code,
)
_extra_audio_ds_args = (
    _extra_source,
    1,
    _extra_language_code,
    None,
    None,
    rf'{_extra_source}\.co',
)

_correct_video_track = Track(
    1,
    'Video',
    f'{_original_source} {_release_format}',
    _language_code_two,
    'Yes',
    'No',
)
_correct_original_audio_track = Track(
    2,
    'Audio',
    None,
    _language_code_two,
    'Yes',
    'No',
)
_correct_extra_audio_track = Track(
    3,
    'Audio',
    _extra_source,
    _extra_language_code_two,
    'No',
    'No',
)
_correct_original_subtitle_track = partial(
    Track,
    track_type='Text',
    title=None,
    language=_language_code_two,
    default='No',
    forced='No',
)
_correct_extra_subtitle_track = partial(
    Track,
    track_type='Text',
    title=_extra_source,
    language=_extra_language_code_two,
    default='No',
    forced='No',
)

treat_media_args = (
    'file_search_pattern_to_id, dubbing_suppliers, correct_tracks',
    [
        # Single file with a dummy dubbing supplier
        (
            media_file_search_pattern_to_id,
            [
                # Dummy, won't match with any track.
                DubbingSupplier(_original_ds_name, 0, _language_code),
                DubbingSupplier(*_original_ds_args),
            ],
            [
                _correct_video_track,
                _correct_original_audio_track,
                _correct_original_subtitle_track(3),
            ],
        ),
        # An extra audio file with a dummy dubbing supplier
        (
            {
                **media_file_search_pattern_to_id,
                **_extra_media_file_search_pattern_to_id,
            },
            [
                DubbingSupplier(*_original_ds_args),
                # Dummy, won't match with any track.
                DubbingSupplier(_extra_source, 1, _extra_language_code),
                DubbingSupplier(*_extra_audio_ds_args),
            ],
            [
                _correct_video_track,
                _correct_original_audio_track,
                _correct_extra_audio_track,
                _correct_original_subtitle_track(4),
            ],
        ),
        # An extra subtitle file
        (
            {
                **media_file_search_pattern_to_id,
                _subtitle_file_search_pattern: 1,
            },
            [
                DubbingSupplier(*_original_ds_args),
                DubbingSupplier(_extra_source, 1, _extra_language_code),
            ],
            [
                _correct_video_track,
                _correct_original_audio_track,
                _correct_original_subtitle_track(3),
                _correct_extra_subtitle_track(4),
            ],
        ),
        # Extra audio and subtitle files
        (
            {
                **media_file_search_pattern_to_id,
                **_extra_media_file_search_pattern_to_id,
                _subtitle_file_search_pattern: 2,
            },
            [
                DubbingSupplier(*_original_ds_args),
                DubbingSupplier(*_extra_audio_ds_args),
                DubbingSupplier(_extra_source, 2, _extra_language_code),
            ],
            [
                _correct_video_track,
                _correct_original_audio_track,
                _correct_extra_audio_track,
                _correct_original_subtitle_track(4),
                _correct_extra_subtitle_track(5),
            ],
        ),
    ],
)
treat_subtitle_args = (
    'include_full_information, suffix',
    [(True, '.mks'), (False, '.srt')],
)
season_info_args = ('season_number, available_episode_count', [(5, 1), (6, 6)])
