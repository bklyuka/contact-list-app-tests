from dataclasses import dataclass, field

from src.faker_provider import faker
from src.helpers import get_random_string


@dataclass
class CreateUser:
    firstName: str = field(default_factory=get_random_string)
    lastName: str = field(default_factory=get_random_string)
    email: str = field(default_factory=faker.email)
    password: str = field(default_factory=lambda: get_random_string(length=7))
