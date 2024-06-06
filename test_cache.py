import logging

import pytest

from main import cache


@pytest.fixture()
def cache_size():
    return 10


def test_cache_get_from_cache_by_logs(caplog, cache_size):
    caplog.set_level(logging.INFO)

    storage = {}

    @cache(storage, cache_size=cache_size)
    def sub(a, b):
        return a - b

    sub(1, 2)
    sub(1, 2)

    logs = caplog.messages
    assert logs[0] == 'Computing result'
    assert 'Retrieving from cache:' in logs[1]


def test_cache_get_from_cache(cache_size):
    storage = {}

    @cache(storage, cache_size=cache_size)
    def sub(a, b):
        return a - b

    result = sub(1, 2)
    assert storage['sub(1, 2)'].value == result


def test_cache_test_max_len():
    storage = {}

    cache_size_ = 2

    @cache(storage, cache_size=cache_size_)
    def sub(a, b):
        return a - b

    for i in range(5):
        sub(i, 2)
        assert len(storage) <= cache_size_
