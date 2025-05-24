from dataclasses import dataclass, field
from typing import Optional

from src.helpers import get_random_string
from src.payloads import LoginCredentials


@dataclass
class CreateUser:
    firstName: str = field(default_factory=get_random_string)
    lastName: str = field(default_factory=get_random_string)
    email: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self):
        if self.email is None or self.password is None:
            creds: LoginCredentials = LoginCredentials()
            self.email: str = self.email or creds.email
            self.password: str = self.password or creds.password
