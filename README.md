# pywinmutex

A simple Python library to create and manage Windows mutexes.

## Installation

You can install the library using pip:

```bash
pip install pywinmutex
```

## Usage

### Basic Example
```python
from pywinmutex import WindowsMutex

mutex = WindowsMutex("anidev/pywinmutex/simple", True)  # Name may be any string
mutex.timeout = 2500  # Set a timeout of 2.5 seconds

with mutex:
    print(f"[I] Mutex({mutex}) acquired.")
    input("Enter to release the mutex and exit> ")

print(f"[I] Mutex({mutex}) released. Exiting...")
```

### Legacy
```python
from pywinmutex import WindowsMutex

mutex = WindowsMutex("anidev/pywinmutex/acquire", True)  # Name may be any string

if not mutex.acquire(5000):  # Acquire the mutex with a timeout of 5 seconds; None for no timeout
    print(f"[W] Mutex({mutex}) already exists or acquire timeout exceeded.")
    exit(1)

# Do some work while holding the mutex

print(f"[I] Mutex({mutex}) acquired.")
input("Enter to release the mutex and exit> ")

# Release the mutex
mutex.release()
print(f"[I] Mutex({mutex}) released. Exiting...")
```

## License

This project is licensed under the `MIT License`. See the [LICENSE](LICENSE) file for details.
