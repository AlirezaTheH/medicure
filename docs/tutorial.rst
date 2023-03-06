********
Tutorial
********
Let's find out how Medicure works.


Functionality
=============
Medicure provides two similar API for treating media and subtitle files.

1. Treat Media API
------------------
This API:

1. Takes and IMDb id (and a season number for TV show).
2. Scans your collection to find given movie or TV show files based on given
   ``file_search_patterns`` parameter.
3. Extracts files tracks based on given ``dubbing_suppliers``.
4. Properly sorts tracks and correct their infos.
5. And finally creates a new treated file.

Usage Notes
^^^^^^^^^^^
The key to get desired treated output is proper configuration of
``file_search_patterns`` and ``dubbing_suppliers``. To properly configure this
parameters always consider following notes:

- If your treatment contains multiple files (video, audio or subtitle) per
  movie or episode, first pattern in ``file_search_patterns`` should always
  match the file that you want select video from.
- The order in ``dubbing_suppliers`` matters. It determines track order in
  final treated file.
- The ``file_id`` in each ``DubbingSupplier`` is the index of pattern in
  ``file_search_patterns`` which its file contains dubbing supplier tracks.
- An audio track in a file matches with a ``DubbingSupplier`` if only:

  1. ``file_id`` matches with ``DubbingSupplier``'s ``file_id``
  2. Track's language code matches with ``DubbingSupplier``'s
     ``audio_language_code`` and track's title matches with
     ``DubbingSupplier``'s ``audio_search_pattern``.
- A subtitle track in a file matches with a ``DubbingSupplier`` if only:

  1. ``file_id`` matches with ``DubbingSupplier``'s ``file_id``
  2. Track's language code matches with ``DubbingSupplier``'s
     ``subtitle_language_code`` and track's title matches with
     ``DubbingSupplier``'s ``subtitle_search_pattern``.

2. Treat Subtitle API
---------------------
This API:

1. Takes and IMDb id (and a season number for TV show).
2. Scans your collection to find given movie or TV show files based on given
   ``file_search_patterns`` parameter.
3. And finally creates a new treated file based on given
   ``include_full_information`` flag. If this flag is set an ``.mks`` file
   will be generated to include all subtitle information, otherwise API keeps
   the current file suffix and just renames the file properly.

Directory Scanning
==================
- TV shows: Medicure expects following structure for your TV shows directory:

  .. code:: bash

      {Your TV shows directory}
      └── {TV show name on TMDB}
          └── {TV show season name on TMDB}
              └── {Episde files}

- Movies: And for movies directory Medicure expects:

  .. code:: bash

      {You movies directory}
      └── {Movie name on TMDB} - {Movie release year}
          └── {Movie files}

Examples
========
Now see some treat examples together.

Treat Media API
---------------

Single Video File
^^^^^^^^^^^^^^^^^
In this example we want to treat video files of Season 6 of the famous TV show
`Peaky Blinders <https://en.wikipedia.org/wiki/Peaky_Blinders_(TV_series)>`_
downloaded from `PSArips <https://psa.pm>`_.

First we search for the TV show in `TMDB <https://www.themoviedb.org>`_ to
see season names. In this case season name starts with ``Series``. In our
TV shows directory we create ``Peaky Blinders/Series 6`` directory and put the
files there.

Initial Directory Structure
"""""""""""""""""""""""""""
.. code:: bash

    TV Shows
    └── Peaky Blinders
        └── Series 6
            ├── Peaky.Blinders.S06E01.1080p.10bit.WEB-DL.x265.HEVC.PSA.AM.mkv
            ├── Peaky.Blinders.S06E02.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E03.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E04.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E05.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            └── Peaky.Blinders.S06E06.1080p.10bit.WEB-DL.x265.PSA.AM.mkv

Initial File Track Infos
""""""""""""""""""""""""
+----------+-------+--------------+---------+--------+
| Type     | Title | Language     | Default | Forced |
+==========+=======+==============+=========+========+
| Video    |       | Undetermined | Yes     | No     |
+----------+-------+--------------+---------+--------+
| Audio    |       | English      | Yes     | No     |
+----------+-------+--------------+---------+--------+
| Subtitle |       | English      | Yes     | No     |
+----------+-------+--------------+---------+--------+

Python Snippet
""""""""""""""
.. code:: python

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

CLI Command
"""""""""""
Since we're using CLI for the first time, we need to save our
TMDB API key and TV shows directory locally:

.. code:: bash

    medicure save tmdb-info YOUR_TMDB_API_KEY

.. code:: bash

    medicure save collection-info \
    --tvshows-directory PATH_TO_YOUR_TVSHOWS_DIRECTORY

Now we can run:

.. code:: bash

    medicure treat media \
    tt2442560 \
    '["PSA"]' \
    eng \
    PSA \
    WEB-DL \
    '[["original", 0, "eng", "eng", "eng"]]' \
    6

Final Directory Structure
"""""""""""""""""""""""""
.. code:: bash

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

Edited File Tracks Info
"""""""""""""""""""""""
+----------+------------+----------+---------+--------+
| Type     | Title      | Language | Default | Forced |
+==========+============+==========+=========+========+
| Video    | PSA WEB-DL | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Audio    |            | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Subtitle |            | English  | No      | No     |
+----------+------------+----------+---------+--------+

An Extra Audio File
^^^^^^^^^^^^^^^^^^^
Let's dig a little bit deeper and add an extra audio file for each episode
which contains Persian dubbed audio for our TV show.

Initial Directory Structure
"""""""""""""""""""""""""""
.. code:: bash

    TV Shows
    └── Peaky Blinders
        └── Series 6
            ├── Peaky.Blinders.S06E01.1080p.10bit.WEB-DL.x265.HEVC.PSA.AM.mkv
            ├── Peaky.Blinders.S06E01.Farsi.Dubbed.Audio.TinyMoviez.mka
            ├── Peaky.Blinders.S06E02.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E02.Farsi.Dubbed.Audio.TinyMoviez.mka
            ├── Peaky.Blinders.S06E03.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E03.Farsi.Dubbed.Audio.TinyMoviez.mka
            ├── Peaky.Blinders.S06E04.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E04.Farsi.Dubbed.Audio.TinyMoviez.mka
            ├── Peaky.Blinders.S06E05.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            ├── Peaky.Blinders.S06E05.Farsi.Dubbed.Audio.TinyMoviez.mka
            ├── Peaky.Blinders.S06E06.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
            └── Peaky.Blinders.S06E06.Farsi.Dubbed.Audio.TinyMoviez.mka

Initial File Track Infos
""""""""""""""""""""""""
+----------+---------------+--------------+---------+--------+
| Type     | Title         | Language     | Default | Forced |
+==========+===============+==============+=========+========+
| Audio    | TinyMoviez.co | Undetermined | Yes     | No     |
+----------+---------------+--------------+---------+--------+

Python Snippet
""""""""""""""
.. code:: python

    medicure.treat_media(
        imdb_id='tt2442560',
        file_search_patterns=['PSA', 'TinyMoviez'],
        video_language_code='eng',
        video_source='PSA',
        video_release_format='WEB-DL',
        dubbing_suppliers=[
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
                audio_search_pattern=r'TinyMoviez',
            ),
        ],
        season_number=6,
    )

CLI Command
"""""""""""
.. code:: bash

    medicure treat media \
    tt2442560 \
    '["PSA", "TinyMoviez"]' \
    eng \
    PSA \
    WEB-DL \
    '[["original", 0, "eng", "eng", "eng"], ["TinyMoviez", 1, "per", null, null, "TinyMoviez"]]' \
    6

Final Directory Structure
"""""""""""""""""""""""""
.. code:: bash

    TV Shows
    └── Peaky Blinders
        ├── Series 6
        │   ├── Peaky.Blinders.S06E01.1080p.10bit.WEB-DL.x265.HEVC.PSA.AM.mkv
        │   ├── Peaky.Blinders.S06E01.Farsi.Dubbed.Audio.TinyMoviez.mka
        │   ├── Peaky.Blinders.S06E02.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        │   ├── Peaky.Blinders.S06E02.Farsi.Dubbed.Audio.TinyMoviez.mka
        │   ├── Peaky.Blinders.S06E03.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        │   ├── Peaky.Blinders.S06E03.Farsi.Dubbed.Audio.TinyMoviez.mka
        │   ├── Peaky.Blinders.S06E04.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        │   ├── Peaky.Blinders.S06E04.Farsi.Dubbed.Audio.TinyMoviez.mka
        │   ├── Peaky.Blinders.S06E05.INTERNAL.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        │   ├── Peaky.Blinders.S06E05.Farsi.Dubbed.Audio.TinyMoviez.mka
        │   ├── Peaky.Blinders.S06E06.1080p.10bit.WEB-DL.x265.PSA.AM.mkv
        │   └── Peaky.Blinders.S06E06.Farsi.Dubbed.Audio.TinyMoviez.mka
        └── Series 6 Edited
            ├── Peaky Blinders - S06E01 - Black Day.mkv
            ├── Peaky Blinders - S06E02 - Black Shirt.mkv
            ├── Peaky Blinders - S06E03 - Gold.mkv
            ├── Peaky Blinders - S06E04 - Sapphire.mkv
            ├── Peaky Blinders - S06E05 - The Road to Hell.mkv
            └── Peaky Blinders - S06E06 - Lock and Key.mkv

Edited File Track Infos
"""""""""""""""""""""""
+----------+------------+----------+---------+--------+
| Type     | Title      | Language | Default | Forced |
+==========+============+==========+=========+========+
| Video    | PSA WEB-DL | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Audio    |            | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Audio    | TinyMoviez | Persian  | No      | No     |
+----------+------------+----------+---------+--------+
| Subtitle |            | English  | No      | No     |
+----------+------------+----------+---------+--------+


Treat Subtitle API
------------------

Single Subtitle File
^^^^^^^^^^^^^^^^^^^^
Let's add some Persian subtitle files for our TV show and treat them
separately.

Initial Directory Structure
"""""""""""""""""""""""""""
.. code:: bash

    TV Shows
    └── Peaky Blinders
        └── Series 6
            ├── [For TV].Peaky.Blinders.S06E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
            ├── [For TV].Peaky.Blinders.S06E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
            ├── [For TV].Peaky.Blinders.S06E03.Gold.720p.iP.WEB-DL.AAC2.0.H264-FLUX + PSA (INTERNAL).srt
            ├── [For TV].Peaky.Blinders.S06E04.Sapphire.720p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
            ├── [For TV].Peaky.Blinders.S06E05.The.Road.to.Hell.1080p.iP.WEB-DL.AAC2.0.H.264-FLUX + PSA (INTERNAL).srt
            └── [For TV].Peaky.Blinders.S06E06.Lock.and.Key.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt

Python Snippet
""""""""""""""
For treating subtitle files we have two options:

.. _first_option:

1. Keep the current files format:

   .. code:: python

       medicure.treat_subtitle(
           imdb_id='tt2442560',
           file_search_patterns=['For TV'],
           language_code='per',
           season_number=6,
       )

.. _second_option:

2. Convert files to ``.mks`` format to include all information:

   .. code:: python

       medicure.treat_subtitle(
           imdb_id='tt2442560',
           file_search_patterns=['For TV'],
           video_language_code='per',
           video_source='TinyMoviez',
           release_format='WEB-DL',
           include_full_information=True,
           season_number=6,
       )


CLI Command
"""""""""""
1. :ref:`First option<first_option>`:

   .. code:: bash

       medicure treat subtitle tt2442560 '["For TV"]' per 6

2. :ref:`Second option<second_option>`:

   .. code:: bash

       medicure treat subtitle \
       tt2442560 \
       '["For TV"]' \
       per \
       TinyMoviez \
       WEB-DL \
       6 \
       --include-full-information

Final Directory Structure
"""""""""""""""""""""""""
1. :ref:`First option<first_option>`:

   .. code:: bash

       TV Shows
       └── Peaky Blinders
           ├── Series 6
           │   ├── [For TV].Peaky.Blinders.S06E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E03.Gold.720p.iP.WEB-DL.AAC2.0.H264-FLUX + PSA (INTERNAL).srt
           │   ├── [For TV].Peaky.Blinders.S06E04.Sapphire.720p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E05.The.Road.to.Hell.1080p.iP.WEB-DL.AAC2.0.H.264-FLUX + PSA (INTERNAL).srt
           │   └── [For TV].Peaky.Blinders.S06E06.Lock.and.Key.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           └── Series 6 Edited
               ├── Peaky Blinders - S06E01 - Black Day.per.srt
               ├── Peaky Blinders - S06E02 - Black Shirt.per.srt
               ├── Peaky Blinders - S06E03 - Gold.per.srt
               ├── Peaky Blinders - S06E04 - Sapphire.per.srt
               ├── Peaky Blinders - S06E05 - The Road to Hell.per.srt
               └── Peaky Blinders - S06E06 - Lock and Key.per.srt

2. :ref:`Second option<second_option>`:

   .. code:: bash

       TV Shows
       └── Peaky Blinders
           ├── Series 6
           │   ├── [For TV].Peaky.Blinders.S06E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E03.Gold.720p.iP.WEB-DL.AAC2.0.H264-FLUX + PSA (INTERNAL).srt
           │   ├── [For TV].Peaky.Blinders.S06E04.Sapphire.720p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           │   ├── [For TV].Peaky.Blinders.S06E05.The.Road.to.Hell.1080p.iP.WEB-DL.AAC2.0.H.264-FLUX + PSA (INTERNAL).srt
           │   └── [For TV].Peaky.Blinders.S06E06.Lock.and.Key.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX + PSA + Pahe.srt
           └── Series 6 Edited
               ├── Peaky Blinders - S06E01 - Black Day.per.mks
               ├── Peaky Blinders - S06E02 - Black Shirt.per.mks
               ├── Peaky Blinders - S06E03 - Gold.per.mks
               ├── Peaky Blinders - S06E04 - Sapphire.per.mks
               ├── Peaky Blinders - S06E05 - The Road to Hell.per.mks
               └── Peaky Blinders - S06E06 - Lock and Key.per.mks

Edited File Track Infos
"""""""""""""""""""""""
2. :ref:`Second option<second_option>`:

   +------+-------------------+----------+---------+--------+
   | Type | Title             | Language | Default | Forced |
   +======+===================+==========+=========+========+
   | Text | TinyMoviez WEB-DL | Persian  | Yes     | No     |
   +------+-------------------+----------+---------+--------+
