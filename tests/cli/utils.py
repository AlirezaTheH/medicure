from typing import Tuple

from medicure.cli.utils import create_flag


def get_flag_args(flag: bool, flag_name: str) -> Tuple[str, ...]:
    flag_args = (create_flag(flag_name),) if flag else ()
    return flag_args
