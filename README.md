# Medicure
[![tests](https://github.com/alirezatheh/medicure/workflows/tests/badge.svg)](https://github.com/alirezatheh/medicure/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/alirezatheh/medicure/branch/main/graph/badge.svg)](https://codecov.io/gh/alirezatheh/medicure)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/AlirezaTheH/medicure/main.svg)](https://results.pre-commit.ci/latest/github/alirezatheh/medicure/main)
[![PyPI Version](https://img.shields.io/pypi/v/medicure)](https://pypi.python.org/pypi/medicure)
[![Python Versions](https://img.shields.io/pypi/pyversions/medicure)](https://pypi.org/project/medicure)

Medicure is a cosmetic treatment for your media files: movies, TV shows
and also their subtitles. Medicure provides a command-line tool and also
a Python package for you.

## Name
The word *medicure* is combination of *media* and the Latin word *cura*
which means "care".

## Requirements
- [TMDB](https://www.themoviedb.org) API Key: Medicure uses TMDB's API to get
  correct info for movies and TV shows. So you need to create a TMDB account
  and generate an API key inorder to use Medicure.
- [Mediainfo](https://mediaarea.net/en/MediaInfo): Medicure requires Mediainfo
  to extract track info from video and audio files.
- [MKVToolNix](https://mkvtoolnix.download): Medicure uses `mkvmerge` to craete
  new treated media files. `mkvmerge` is one of the MKVToolNix's command-line
  tools

## Installation
The easiest way to install is from PyPI:
```bash
pip install medicure
```
Alternatively, you can install directly from GitHub:
```bash
pip install git+https://github.com/alirezatheh/medicure.git
```

## Simple Example
In this example we want to treat video files of Season 6 of the famous TV show
[Peaky Blinders](https://en.wikipedia.org/wiki/Peaky_Blinders_(TV_series))
downloaded from [PSArips](https://psa.pm).

First we search the name of TV show in [TMDB](https://www.themoviedb.org) to
see season names. In this case season name starts with `Series`. In our
TV shows directory we create `Peaky Blinders/Series 6` directory and put the
files there. directory structure will look like this:
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


Then we run following python script:
```python
from pathlib import Path

from medicure import Medicure, DubbingSupplier

# In this example we only have one dubbing supplier and that's which
# contains original audio and subtitle.
dubbing_suppliers = [
    DubbingSupplier(
        name='original',
        file_id=0,
        correct_language_code='eng',
        audio_language_code='eng',
        subtitle_language_code='eng',
    ),
]

file_search_pattern_to_id = {
    # We have only one file for each episode that can be found by this
    # pattern.
    'PSA': 0,
}
medicure = Medicure(
    tmdb_api_key='YOUR_TMDB_API_KEY',
    tvshows_directory=Path('path/to/tvshows_directory'),
)
medicure.treat_media(
    # You can find this in url of TV show in imdb.
    imdb_id='tt2442560',
    file_search_pattern_to_id=file_search_pattern_to_id,
    video_language_code='eng',
    video_source='PSA',
    video_release_format='WEB-DL',
    dubbing_suppliers=dubbing_suppliers,
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
And each file track info:

| Type     | Title      | Language | Default | Forced |
|----------|------------|----------|---------|--------|
| Video    | PSA WEB-DL | English  | Yes     | No     |
| Audio    |            | English  | Yes     | No     |
| Subtitle |            | English  | No      | No     |

More in depth examples will be coming soon with Medicure's documentation.

### Command-line Interface
Let's treat the above example using Medicure's command-line
interface.

Since we're using CLI for the first time, we need to save our
TMDB API key and TV shows directory locally:
```bash
medicure save tmdb-info YOUR_TMDB_API_KEY
```
```bash
medicure save collection-info \
    --tvshows-directory PATH_TO_YOUR_TVSHOWS_DRIECTORY
```
Now we can run:
```bash
medicure treat media \
    tt2442560 \
    '{"PSA": 0}' \
    eng \
    PSA \
    WEB-DL \
    '[["original", 0, "eng", "eng", "eng"]]' \
    6
```

## Directory Scanning
- TV shows: As showed above Medicure expects following structure for your
  TV shows directory:
  ```bash
  {Your TV shows directory}
  └── {TV show name on TMDB}
      └── {TV show season name on TMDB}
          └── {Episde files}
  ```
- Movies: And for movies directory Medicure expects:
  ```bash
  {You movies directory}
  └── {Movie name on TMDB} - {Movie release year}
      └── {Movie files}
  ```
