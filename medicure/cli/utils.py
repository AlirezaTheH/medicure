import json
import platform
from pathlib import Path
from typing import Dict

import typer


def get_base_path() -> Path:
    """
    Get base path for medicure
    """
    base_path = None

    # Windows
    if platform.system() == 'Windows':
        base_path = Path('~\\AppData\\Local\\Programs\\medicure')
    # macOS
    elif platform.system() == 'Darwin':
        base_path = Path('~/Library/Application Support/medicure͏͏͏͏')
    # Linux
    elif platform.system() == 'Linux':
        base_path = Path('~/.config/medicure')

    base_path = base_path.expanduser()
    if not base_path.exists():
        base_path.mkdir()

    return base_path


def load_tmdb_info() -> Dict[str, str]:
    """
    Loads TMDB info from disk
    """
    info_path = get_base_path() / 'tmdb_info.json'
    if not info_path.exists():
        typer.secho('Error: No TMDB info found.', err=True, fg='red')
        typer.secho(
            'You need to save your TMDB info '
            'with `medicure save tmdb-info` command.',
            fg='blue',
        )
        raise typer.Exit(code=1)

    with open(info_path) as f:
        info = json.load(f)

    return info


def load_collection_info() -> Dict[str, Path]:
    """
    Loads collection info from disk.
    """
    info_path = get_base_path() / 'collection_info.json'
    if not info_path.exists():
        typer.secho('Error: No collection info found.', err=True, fg='red')
        typer.secho(
            'You need to save your collection info '
            'with `medicure save collection-info` command.',
            fg='blue',
        )
        raise typer.Exit(code=1)

    with open(info_path) as f:
        info = json.load(f, object_hook=collection_info_from_json)

    return info


def collection_info_from_json(json_object: Dict[str, str]) -> Dict[str, Path]:
    """
    A from_json function for collection info
    """
    return {k: Path(v) for k, v in json_object.items()}


def create_help(*lines: str) -> str:
    """
    Creates a beautiful help message for typer.
    """
    return '\b\n\b\n{}\n'.format('\n'.join(lines))
