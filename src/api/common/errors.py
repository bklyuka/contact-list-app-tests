from dataclasses import dataclass


@dataclass(frozen=True)
class CommonAPIErrors:
    NOT_AUTHENTICATE: str = "Please authenticate."
