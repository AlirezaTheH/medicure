class NoInfoError(Exception):
    """
    No info found.
    """

    msg = (
        'No {name} info found. '
        'You need to save your {name} info '
        'with `save {name_lower}-info` command.'
    )

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.msg.format(name=self.name, name_lower=self.name.lower())
