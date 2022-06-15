import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional

import tmdbsimple as tmdb
from pymediainfo import MediaInfo, Track

from medicure.data_structures import DubbingSupplier, FileInfo
from medicure.utils import (
    extract_episode_number,
    get_movie_name,
    get_tvshow_info,
)


class Medicure:
    """
    The Medicure
    """

    _media_suffix_pattern = r'\.(mkv|m4v|mp4|mka|mp3)$'
    _subtitle_suffix_pattern = r'\.(srt|mks|idx|sub)$'

    def __init__(
        self,
        tmdb_api_key: str,
        movies_directory: Optional[Path] = None,
        tvshows_directory: Optional[Path] = None,
    ) -> None:
        """
        Initializes Medicure.

        Parameters
        ----------
        tmdb_api_key: str
            Your TMDB API key

        movies_directory: Path, optional
            Your movies' directory, this should be given for treating a
            movie.

        tvshows_directory: Path, optional
            Your TV shows' directory, this should be given for treating
            a TV show.
        """
        tmdb.API_KEY = tmdb_api_key
        self._movies_directory = movies_directory
        self._tvshows_directory = tvshows_directory
        self._dubbing_suppliers: Optional[List[DubbingSupplier]] = None
        self._movie_file_infos: Optional[List[FileInfo]] = None
        self._season_file_infos: Optional[
            DefaultDict[int, List[FileInfo]]
        ] = None
        self._video_track_id: Optional[int] = None

    def treat_media(
        self,
        imdb_id: str,
        file_search_pattern_to_id: Dict[str, int],
        video_language_code: str,
        video_source: str,
        video_release_format: str,
        dubbing_suppliers: List[DubbingSupplier],
        season_number: Optional[int] = None,
    ) -> None:
        """
        Fixes video source, audio source, file name and language for
        all tracks.

        Parameters
        ----------
        imdb_id: str
            IMDB id

        file_search_pattern_to_id: dict[str, int]
            Dict of patterns for finding files to file ids

        video_language_code: str
            3-letter language code for video track
            See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
            for available langauge codes.

        video_source: str
            Source of the video file; name of encoder or the website
            which video is downloaded from

        video_release_format: str
            Format of the video file eg: Blu-ray, WEBRip, etc. See
            https://en.wikipedia.org/wiki/Pirated_movie_release_types
            for available formats.

        dubbing_suppliers: list[DubbingSupplier]
            List of possible dubbing suppliers

        season_number: int, optional
            If imdb_id is a TV show, season number should be given.
        """
        self._dubbing_suppliers = dubbing_suppliers

        # Getting info from TMDB
        info = tmdb.Find(imdb_id).info(external_source='imdb_id')

        # If id is a movie
        if info['movie_results']:
            assert (
                self._movies_directory is not None
            ), 'Movies directory has been not given for a movie.'

            movie_name = get_movie_name(info)
            movie_directory = self._movies_directory / movie_name
            self._scan_directory(
                movie_directory,
                file_search_pattern_to_id,
                'movie',
                rf'({self._media_suffix_pattern})'
                rf'|({self._subtitle_suffix_pattern})',
            )
            self._reset_tracks_info()
            for file_info in self._movie_file_infos:
                self._save_file_tracks_info(file_info)

            destination_directory = self._get_destination_directory(
                movie_directory
            )
            os.system(
                'mkvmerge -o "{output}" {track_config}'
                ''.format(
                    output=destination_directory / f'{movie_name}.mkv',
                    track_config=self._get_track_config(
                        'movie',
                        video_language_code,
                        video_source,
                        video_release_format,
                    ),
                )
            )

        # If id is a TV show
        elif info['tv_results']:
            assert (
                self._tvshows_directory is not None
            ), 'TV shows directory has been not given for a TV show.'
            assert (
                season_number is not None
            ), '`season_number` has not been given for a TV show.'

            name, season_name, season = get_tvshow_info(season_number, info)
            season_directory = self._tvshows_directory / name / season_name
            self._scan_directory(
                season_directory,
                file_search_pattern_to_id,
                'season',
                rf'({self._media_suffix_pattern})'
                rf'|({self._subtitle_suffix_pattern})',
            )

            destination_directory = self._get_destination_directory(
                season_directory
            )

            for episode in season['episodes']:
                self._reset_tracks_info()
                ename = episode['name']
                enumber = episode['episode_number']

                # If episode file does not exist
                if enumber not in self._season_file_infos:
                    continue

                for file_info in self._season_file_infos[enumber]:
                    self._save_file_tracks_info(file_info)

                os.system(
                    'mkvmerge -o "{output}" {track_config}'
                    ''.format(
                        output=destination_directory.joinpath(
                            f'{name} '
                            f'- S{season_number:02d}E{enumber:02d} '
                            f'- {ename}.mkv',
                        ),
                        track_config=self._get_track_config(
                            'tvshow',
                            video_language_code,
                            video_source,
                            video_release_format,
                            enumber,
                        ),
                    )
                )

    def treat_subtitle(
        self,
        imdb_id: str,
        file_search_pattern_to_id: Dict[str, int],
        language_code: str,
        source: Optional[str] = None,
        release_format: Optional[str] = None,
        include_full_information: bool = False,
        season_number: Optional[int] = None,
    ) -> None:
        """
        Fixes subtitle source, file name and language.

        Parameters
        ----------
        imdb_id: str
            IMDB id

        file_search_pattern_to_id: dict[str, int]
            Dict of patterns for finding files to file ids

        language_code: str
            3-letter language code for subtitle
            See https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
            for available langauge codes.

        source: str, optional
            Source of the subtitle file: name of author or the website
            which subtitle is downloaded from. This should be given only
            when `include_full_information` is `True`.

        release_format: str, optional
            Format of the video that the subtitle is sync with eg:
            Blu-ray, WEBRip, etc. See
            https://en.wikipedia.org/wiki/Pirated_movie_release_types
            for available formats. This should be given only
            when `include_full_information` is `True`.

        include_full_information: bool
            If set to `True` the subtitle will be converted to mks
            format inorder to save all subtitle information. If set to
            `True`, `source` and `release_format`
            should also be given.

        season_number: int, optional
            If imdb_id is a TV show season number should be given.
        """
        if include_full_information:
            assert source is not None and release_format is not None, (
                'When `include_full_information` is `True`, '
                '`source` and `release_format` should be given.'
            )

        # Getting info from TMDB
        info = tmdb.Find(imdb_id).info(external_source='imdb_id')

        track_config = (
            '--language 0:{lc} '
            '--track-name 0:"{tn}" '
            '--sub-charset 0:WINDOWS-1256 '
            '--default-track 0 '
            '--forced-track 0:0 '
        ).format(
            lc=language_code,
            tn=f'{source} {release_format}',
        )

        # If id is a movie
        if info['movie_results']:
            assert (
                self._movies_directory is not None
            ), 'Movies directory has been not given for a movie.'

            movie_name = get_movie_name(info)
            movie_directory = self._movies_directory / movie_name
            self._scan_directory(
                movie_directory,
                file_search_pattern_to_id,
                'movie',
                self._subtitle_suffix_pattern,
                include_full_information,
            )
            destination_directory = self._get_destination_directory(
                movie_directory
            )
            output = destination_directory / f'{movie_name}.{language_code}'

            if include_full_information:
                os.system(
                    'mkvmerge -o "{output}" {track_config}"{input}"'
                    ''.format(
                        output=f'{output}.mks',
                        track_config=track_config,
                        input=self._movie_file_infos[0].path,
                    )
                )
            else:
                for file_info in self._movie_file_infos:
                    original_file_path = file_info.path
                    final_file_path = '{output}{ext}'.format(
                        output=output,
                        ext=original_file_path.suffix,
                    )
                    shutil.copyfile(original_file_path, final_file_path)
                    print(
                        f'The file: {original_file_path} '
                        f'copied and renamed to: {final_file_path}.',
                    )

        # If id is a TV show
        elif info['tv_results']:
            assert (
                self._tvshows_directory is not None
            ), 'TV shows directory has been not given for a TV show.'
            assert (
                season_number is not None
            ), '`season_number` has not been given for a TV show.'

            name, season_name, season = get_tvshow_info(season_number, info)
            season_directory = self._tvshows_directory / name / season_name
            self._scan_directory(
                season_directory,
                file_search_pattern_to_id,
                'season',
                self._subtitle_suffix_pattern,
                include_full_information,
            )
            destination_directory = self._get_destination_directory(
                season_directory
            )

            for episode in season['episodes']:
                ename = episode['name']
                enumber = episode['episode_number']

                # If episode file exists
                if enumber not in self._season_file_infos:
                    continue

                output = destination_directory.joinpath(
                    f'{name} - S{season_number:02d}E{enumber:02d} - {ename}'
                    f'.{language_code}',
                )

                if include_full_information:
                    os.system(
                        'mkvmerge -o "{output}" {track_config}"{input}"'
                        ''.format(
                            output=f'{output}.mks',
                            track_config=track_config,
                            input=self._season_file_infos[enumber][0].path,
                        )
                    )
                else:
                    for file_info in self._season_file_infos[enumber]:
                        original_file_path = file_info.path
                        final_file_path = '{output}{ext}'.format(
                            output=output,
                            ext=original_file_path.suffix,
                        )
                        shutil.copyfile(original_file_path, final_file_path)
                        print(
                            f'The file: {original_file_path} '
                            f'copied and renamed to : {final_file_path}.',
                        )

    def _scan_directory(
        self,
        directory: Path,
        file_search_pattern_to_id: Dict[str, int],
        directory_type: str,
        file_suffix_pattern: str,
        include_full_information: bool = True,
    ) -> None:
        setattr(
            self,
            f'_{directory_type}_file_infos',
            list() if directory_type == 'movie' else defaultdict(list),
        )

        for file_name in directory.iterdir():
            if re.search(file_suffix_pattern, file_name.suffix) is None:
                continue

            file_infos = getattr(self, f'_{directory_type}_file_infos')
            if directory_type == 'season':
                file_infos = file_infos[extract_episode_number(file_name)]

            for pattern in file_search_pattern_to_id:
                if re.search(pattern, str(file_name)) is None:
                    continue

                assert (
                    not include_full_information or file_name.suffix != '.sub'
                ), 'Files with .sub suffix does not contain any information.'

                file_infos.append(
                    FileInfo(
                        path=directory / file_name,
                        id=file_search_pattern_to_id[pattern],
                    ),
                )
                break

        if directory_type == 'movie':
            self._movie_file_infos.sort(key=lambda file: file.id)
        # season
        else:
            for enumber in self._season_file_infos:
                self._season_file_infos[enumber].sort(key=lambda file: file.id)

    def _save_file_tracks_info(self, file_info: FileInfo) -> None:
        media_info = MediaInfo.parse(file_info.path)
        for track in media_info.tracks:

            if track.track_type == 'Video':
                self._video_track_id = track.track_id - 1
                continue

            track_type_to_mediainfo_track_type = {
                'audio': 'Audio',
                'subtitle': 'Text',
            }
            for tt, mitt in track_type_to_mediainfo_track_type.items():
                if track.track_type == mitt:
                    for ds in self._dubbing_suppliers:
                        if (
                            not getattr(ds, f'_has_{tt}')
                            and file_info.id == ds.file_id
                            and self._track_title_match(
                                track, getattr(ds, f'{tt}_search_pattern')
                            )
                            and self._track_language_match(
                                track, getattr(ds, f'{tt}_language_code')
                            )
                        ):
                            setattr(
                                ds,
                                f'_{tt}_track_id',
                                (track.track_id or 1) - 1,
                            )
                            break
                    break

    def _reset_tracks_info(self) -> None:
        for ds in self._dubbing_suppliers:
            ds._audio_track_id = None
            ds._subtitle_track_id = None

    def _get_track_config(
        self,
        id_type: str,
        video_language_code: str,
        video_source: str,
        video_release_format: str,
        episode_number: int = None,
    ) -> str:
        track_config = '--track-order {track_order} '.format(
            track_order=self._get_track_order(),
        )
        file_infos = []
        if id_type == 'movie':
            file_infos = self._movie_file_infos
        elif id_type == 'tvshow':
            file_infos = self._season_file_infos[episode_number]

        for file_info in file_infos:
            file_tracks_ids = {
                'audio': [],
                'subtitle': [],
            }

            if file_info.id == 0:
                track_config += '--language {tid}:{lc} '.format(
                    tid=self._video_track_id,
                    lc=video_language_code,
                )
                track_config += '--default-track {tid} '.format(
                    tid=self._video_track_id,
                )
                track_config += '--forced-track {tid}:0 '.format(
                    tid=self._video_track_id
                )
                track_config += '--track-name {tid}:"{tn}" '.format(
                    tid=self._video_track_id,
                    tn=f'{video_source} {video_release_format}',
                )

            for ds in self._dubbing_suppliers:
                if ds.file_id == file_info.id:
                    for tt in ['audio', 'subtitle']:
                        if getattr(ds, f'_has_{tt}'):
                            track_config += self._make_language_code(ds, tt)
                            track_config += self._make_default_or_forced(
                                ds, tt, 'default-track'
                            )
                            track_config += self._make_default_or_forced(
                                ds, tt, 'forced-track'
                            )
                            track_config += self._make_name(ds, tt)
                            file_tracks_ids[tt].append(
                                getattr(ds, f'_{tt}_track_id'),
                            )

            for i, tt in enumerate(['audio', 'subtitle']):
                if len(file_tracks_ids[tt]) > 0:
                    track_config += '--{tt}-tracks {ts} '.format(
                        tt=tt,
                        ts=','.join([str(tid) for tid in file_tracks_ids[tt]]),
                    )
                else:
                    track_config += f'--no-{tt}{"s" * i} '

            track_config += f'"{file_info.path}" '

        return track_config

    def _get_track_order(self) -> str:
        track_order = f'0:{self._video_track_id}'

        for tt in ['audio', 'subtitle']:
            for ds in self._dubbing_suppliers:
                if getattr(ds, f'_has_{tt}'):
                    track_order += self._make_order(ds, tt)

        return track_order

    @staticmethod
    def _make_order(ds: DubbingSupplier, sa: str) -> str:
        return ',{fid}:{tid}'.format(
            fid=ds.file_id,
            tid=getattr(ds, f'_{sa}_track_id'),
        )

    def _make_name(self, ds: DubbingSupplier, sa: str) -> str:
        return '--track-name {tid}:"{tn}" '.format(
            tid=getattr(ds, f'_{sa}_track_id'),
            tn=ds.name if self._dubbing_suppliers[0].name != ds.name else '',
        )

    def _make_default_or_forced(
        self,
        ds: DubbingSupplier,
        sa: str,
        df: str,
    ) -> str:
        flag = 0
        if df == 'default-track' and sa == 'audio':
            if self._dubbing_suppliers[0].name == ds.name:
                flag = 1
        return '--{df} {tid}:{flag} '.format(
            df=df, tid=getattr(ds, f'_{sa}_track_id'), flag=flag
        )

    @staticmethod
    def _get_destination_directory(directory: Path) -> Path:
        destination_directory = Path(f'{directory} Edited')
        if not destination_directory.exists():
            destination_directory.mkdir()

        return destination_directory

    @staticmethod
    def _make_language_code(ds: DubbingSupplier, sa: str) -> str:
        return '--language {tid}:{lc} '.format(
            tid=getattr(ds, f'_{sa}_track_id'), lc=ds.correct_language_code
        )

    @staticmethod
    def _track_title_match(track: Track, pattern: str) -> bool:
        title = track.title
        if pattern is None and title is None:
            return True
        if pattern is None or title is None:
            return False
        return re.search(pattern, title) is not None

    @staticmethod
    def _track_language_match(track: Track, language_code: str) -> bool:
        language = track.language
        if language_code is None and language is None:
            return True
        if language_code is None or language is None:
            return False
        return language_code in track.other_language
