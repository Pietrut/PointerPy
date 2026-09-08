import pymem

from .freezer import Freezer
from typing import Any
from collections.abc import Callable

freezer = Freezer()

class Pointer:
    def __init__(self, *, pm: pymem.Pymem, base: int, offsets: tuple[int, ...], data_type: str) -> None:
        self._pm = pm
        self._base = base
        self._offsets = offsets
        self._data_type = data_type
        self._frozen = False

        self._reader, self._writer = self._reader_writer()

        self._address = self._resolve()

    def modify(self, *, pm: pymem.Pymem | None = None, base: int | None = None, offsets: tuple[int, ...] | None = None, data_type: str | None = None) -> None:
        self.unfreeze()

        if pm is not None:
            self._pm = pm

        if base is not None:
            self._base = base

        if offsets is not None:
            self._offsets = offsets

        if data_type is not None:
            self._data_type = data_type
            self._reader, self._writer = self._reader_writer()

        self._address = self._resolve()

    def _reader_writer(self) -> tuple[Callable[[int], Any], Callable[[int, Any], None]]:
        read_name = f"read_{self._data_type}"
        write_name = f"write_{self._data_type}"

        if not hasattr(self._pm, read_name) or not hasattr(self._pm, write_name):
            raise ValueError(f"Unsupported data type: {self._data_type}")   

        return getattr(self._pm, read_name), getattr(self._pm, write_name)

    def _resolve(self) -> int:
        pointer = self._base
        
        for offset in self._offsets:
            pointer = self._pm.read_longlong(pointer) + offset # type: ignore

        return pointer

    def refresh(self) -> None:
        self._address = self._resolve()

    def freeze(self, value=None) -> None:
        freezer.freeze(self, value)

    def unfreeze(self) -> None:
        freezer.unfreeze(self)

    @property
    def pm(self) -> pymem.Pymem:
        return self._pm

    @property
    def base(self) -> int:
        return self._base

    @property
    def offsets(self) -> tuple[int, ...]:
        return self._offsets

    @property
    def data_type(self) -> str:
        return self._data_type

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def address(self) -> int:
        return self._address

    @property
    def value(self) -> Any:
        return self._reader(self.address) 

    @value.setter 
    def value(self, new) -> None:
        self._writer(self.address, new)