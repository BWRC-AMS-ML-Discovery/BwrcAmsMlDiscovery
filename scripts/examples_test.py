from example_server import (
    example_func,
)
from example_client import (
    do_example_stuff,
    do_example_stuff_func,
)

from example_shared import (
    example,
    Example,
)

from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc

def test_example_server_func_1():
    res = example_func(Example(txt="Hello", num=3))
    assert res == Example(txt="HelloHelloHello", num=1)

def test_example_server_func_2():
    res = example_func(Example(txt="Hello", num=2))
    assert res == Example(txt="HelloHello", num=1)

def test_example_client():
    res = do_example_stuff()
    assert res == Example(txt="HelloHelloHello", num=1)

def test_example_client_func():
    def test_func(example) -> Example:
        return Example(txt="HelloHello", num=1)
    
    res = do_example_stuff_func(test_func)
    assert res == Example(txt="HelloHello", num=1)


