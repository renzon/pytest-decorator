from functools import wraps

import pytest


def regular_decorator(foo, bar):
    print(foo, bar)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.fixture
def a():
    return 'a'


@pytest.fixture
def b():
    return 'b'


@pytest.mark.parametrize('c,d', [('c', 'd')])
@regular_decorator('foo', 'bar')
def test_regular_decorator(a, b, c, d):
    assert ('a', 'b', 'c', 'd') == (a, b, c, d)
