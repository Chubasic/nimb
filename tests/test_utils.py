"""
Utils unit tests
"""

from utils.skip_none import dict_skip_none


def test_no_none_values():
    """
    Test function for the `dict_skip_none` function.
    """
    params = {"a": 1, "b": 2, "c": 3}
    expected_result = {"a": 1, "b": 2, "c": 3}
    assert dict_skip_none(params) == expected_result


def test_some_none_values():
    """
    Test function for the `dict_skip_none` function.
    """
    params = {"a": 1, "b": None, "c": 3}
    expected_result = {"a": 1, "c": 3}
    assert dict_skip_none(params) == expected_result


def test_all_none_values():
    """
    Test function for the `dict_skip_none` function.
    """
    params = {"a": None, "b": None, "c": None}
    expected_result = {}
    assert dict_skip_none(params) == expected_result


def test_empty_dict():
    """
    Test function for the `dict_skip_none` function.
    """
    params = {}
    expected_result = {}
    assert dict_skip_none(params) == expected_result
