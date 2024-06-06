import pytest

from main import sum


@pytest.mark.parametrize(
    ('a', 'b', 'result'), [
        (1, 2, 3),
        (-3, 2, -1)
    ],
    ids=['positive', 'negative']
)
def test_sum(a, b, result):
    assert sum(a, b) == result


def test_sum_string():
    assert sum('hello ', 'world') == 'hello world'


def test_sum_string_not_equal():
    assert sum('hello', 'world') != 'hello world'


def test_sum_error():
    with pytest.raises(TypeError):
        sum('hello', 1)
