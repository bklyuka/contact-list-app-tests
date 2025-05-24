from dataclasses import dataclass, field

from src.faker_provider import faker
from src.helpers import get_random_string, get_random_int


@dataclass
class CreateUpdateContact:
    firstName: str = field(default_factory=get_random_string)
    lastName: str = field(default_factory=get_random_string)
    email: str = field(default_factory=faker.email)
    birthdate: str = field(default_factory=lambda: faker.date_of_birth().strftime("%Y-%m-%d"))
    phone: str = field(default_factory=lambda: str(get_random_int()))
    street1: str = field(default_factory=faker.street_address)
    street2: str = field(default_factory=get_random_string)
    city: str = field(default_factory=faker.city)
    stateProvince: str = field(default_factory=faker.state_abbr)
    postalCode: str = field(default_factory=faker.postcode)
    country: str = field(default_factory=faker.country)
