import json
import platform
import re
from inspect import signature
from pathlib import Path
from typing import Callable, Dict

import typer
from docstring_parser import parse

from medicure.cli.types import DataList, StringListParamType


def get_base_path() -> Path:
    """
    Get base path for Medicure
    """
    os_base_path = {
        'Windows': '~\\AppData\\Local\\Medicure',
        'Darwin': '~/.medicure',
        'Linux': '~/.medicure',
    }
    base_path = Path(os_base_path[platform.system()]).expanduser()
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
            'Hint: You need to save your TMDB info '
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
            'Hint: You need to save your collection info '
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


def create_option(option: str) -> str:
    """
    Creates a CLI option from an option.
    """
    return f'--{option.replace("_", "-")}'


def create_error_message(message: str) -> str:
    """
    Create a CLI error message from a message.
    """

    def replacement(match: re.Match):
        qs = match.group(1)
        if qs == 'True':
            return 'set'
        elif qs.startswith('include'):
            return f'`{create_option(qs)}` flag'
        return f'`{qs.upper()}`'

    return re.sub(r'`([^`]+)`', replacement, message)


def create_cli_text(text: str, cli_function: Callable) -> str:
    """
    Creates a CLI suitable text for a CLI function from a core text.
    """

    def replacement(match: re.Match):
        qs = match.group(1)
        if qs == 'True':
            return 'set'
        elif isinstance(parameters[qs].default, typer.params.OptionInfo):
            flag = ' flag' if parameters[qs].annotation == bool else ''
            return f'`{create_option(qs)}`{flag}'
        return f'`{qs.upper()}`'

    parameters = signature(cli_function).parameters
    return re.sub(r'`([^`]+)`', replacement, text)


def create_helps_from(function: Callable) -> Callable:
    """
    A decorator to create helps for a Typer command's parameters based
    on parameters' descriptions of a function.
    """

    def new_command(command: Callable) -> Callable:
        descriptions = {
            parameter.arg_name: create_cli_text(parameter.description, command)
            for parameter in parse(function.__doc__).params
        }
        for i, parameter in enumerate(signature(command).parameters.values()):
            default_help = ''
            if isinstance(parameter.default.param_type, StringListParamType):
                default_help = (
                    ', you can pass a json-like string for this argument.'
                )
            elif isinstance(parameter.default.param_type, DataList):
                default_help = (
                    ', for each member of this list have you can pass a '
                    'json-like string containing either list of value lists '
                    'or list of dicts of keyword arguments. See the the '
                    'available attributes in `medicure.{}`'.format(
                        parameter.default.param_type.dataclass.__name__,
                    )
                )
            default = command.__defaults__[i]
            default.help = f'{descriptions[parameter.name]}{default_help}'

        return command

    return new_command
