from typing import Tuple

from medicure.cli.utils import create_option


def get_flag_args(flag: bool, flag_name: str) -> Tuple[str, ...]:
    flag_args = (create_option(flag_name),) if flag else ()
    return flag_args
