import random


__all__ = ("get_random_hex_string_of_length",)


def get_random_hex_string_of_length(length: int):
    """
    Generate a random hexadecimal string of a specified length.

    This function creates a string consisting of randomly selected hexadecimal characters (0-9, a-f).

    Args:
        length (int): The length of the hexadecimal string to be generated.

    Returns:
        str: A string containing random hexadecimal characters of the given length.
    """
    random_range = "0123456789abcdef"
    return "".join(random.choice(random_range) for _ in range(length))  # nosec
