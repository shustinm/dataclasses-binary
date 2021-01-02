from dataclasses import dataclass, fields
from hydration import *
from struct import pack
import abc


class DataClassBinaryMixin(abc.ABC):

    def serialize(self):

        # noinspection PyDataclass
        # fields(self)
        return b''.join(pack('L', getattr(self, f.name)) for f in fields(self))

    def __bytes__(self):
        return self.serialize()


def dataclass_binary(_cls=None):

    def wrap(cls) -> DataClassBinaryMixin:
        return _process_class(cls)

    if _cls is None:
        return wrap

    return wrap(_cls)


def _process_class(cls) -> DataClassBinaryMixin:
    cls.serialize = DataClassBinaryMixin.serialize
    cls.__bytes__ = DataClassBinaryMixin.__bytes__
    return cls


@dataclass_binary
@dataclass
class Point:
    x: int
    y: int


if __name__ == '__main__':
    p = Point(3, 5)
    # noinspection PyTypeChecker
    print(bytes(p))


