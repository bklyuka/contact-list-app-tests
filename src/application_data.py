from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class AppData:
    url: str = getenv("URL")
    user_email: str = getenv("TEST_USER_EMAIL")
    user_password: str = getenv("TEST_USER_PASSWORD")


config = AppData()
