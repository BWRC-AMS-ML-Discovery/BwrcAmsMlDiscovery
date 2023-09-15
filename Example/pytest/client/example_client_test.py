from example_client import (
    do_simple_example,
)
from example_shared import (
    Example,
)


def test_example_client():
    res = do_simple_example()
    assert res == Example(txt="HelloHelloHello", num=1)


# def test_example_client_func():
#     def test_func(example) -> Example:
#         return Example(txt="HelloHello", num=1)
#     res = do_example_stuff_func(test_func)
#     assert res == Example(txt="HelloHello", num=1)
