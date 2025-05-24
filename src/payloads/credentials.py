from dataclasses import dataclass, field

from src.helpers import get_random_string, get_fake_email


@dataclass
class Credentials:
    email: str = field(default_factory=get_fake_email)
    password: str = field(default_factory=get_random_string)
