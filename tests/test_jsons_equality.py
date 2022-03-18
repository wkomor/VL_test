import pytest
from jsons_equality import compare, is_jsons_equal


@pytest.mark.parametrize(
    ['item1', 'item2', 'result'],
    [
        pytest.param(1, 1, True),
        pytest.param(1, 2, False),
        pytest.param(1, '1', False),
        pytest.param([1, 2], [1, 2], True),
        pytest.param([1, 2], [2, 1], False),
        pytest.param('str', 'str', True),
        pytest.param(1.12345, 1.12345, True),
        pytest.param(1.123456, 1.123457, True),
        pytest.param(1.12345, 1.12344, False),
        pytest.param({'a': 1}, {'a': 1}, True),
    ]
)
def test_compare(item1, item2, result):
    assert compare(item1, item2) == result


@pytest.mark.parametrize(
    ['json1', 'json2', 'result'],
    [
        pytest.param({}, {}, True),
        pytest.param({'a': 1}, {'b': 1}, False),
        pytest.param({'a': 1}, {'b': 1}, False),
        pytest.param({'a': {'b': 2}}, {'a': {'b': 2}}, True),
        pytest.param({'a': {'b': 2}}, {'a': {'b': 3}}, False),
    ]
)
def test_is_jsons_equal(json1, json2, result) -> None:
    assert is_jsons_equal(json1, json2) == result
