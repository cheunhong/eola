from contextlib import contextmanager

from sqlglot import parse


class Connection:
    pass


@contextmanager
def connect():
    yield
