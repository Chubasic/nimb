"""
Filter out None values from the dictionary
"""


def dict_skip_none(params) -> str:
    """
    Filter out None values from the dictionary.

    :param params: A dictionary containing key-value pairs.
    :return: A new dictionary with the same key-value pairs as the
    input dictionary, but without any values that are None.
    """
    filtered_params = {key: value for key, value in params.items() if value is not None}

    return filtered_params
