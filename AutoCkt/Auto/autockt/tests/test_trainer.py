from ..trainer import autockt_train


def test():
    assert type(autockt_train) == type(lambda: None)
