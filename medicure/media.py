import os
import re
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional

import tmdbsimple as tmdb
from iso639 import languages
from pymediainfo import MediaInfo

from medicure.data_structures import DubbingSupplier, FileInfo
from medicure.utils import escape_nonpath_characters, extract_episode_number


class Medicure:
    """
    The Medicure
    """

    media_ext_pattern = r'\.mkv$|\.m4v$|\.mp4$|\.mka$'

    def __init__(
        self,
        movies_directory: Optional[Path] = None,
        tvshows_directory: Optional[Path] = None,
    ) -> None:
        """
        Initializes Medicure.

        Parameters
        ----------
        movies_directory: Path, optional
            Your movies' directory, this should be given for treating a
            movie.

        tvshows_directory: Path, optional
            Your tv shows' directory, this should be given for treating
            a tv show.
        """
        self._movies_directory = movies_directory
        self._tvshows_directory = tvshows_directory
        self._dubbing_suppliers: Optional[List[DubbingSupplier]] = None
        self._movie_file_infos: Optional[List[FileInfo]] = None
        self._season_file_infos: Optional[
            DefaultDict[int, List[FileInfo]]
        ] = None
        self._video_track_id: Optional[int] = None

    def treat(
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
            If imdb_id is a tv show, season number should be given.
        """
        self._dubbing_suppliers = dubbing_suppliers

        # Getting info from TMDB
        find = tmdb.Find(imdb_id)
        info = find.info(external_source='imdb_id')

        # If id is a movie
        if info['movie_results']:
            assert (
                self._movies_directory is not None
            ), 'Movies directory has been not given for a movie.'
            movie = info['movie_results'][0]
            title = escape_nonpath_characters(movie['title'])
            release_year = movie['release_date'][:5]
            movie_directory = self._movies_directory.joinpath(
                f'{title} - {release_year}'
            )
            self._scan_directory(
                movie_directory, file_search_pattern_to_id, 'movie'
            )
            self._reset_tracks_info()
            for file_info in self._movie_file_infos:
                self._save_file_tracks_info(file_info)

            os.system(
                'mkvmerge -o "{output}" {track_config}'
                ''.format(
                    output=movie_directory.joinpath(
                        f'{title} - {release_year}.mkv'
                    ),
                    track_config=self._get_track_config(
                        'movie',
                        video_language_code,
                        video_source,
                        video_release_format,
                    ),
                )
            )

        # If id is a tv show
        elif info['tv_results']:
            assert (
                self._tvshows_directory is not None
            ), 'tv shows directory has been not given for a tv show.'
            assert (
                season_number is not None
            ), '`season_number` has not been given for a tv show.'

            tvshow = info['tv_results'][0]
            name = escape_nonpath_characters(tvshow['name'])
            tmdb_id = tvshow['id']
            season = tmdb.TV_Seasons(tmdb_id, season_number).info()
            season_name = escape_nonpath_characters(season['name'])

            season_directory = self._tvshows_directory.joinpath(
                name, season_name
            )
            self._scan_directory(
                season_directory, file_search_pattern_to_id, 'season'
            )

            # Create destination directory if not exists already
            destination_directory = Path(f'{str(season_directory)} Edited')
            if not destination_directory.exists():
                destination_directory.mkdir()

            for episode in season['episodes']:
                self._reset_tracks_info()
                ename = escape_nonpath_characters(episode['name'])
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

    def _scan_directory(
        self,
        directory: Path,
        file_search_pattern_to_id: Dict[str, int],
        directory_type: str,
    ) -> None:
        setattr(
            self,
            f'_{directory_type}_file_infos',
            list() if directory_type == 'movie' else defaultdict(list),
        )

        for file_name in directory.iterdir():
            if re.search(self.media_ext_pattern, file_name.suffix) is None:
                continue

            file_infos = getattr(self, f'_{directory_type}_file_infos')
            if directory_type == 'season':
                file_infos = file_infos[extract_episode_number(file_name)]

            for pattern in file_search_pattern_to_id:
                if re.search(pattern, str(file_name)) is None:
                    continue

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

            track_types = {
                'audio': 'Audio',
                'subtitle': 'Text',
            }
            for tt in track_types:
                if track.track_type == track_types[tt]:
                    for ds in self._dubbing_suppliers:
                        if (
                            not getattr(ds, f'_has_{tt}')
                            and file_info.id == ds.file_id
                            and (
                                self._match(
                                    getattr(ds, f'{tt}_search_pattern'),
                                    track.title,
                                )
                                or (
                                    ds.audio_language_code is None
                                    and track.language is None
                                )
                                or ds.audio_language_code
                                == languages.get(
                                    part1=track.language,
                                ).part2b
                            )
                        ):
                            setattr(ds, f'_{tt}_track_id', track.track_id - 1)
                    continue

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

            for tt in ['audio', 'subtitle']:
                if len(file_tracks_ids[tt]) > 0:
                    track_config += '--{tt}-tracks {ts} '.format(
                        tt=tt,
                        ts=','.join([str(tid) for tid in file_tracks_ids[tt]]),
                    )
                else:
                    track_config += f'--no-{tt} '

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
    def _make_language_code(ds: DubbingSupplier, sa: str) -> str:
        return '--language {tid}:{lc} '.format(
            tid=getattr(ds, f'_{sa}_track_id'), lc=ds.correct_language_code
        )

    @staticmethod
    def _match(pattern: str, string: str) -> bool:
        if pattern == r'':
            return True
        if pattern is None or string is None:
            return False
        return re.search(pattern, string) is not None
