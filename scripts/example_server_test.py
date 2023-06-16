from example_server import (
    example_func,
)

from example_shared import (
    example,
    Example,
)


def test_example_server_func_1():
    res = example_func(Example(txt="Hello", num=3))
    assert res == Example(txt="HelloHelloHello", num=1)


def test_example_server_func_2():
    res = example_func(Example(txt="Hello", num=2))
    assert res == Example(txt="HelloHello", num=1)