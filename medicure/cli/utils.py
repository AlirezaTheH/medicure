import json
import os
import platform
from os import path
from typing import Dict

from medicure.cli.exceptions import NoInfoError


def get_base_path() -> str:
    """
    Get base path for medicure
    """
    base_path = None
    user_path = path.expanduser('~')

    # Windows
    if platform.system() == 'Windows':
        base_path = path.join(user_path, 'AppData\\Local\\Programs\\medicure')
    # macOS
    elif platform.system() == 'Darwin':
        base_path = path.join(
            user_path, 'Library/Application Support/medicure͏͏͏͏'
        )
    # Linux
    elif platform.system() == 'Linux':
        base_path = path.join(user_path, '.config/medicure')

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    return base_path


def load_tmdb_info() -> Dict[str, str]:
    """
    Loads TMDB info from disk
    """
    info_path = path.join(get_base_path(), 'tmdb_info.json')
    if not path.exists(info_path):
        raise NoInfoError('TMDB')

    with open(info_path) as f:
        info = json.load(f)

    return info


def load_collection_info() -> Dict[str, str]:
    """
    Loads collection info from disk.
    """
    info_path = path.join(get_base_path(), 'collection_info.json')
    if not path.exists(info_path):
        raise NoInfoError('collection')

    with open(info_path) as f:
        info = json.load(f)

    return info
