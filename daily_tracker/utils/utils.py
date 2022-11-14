"""
Utilities to use throughout the scripts.
"""


def comma_list_to_list(comma_list: str) -> list:
    """
    Convert a string comma-separator list to a Python list.
    """
    return [category.strip() for category in comma_list.split(",")] if comma_list else []
