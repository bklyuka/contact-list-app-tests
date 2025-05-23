from dataclasses import dataclass


@dataclass(frozen=True)
class CommonAPIErrors:
    NOT_AUTHENTICATE: str = "Please authenticate."


@dataclass(frozen=True)
class ContactAPIErrors:
    INVALID_ID: str = "Invalid Contact ID"
