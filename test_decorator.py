from functools import wraps

import pytest
from decorator import decorator


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


cd_parametrize = pytest.mark.parametrize(
    'c,d', [('c', 'd'), ('C', 'D')], ids='low upper'.split())


@cd_parametrize
@regular_decorator('foo', 'bar')
def test_regular_decorator(a, b, c, d):
    assert ('a', 'b', 'c'.capitalize(), 'd'.capitalize()) == (
        a, b, c.capitalize(), d.capitalize())


def lib_decorator(foo, bar):
    @decorator
    def wrapper(func, *args, **kwargs):
        print(foo, bar)
        return func(*args, **kwargs)

    return wrapper


@cd_parametrize
@lib_decorator('foo', 'bar')
def test_lib_decorator(a, b, c, d):
    assert ('a', 'b', 'c'.capitalize(), 'd'.capitalize()) == (
        a, b, c.capitalize(), d.capitalize())
