# Medicure
[![tests](https://github.com/alirezatheh/medicure/workflows/tests/badge.svg)](https://github.com/alirezatheh/medicure/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/alirezatheh/medicure/branch/main/graph/badge.svg)](https://codecov.io/gh/alirezatheh/medicure)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/AlirezaTheH/medicure/main.svg)](https://results.pre-commit.ci/latest/github/alirezatheh/medicure/main)
[![PyPI Version](https://img.shields.io/pypi/v/medicure)](https://pypi.python.org/pypi/medicure)
[![Python Versions](https://img.shields.io/pypi/pyversions/medicure)](https://pypi.org/project/medicure)
[![Documentation Status](https://readthedocs.org/projects/medicure/badge/?version=latest)](https://medicure.readthedocs.io/en/latest/?badge=latest)

Medicure is a cosmetic treatment for your media files: movies, TV shows and
also their subtitles. Medicure provides a command-line tool and also a Python
package for you to properly rename, sort tracks and correct tracks info for
your files.

## Name
The word *medicure* is combination of *media* and the Latin word *cura* which
means "care".

## Installation
The easiest way to install is from PyPI:
```bash
pip install medicure
```
Alternatively, you can install directly from GitHub:
```bash
pip install git+https://github.com/alirezatheh/medicure.git
```

## Requirements
- [TMDB](https://www.themoviedb.org) API Key: Medicure uses TMDB's API to get
  correct info for movies and TV shows. So you need to create a TMDB account
  and generate an API key in order to use Medicure.
- [Mediainfo](https://mediaarea.net/en/MediaInfo): Medicure requires Mediainfo
  to extract track info from video and audio files.
- [MKVToolNix](https://mkvtoolnix.download): Medicure uses `mkvmerge` to craete
  new treated media files. `mkvmerge` is one of the MKVToolNix's command-line
  tools.

## Simple Example
In this example we want to treat
[Peaky Blinders](https://en.wikipedia.org/wiki/Peaky_Blinders_(TV_series))'s
Season 6 video files, downloaded from [PSArips](https://psa.pm).

First we search for the TV show in [TMDB](https://www.themoviedb.org) to see
season names. In this case season name starts with `Series`. In our TV shows
directory we create `Peaky Blinders/Series 6` directory and put the files
there. Directory structure will look like this:
```bash
TV Shows
└── Peaky Blinders
    └── Series 6
        ├── Peaky.Blinders.S06E01.1080p.10bit.WEB-DL.x265.HEVC.PSA.AM.mkv
        ├── Peaky.Blinders.S06E02.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        ├── Peaky.Blinders.S06E03.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        ├── Peaky.Blinders.S06E04.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        ├── Peaky.Blinders.S06E05.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        └── Peaky.Blinders.S06E06.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
```

And each file has the following track infos:

| Type     | Title | Language     | Default | Forced |
|----------|-------|--------------|---------|--------|
| Video    |       | Undetermined | Yes     | No     |
| Audio    |       | English      | Yes     | No     |
| Subtitle |       | English      | Yes     | No     |

Now we run the following python snippet:

```python
from pathlib import Path

from medicure import Medicure, DubbingSupplier

medicure = Medicure(
    tmdb_api_key='YOUR_TMDB_API_KEY',
    tvshows_directory=Path('path/to/tvshows_directory'),
)
medicure.treat_media(
    # You can find this in url of TV show in IMDb.
    imdb_id='tt2442560',
    file_search_patterns=[
        # We have only one file for each episode that can be found by
        # this pattern.
        'PSA',
    ],
    video_language_code='eng',
    video_source='PSA',
    video_release_format='WEB-DL',
    dubbing_suppliers=[
        # In this example we only have one dubbing supplier and that's
        # which contains original audio and subtitle.
        DubbingSupplier(
            name='original',
            file_id=0,
            correct_language_code='eng',
            audio_language_code='eng',
            subtitle_language_code='eng',
        ),
    ],
    season_number=6,
)
```
Then directory structure will look like this:
```bash
TV Shows
└── Peaky Blinders
    ├── Series 6
    │   ├── Peaky.Blinders.S06E01.1080p.10bit.WEB-DL.x265.HEVC.PSA.AM.mkv
    │   ├── Peaky.Blinders.S06E02.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
    │   ├── Peaky.Blinders.S06E03.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
    │   ├── Peaky.Blinders.S06E04.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
    │   ├── Peaky.Blinders.S06E05.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
    │   └── Peaky.Blinders.S06E06.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
    └── Series 6 Edited
        ├── Peaky Blinders - S06E01 - Black Day.mkv
        ├── Peaky Blinders - S06E02 - Black Shirt.mkv
        ├── Peaky Blinders - S06E03 - Gold.mkv
        ├── Peaky Blinders - S06E04 - Sapphire.mkv
        ├── Peaky Blinders - S06E05 - The Road to Hell.mkv
        └── Peaky Blinders - S06E06 - Lock and Key.mkv
```
And each file track infos:

| Type     | Title      | Language | Default | Forced |
|----------|------------|----------|---------|--------|
| Video    | PSA WEB-DL | English  | Yes     | No     |
| Audio    |            | English  | Yes     | No     |
| Subtitle |            | English  | No      | No     |

Let's treat again, this time using Medicure's command-line interface.

Since we're using CLI for the first time, we need to save our TMDB API key and
TV shows directory locally:
```bash
medicure save tmdb-info YOUR_TMDB_API_KEY
```
```bash
medicure save collection-info \
--tvshows-directory PATH_TO_YOUR_TVSHOWS_DIRECTORY
```
Now we can run:
```bash
medicure treat media \
tt2442560 \
'["PSA"]' \
eng \
PSA \
WEB-DL \
'[["original", 0, "eng", "eng", "eng"]]' \
6
```

If you want to learn more about Medicure with more in depth examples you can
visit [Medicure's documentation](https://medicure.readthedocs.io).
