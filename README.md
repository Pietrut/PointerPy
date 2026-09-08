# PointerPy

A lightweight Python library for working with memory pointers and pointer chains.

PointerPy provides an object-oriented interface for resolving pointer chains, reading and writing values, and freezing values in memory.

## Features

* Resolve multi-level pointer chains
* Read values from memory
* Write values to memory
* Freeze values in memory
* Refresh pointer addresses
* Modify pointer configuration at runtime
* Built on top of [PyMem](https://github.com/srounet/Pymem)

## Quick Start

### Example
```python
import pymem

from pointerpy import Pointer

pm = pymem.Pymem("game.exe")

pointer = Pointer(
    pm=pm,
    base=0x12345678,
    offsets=(0x10, 0x20, 0x30),
    data_type="int"
)

print(pointer.value)

pointer.value = 100
```

### Pointer Chains

PointerPy can resolve multi-level pointer chains automatically.

For example, given:

```text
[base]
  ↓ + 0x10
[address]
  ↓ + 0x20
[address]
  ↓ + 0x30
[value]
```

you can represent the chain with:

```python
pointer = Pointer(
    pm=pm,
    base=base,
    offsets=(0x10, 0x20, 0x30),
    data_type="int"
)
```

The final resolved address is available through:

```python
pointer.address
```

## Reading and Writing

The value stored at the resolved address can be accessed through the `value` property:

```python
value = pointer.value
```

Writing works the same way:

```python
pointer.value = 500
```

The `data_type` parameter determines which PyMem read/write functions are used.

For example:

```python
Pointer(
    pm=pm,
    base=base,
    offsets=(0x10,),
    data_type="int"
)
```

uses:

```python
pm.read_int(...)
pm.write_int(...)
```

while:

```python
Pointer(
    pm=pm,
    base=base,
    offsets=(0x10,),
    data_type="float"
)
```

uses:

```python
pm.read_float(...)
pm.write_float(...)
```

Any data type supported by the corresponding PyMem `read_*` and `write_*` methods can be used.

## Refreshing a Pointer

If the pointer chain can change while the program is running, its address can be recalculated with:

```python
pointer.refresh()
```

## Freezing Values

PointerPy can continuously write a value back to memory:

```python
pointer.freeze()
```

If no value is provided, the current value is used:

```python
pointer.freeze()
```

You can also specify the value:

```python
pointer.freeze(100)
```

The pointer can later be unfrozen:

```python
pointer.unfreeze()
```

Its current state can be checked with:

```python
print(pointer.frozen)
```

## Modifying a Pointer

A `Pointer` can be reconfigured after creation using `modify()`:

```python
pointer.modify(
    base=new_base,
    offsets=(0x10, 0x20),
    data_type="float"
)
```

Only the parameters you provide are changed.

The pointer is automatically unfrozen when `modify()` is called.

## Properties

| Property    | Return Type     | Description                              |
| ----------- | --------------- | ---------------------------------------- |
| `pm`        |`Pymem`          | The PyMem process object                 |
| `base`      |`int`            | Base address of the pointer chain        |
| `offsets`   |`tuple[int, ...]`| Pointer-chain offsets                    |
| `data_type` |`str`            | PyMem data type used for reading/writing |
| `address`   |`int`            | Currently resolved memory address        |
| `value`     |`any`            | Value stored at the resolved address     |
| `frozen`    |`bool`           | Whether the pointer is currently frozen  |

## Requirements

* Python 3.10+
* [PyMem](https://github.com/srounet/Pymem)

PointerPy currently relies on PyMem for process memory access.

## License

PointerPy is licensed under the [MIT License](LICENSE).

## Disclaimer

PointerPy is a programming library for interacting with process memory.

Use it only with software and systems you are authorized to inspect or modify.
