import json
from typing import List, Optional, TypeVar, Union

import click
import typer

T = TypeVar('T')


class StringListParamType(click.ParamType):
    """
    Represents a list of strings param type.
    """

    name = 'text_list'

    def convert(
        self,
        value: Union[str, bytes],
        param: click.Parameter,
        ctx: click.Context,
    ) -> List[str]:
        """
        Convert the value to the correct type.
        """
        try:
            json_value = json.loads(value.replace("'", '"'))
            if not isinstance(json_value, list):
                typer.secho(
                    f'Error: Bad JSON value for `{param.human_readable_name}`.'
                    f' `{value!r}` is not a JSON list.',
                    fg='red',
                    err=True,
                )
                raise typer.Exit(code=1)

            return json_value

        except json.JSONDecodeError as e:
            typer.secho(
                f'Error: Bad JSON value for `{param.human_readable_name}`. '
                f'{e}',
                fg='red',
                err=True,
            )
            raise typer.Exit(code=1)


StringList = StringListParamType()


class DataList(click.ParamType):
    """
    Represents a list containing dataclass objects.
    """

    name = 'data_list'

    def __init__(self, dataclass: T) -> None:
        self.dataclass = dataclass

    def convert(
        self,
        value: Union[str, bytes],
        param: click.Parameter,
        ctx: click.Context,
    ) -> Optional[List[T]]:
        """
        Convert the value to the correct type.
        """
        try:
            json_value = json.loads(value.replace("'", '"'))
            if not isinstance(json_value, list):
                typer.secho(
                    f'Error: Bad JSON value for `{param.human_readable_name}`.'
                    f' `{value!r}` is not a JSON list.',
                    fg='red',
                    err=True,
                )
                raise typer.Exit(code=1)

            if len(json_value) > 0:
                if isinstance(json_value[0], list):
                    return [self.dataclass(*data) for data in json_value]
                else:
                    return [self.dataclass(**data) for data in json_value]
            else:
                return json_value

        except json.JSONDecodeError as e:
            typer.secho(
                f'Error: Bad JSON value for `{param.human_readable_name}`. '
                f'{e}',
                fg='red',
                err=True,
            )
            raise typer.Exit(code=1)
