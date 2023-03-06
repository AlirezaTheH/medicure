***************
Getting Started
***************
If you are new to Medicure, this is the place to begin. Let's start with a
simple example.

In this example we want to treat
`Peaky Blinders <https://en.wikipedia.org/wiki/Peaky_Blinders_(TV_series)>`_'s
Season 6 video files, downloaded from `PSArips <https://psa.pm>`_.

First we search for the TV show in `TMDB <https://www.themoviedb.org>`_ to see
season names. In this case season name starts with ``Series``. In our TV shows
directory we create ``Peaky Blinders/Series 6`` directory and put the files
there. Directory structure will look like this:

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

And each file has the following track infos:

+----------+-------+--------------+---------+--------+
| Type     | Title | Language     | Default | Forced |
+==========+=======+==============+=========+========+
| Video    |       | Undetermined | Yes     | No     |
+----------+-------+--------------+---------+--------+
| Audio    |       | English      | Yes     | No     |
+----------+-------+--------------+---------+--------+
| Subtitle |       | English      | Yes     | No     |
+----------+-------+--------------+---------+--------+

Now we run the following python snippet:

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

Then directory structure will look like this:

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

And each file track infos:

+----------+------------+----------+---------+--------+
| Type     | Title      | Language | Default | Forced |
+==========+============+==========+=========+========+
| Video    | PSA WEB-DL | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Audio    |            | English  | Yes     | No     |
+----------+------------+----------+---------+--------+
| Subtitle |            | English  | No      | No     |
+----------+------------+----------+---------+--------+

Let's treat again, this time using Medicure's command-line interface.

Since we're using CLI for the first time, we need to save our TMDB API key and
TV shows directory locally:

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

If you want to learn more about Medicure with more in depth examples you can
visit :doc:`Medicure's tutorial <tutorial>`.
