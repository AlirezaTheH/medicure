************
Installation
************

Medicure is a Python package, which means you need to download and install
Python from `python.org <https://www.python.org/downloads>`_ if you haven't
already. Once you have Python installed, you can easily install Medicure from
PyPI:

.. code:: bash

    pip install medicure


Alternatively, you can install directly from GitHub:

.. code:: bash

    pip install git+https://github.com/alirezatheh/medicure.git

Requirements
------------
- `TMDB <https://www.themoviedb.org>`_ API Key: Medicure uses TMDB's API to get
  correct info for movies and TV shows. So you need to create a TMDB account
  and generate an API key in order to use Medicure.
- `Mediainfo <https://mediaarea.net/en/MediaInfo>`_: Medicure requires Mediainfo
  to extract track info from video and audio files.
- `MKVToolNix <https://mkvtoolnix.download>`_: Medicure uses ``mkvmerge`` to craete
  new treated media files. ``mkvmerge`` is one of the MKVToolNix's command-line
  tools.
