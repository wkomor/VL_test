# It's not clear whether the function should return bool or comparison diff.
# Assume, that we have mypy and input params have correct format
# The order in lists matters
import math
from typing import Any

FLOAT_COMPARISON_PRECISION = 0.00001


def compare(item1: Any, item2: Any) -> bool:
    if type(item1) != type(item2):
        return False
    if isinstance(item1, dict):
        return is_jsons_equal(item1, item2)
    if isinstance(item1, float):
        return math.isclose(item1, item2, abs_tol=FLOAT_COMPARISON_PRECISION)
    return item1 == item2


def is_jsons_equal(first_json: dict, second_json: dict) -> bool:
    if not first_json and not second_json:
        return True
    if first_json.keys() != second_json.keys():
        return False
    for key, val in first_json.items():
        if not compare(val, second_json[key]):
            return False
    return True
