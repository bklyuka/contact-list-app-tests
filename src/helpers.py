import random
import string


def get_random_bool() -> bool:
    return bool(random.getrandbits(1))


def get_random_string(length: int = 10) -> str:
    characters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choices(characters, k=length))
