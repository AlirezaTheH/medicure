import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def tmdb_api_key() -> str:
    return os.environ['TMDB_API_KEY']


@pytest.fixture(scope='session')
def movies_directory() -> Path:
    return Path(__file__).parent / 'data' / 'Movies'


@pytest.fixture(scope='session')
def tvshows_directory() -> Path:
    return Path(__file__).parent / 'data' / 'TV Shows'


@pytest.fixture(autouse=True)
def clean_data_directory(
    movies_directory: Path, tvshows_directory: Path
) -> None:
    yield

    for directory in movies_directory.iterdir():
        if directory.name.endswith('Edited'):
            shutil.rmtree(directory)

    for directory in tvshows_directory.iterdir():
        if directory.is_dir():
            for sub_directory in directory.iterdir():
                if sub_directory.name.endswith('Edited'):
                    shutil.rmtree(sub_directory)
