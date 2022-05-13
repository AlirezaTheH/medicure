import re
from pathlib import Path


def extract_episode_number(file_name: Path) -> int:
    """
    Extracts episode number from file name
    """
    for pattern in (r'(?<=[xXeE])\d{2}', r'\d{1,2}'):
        match = re.search(pattern, str(file_name))
        if match is not None:
            episode_number = int(match.group())
            return episode_number

    raise ValueError('File name did not match to any pattern.')


def escape_nonpath_characters(string: str) -> str:
    """
    Escapes all non-path characters from a string.
    """
    return string.translate(str.maketrans(':/', '  '))
