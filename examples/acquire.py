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
