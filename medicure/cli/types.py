import json
from typing import Any, Dict, List, Optional, TypeVar, Union

import click

T = TypeVar('T')


class JsonParamType(click.ParamType):
    """
    Represents json type.
    """

    name = 'json'

    def convert(
        self,
        value: Optional[Union[Dict[Any, Any], str, bytes]],
        param: click.Parameter,
        ctx: click.Context,
    ) -> Optional[Dict[Any, Any]]:
        """
        Convert the value to the correct type.
        """
        try:
            if isinstance(value, (str, bytes)):
                return json.loads(value)
            else:
                self.fail(
                    f'{value!r} was not a `str`, `bytes` or `None`.',
                    param,
                    ctx,
                )
        except OSError as e:
            self.fail([*e.args, None][0], param, ctx)
        except json.JSONDecodeError as e:
            self.fail(f'Bad JSON: {[*e.args, None][0]}', param, ctx)


Json = JsonParamType()


class DataList(click.ParamType):
    """
    Represents a list containing dataclass objects.
    """

    name = 'dataclass'

    def __init__(self, dataclass: T) -> None:
        self.dataclass = dataclass

    def convert(
        self,
        value: Optional[
            Union[List[Dict[str, Any]], List[List[Any]], str, bytes]
        ],
        param: click.Parameter,
        ctx: click.Context,
    ) -> Optional[List[T]]:
        """
        Convert the value to the correct type.
        """
        try:
            if isinstance(value, (str, bytes)):
                json_value = json.loads(value)
                if isinstance(json_value[0], list):
                    return [self.dataclass(*data) for data in json_value]
                else:
                    return [self.dataclass(**data) for data in json_value]
            else:
                self.fail(
                    f'{value!r} was not a `str`, `bytes` or `None`.',
                    param,
                    ctx,
                )
        except OSError as e:
            self.fail([*e.args, None][0], param, ctx)
        except json.JSONDecodeError as e:
            self.fail(f'Bad JSON: {[*e.args, None][0]}', param, ctx)
