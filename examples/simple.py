from winmutex import WindowsMutex

mutex = WindowsMutex("anidev/winmutex/simple", True)  # Name may be any string
mutex.timeout = 2500  # Set a timeout of 2.5 seconds

with mutex:
    print(f"[I] Mutex({mutex}) acquired.")
    input("Enter to release the mutex and exit> ")

print(f"[I] Mutex({mutex}) released. Exiting...")
