from random import getrandbits, choices, randint
from string import ascii_lowercase, ascii_uppercase


def get_random_bool() -> bool:
    return bool(getrandbits(1))


def get_random_string(length: int = 10) -> str:
    characters = ascii_lowercase + ascii_uppercase
    return "".join(choices(characters, k=length))


def get_random_int(start: int = 0, end: int = 999999999) -> int:
    return randint(start, end)


def get_fake_id() -> str:
    return "".join(choices("0123456789abcdef", k=24))
