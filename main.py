from winmutex import WindowsMutex

mutex_name = "anidev.myapp.mutex.{}"  # Name constructor
mutex = WindowsMutex(mutex_name.format(0), True)

# [W] Mutex(<WindowsMutex(name='anidev.myapp.mutex.0', multiuser=True)>) already exists. Reinitializing mutex with a new name: 'anidev.myapp.mutex.1'
# [W] Mutex(<WindowsMutex(name='anidev.myapp.mutex.1', multiuser=True)>) already exists. Reinitializing mutex with a new name: 'anidev.myapp.mutex.2'
# [I] Mutex(<WindowsMutex(name='anidev.myapp.mutex.2', multiuser=True)>) acquired. Running the application...
# Enter to release the mutex and exit>
# Mutex released. Exiting...

def find_index():
    index = 0
    while True:
        index += 1
        if mutex.exist:
            print(f"[W] Mutex({mutex}) already exists. Reinitializing mutex with a new name: {mutex_name.format(index)!r}")
            mutex.reinint(mutex_name.format(index))
        else:
            break

def main():
    with mutex:
        print(f"[I] Mutex({mutex}) acquired. Running the application...")
        input("Enter to release the mutex and exit> ")

    print("Mutex released. Exiting...")

if __name__ == "__main__":
    find_index()
    main()

