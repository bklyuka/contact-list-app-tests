from dataclasses import dataclass


@dataclass(frozen=True)
class CommonAPIErrors:
    NOT_AUTHENTICATE: str = "Please authenticate."
    REQUIRED_PROP: str = "Path `{}` is required."
    INVALID_PROP: str = "{} is invalid"
    MAX_ALLOWED: str = "Path `{}` (`{}`) is longer than the maximum allowed length ({})."


@dataclass(frozen=True)
class ContactAPIErrors:
    INVALID_ID: str = "Invalid Contact ID"
