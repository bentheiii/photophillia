from contextlib import contextmanager
from io import TextIOWrapper
from typing import Callable, Any
from zipfile import ZipFile, ZIP_DEFLATED


@contextmanager
def open_zipped(path, file, mode):
    with ZipFile(path, mode=mode, compression=ZIP_DEFLATED) as zipped:
        with zipped.open(file, mode) as op:
            with TextIOWrapper(op, 'utf-8') as tio:
                yield tio


def remove_where(x: set, predicate: Callable[[Any], bool]):
    x.difference_update([i for i in x if predicate(i)])
