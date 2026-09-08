from __future__ import annotations
from typing import TYPE_CHECKING, Any

import threading, time

if TYPE_CHECKING:
    from .pointer import Pointer

class Freezer:
    def __init__(self, interval: float = 0.025) -> None:
        self._pointers: dict[Pointer, Any] = {}
        self._lock = threading.Lock()
        self._interval = interval

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def freeze(self, pointer: Pointer, value: Any | None = None) -> None:
        if value is None:
            value = pointer.value

        with self._lock:
            self._pointers[pointer] = value
            
        pointer._frozen = True

    def unfreeze(self, pointer: Pointer) -> None:
        with self._lock:
            self._pointers.pop(pointer, None)

        pointer._frozen = False

    def _loop(self) -> None:
        while True:
            with self._lock:
                items = list(self._pointers.items())

            for pointer, value in items:
                try:
                    pointer.value = value
                except Exception:
                    raise Exception

            time.sleep(self._interval)