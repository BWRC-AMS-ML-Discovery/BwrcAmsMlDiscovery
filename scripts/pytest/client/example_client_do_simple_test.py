from example_client import (
    do_simple_example,
)
from example_shared import (
    Example,
)


def test_example_client():
    res = do_simple_example()
    print(res)

    assert res == Example(txt="HelloHelloHello", num=1)
