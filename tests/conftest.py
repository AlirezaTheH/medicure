import shutil

import pytest
import tmdbsimple as tmdb

from tests.parameterize import *
from tests.tmdb_mocks import FindMock, TVSeasonsMock


@pytest.fixture(autouse=True)
def mock_tmdb(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(tmdb, 'Find', FindMock)
    monkeypatch.setattr(tmdb, 'TV_Seasons', TVSeasonsMock)


@pytest.fixture(autouse=True)
def clean_data_directory() -> None:
    yield

    for directory in movies_directory.iterdir():
        if directory.name.endswith('Edited'):
            shutil.rmtree(directory)

    for directory in tvshows_directory.iterdir():
        if directory.is_dir():
            for sub_directory in directory.iterdir():
                if sub_directory.name.endswith('Edited'):
                    shutil.rmtree(sub_directory)
