from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class DubbingSupplier:
    """
    Represents a dubbing supplier data structure.

    Attributes
    ----------
    name: str
        Name of dubbing supplier, if dubbing supplier represents
        original audio of movie or tv show should be set to its
        language.

    audio_language_code: str
        Current 3-letter language code for audio track
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    subtitle_language_code: str
        Current 3-letter language code for subtitle track
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    correct_language_code: str
        Correct 3-letter language code for dubbing supplier
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    audio_search_pattern: str, optional
        The search pattern for finding audio track

    subtitle_search_pattern: str, optional
        The search pattern for finding subtitle track

    file_id: int
        The file id which include dubbing supplier tracks
    """

    name: str
    audio_language_code: str
    subtitle_language_code: str
    correct_language_code: str
    audio_search_pattern: Optional[str]
    subtitle_search_pattern: Optional[str]
    file_id: int

    _audio_track_id: int = None
    _subtitle_track_id: int = None

    def __getattr__(self, item: str) -> Any:
        if item in ('_has_audio', '_has_subtitle'):
            tt = item.split('_')[-1]
            return self.__getattribute__(f'_{tt}_track_id') is not None

        return self.__getattribute__(item)


@dataclass
class FileInfo:
    """
    Represents a file info data structure.

    Attributes
    ----------
    path: Path
        The file path
    id: int
        The file id
    """

    path: Path
    id: int
