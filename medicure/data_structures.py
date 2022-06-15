from dataclasses import MISSING, dataclass, fields
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DubbingSupplier:
    """
    Represents a dubbing supplier data structure.

    Attributes
    ----------
    name: str
        Name of dubbing supplier, if dubbing supplier represents
        original audio of movie or TV show this doesn't matter but
        should set to `'original'` for better convenience.

    file_id: int
        The file id which include dubbing supplier tracks

    correct_language_code: str
        Correct 3-letter language code for dubbing supplier
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    audio_language_code: str, optional
        Current 3-letter language code for audio track
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    subtitle_language_code: str, optional
        Current 3-letter language code for subtitle track
        See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
        for available langauge codes.

    audio_search_pattern: str, optional
        The search pattern for finding audio track

    subtitle_search_pattern: str, optional
        The search pattern for finding subtitle track
    """

    name: str
    file_id: int
    correct_language_code: str
    audio_language_code: Optional[str] = None
    subtitle_language_code: Optional[str] = None
    audio_search_pattern: Optional[str] = None
    subtitle_search_pattern: Optional[str] = None

    _audio_track_id: int = None
    _subtitle_track_id: int = None

    def __getattr__(self, item: str) -> Any:
        if item in ('_has_audio', '_has_subtitle'):
            tt = item.split('_')[-1]
            return self.__getattribute__(f'_{tt}_track_id') is not None

    def to_list(self) -> List[Any]:
        """
        Converts dubbing supplier to a minimal list so can be easily in
        Medicure's CLI.

        Returns
        -------
        result: list[Any]
            List dubbing supplier
        """
        ds_list = []
        last_append_index = 0
        for i, field in enumerate(fields(self)):
            field_value = self.__getattribute__(field.name)

            if field.default == MISSING:
                ds_list.append(field_value)
                last_append_index = i

            elif field_value != field.default:
                for f in fields(self)[last_append_index + 1 : i]:
                    ds_list.append(self.__getattribute__(f.name))
                ds_list.append(field_value)
                last_append_index = i

        return ds_list

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts dubbing supplier to a minimal dictionary so can be
        easily used in Medicure's CLI.

        Returns
        -------
        result: dict[str, Any]
            Dictionary dubbing supplier
        """

        ds_dict = {}
        for field in fields(self):
            field_value = self.__getattribute__(field.name)
            if field_value != field.default:
                ds_dict[field.name] = field_value

        return ds_dict


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
