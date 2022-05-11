import os
import re
from os import path
from typing import Dict, Optional

import tmdbsimple as tmdb
import typer

from medicure.utils import escape_nonpath_characters, extract_episode_number


class Subcure:
    """
    The Subcure
    """

    subtitle_ext_pattern = r'\.srt$|\.mks$|\.idx$'

    def __init__(
        self,
        movies_directory: Optional[str] = None,
        tvshows_directory: Optional[str] = None,
    ) -> None:
        """
        Initialize Subtitle

        Parameters
        ----------
        movies_directory: str, optional
            Your movies' directory, this should be given for treating a
            movie subtitle.

        tvshows_directory: str, optional
            Your tv shows' directory, this should be given for treating
            a tv show subtitle.
        """
        self._movies_directory = movies_directory
        self._tvshows_directory = tvshows_directory
        self._movie_file: Optional[str] = None
        self._season_files: Optional[Dict[int, str]] = None

    def treat(
        self,
        imdb_id: str,
        file_search_pattern: str,
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

        file_search_pattern: str
            Pattern for finding files

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
            `True`, `subtitle_source` and `subtitle_release_format`
            should also be given.

        season_number: int, optional
            If imdb_id is a tv show season number should be given.
        """
        # Getting info from TMDB
        find = tmdb.Find(imdb_id)
        info = find.info(external_source='imdb_id')

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
            movie = info['movie_results'][0]
            title = escape_nonpath_characters(movie['title'])
            release_year = movie['release_date'][:5]
            movie_directory = path.join(
                self._movies_directory,
                f'{title} - {release_year}',
            )
            self._scan_directory(movie_directory, file_search_pattern, 'movie')
            output = path.join(
                movie_directory,
                f'{title} - {release_year}.{language_code}',
            )

            if include_full_information:
                os.system(
                    'mkvmerge -o "{output}" {track_config}"{input}"'
                    ''.format(
                        output=f'{output}.mks',
                        track_config=track_config,
                        input=self._movie_file,
                    )
                )
            else:
                original_file_path = self._movie_file
                final_file_path = '{output}{ext}'.format(
                    output=output,
                    ext=re.search(
                        self.subtitle_ext_pattern, self._movie_file
                    ).group(),
                )
                os.rename(original_file_path, final_file_path)
                typer.echo(
                    f'The file: {original_file_path} '
                    f'renamed to: {final_file_path}',
                )

        # If id is a tv show
        elif info['tv_results']:
            assert (
                self._tvshows_directory is not None
            ), 'tv shows directory has been not given for a tv show.'
            assert (
                season_number is not None
            ), '`season_number` can not be None for a tv show.'

            tvshow = info['tv_results'][0]
            name = escape_nonpath_characters(tvshow['name'])
            tmdb_id = tvshow['id']
            season = tmdb.TV_Seasons(tmdb_id, season_number).info()
            season_name = escape_nonpath_characters(season['name'])

            season_directory = path.join(
                self._tvshows_directory, name, season_name
            )
            self._scan_directory(
                season_directory, file_search_pattern, 'season'
            )

            for episode in season['episodes']:
                ename = escape_nonpath_characters(episode['name'])
                enumber = episode['episode_number']

                # If episode file exists
                if enumber not in self._season_files:
                    continue

                output = path.join(
                    season_directory,
                    f'{name} - S{season_number:02d}E{enumber:02d} - {ename}'
                    f'.{language_code}',
                )

                if include_full_information:
                    os.system(
                        'mkvmerge -o "{output}" {track_config}"{input}"'
                        ''.format(
                            output=f'{output}.mks',
                            track_config=track_config,
                            input=self._season_files[enumber],
                        )
                    )
                else:
                    original_file_path = self._season_files[enumber]
                    final_file_path = '{output}{ext}'.format(
                        output=output,
                        ext=re.search(
                            self.subtitle_ext_pattern,
                            self._season_files[enumber],
                        ).group(),
                    )
                    os.rename(original_file_path, final_file_path)
                    typer.echo(
                        f'The file: {original_file_path} '
                        f'renamed to: {final_file_path}',
                    )

    def _scan_directory(
        self, directory: str, file_pattern: str, directory_type: str
    ) -> None:
        for file_name in os.listdir(directory):
            if (
                re.search(self.subtitle_ext_pattern, file_name) is None
                or re.search(file_pattern, file_name) is None
            ):
                continue

            file_path = path.join(directory, file_name)
            if directory_type == 'movie':
                self._movie_file = file_path
                break
            # season
            else:
                episode_number = extract_episode_number(file_name)
                self._season_files[episode_number] = file_path
