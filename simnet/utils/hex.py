import random


def get_random_hex_string_of_length(length: int):
    random_range = "0123456789abcdef"
    return ''.join(random.choice(random_range) for _ in range(length))  # nosec
