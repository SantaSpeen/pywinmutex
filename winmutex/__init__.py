import threading

import win32event
import win32api
import winerror
import atexit

class WindowsMutex:
    def __init__(self, name, multiuser=False, timeout=None):
        """
        Initialize the WindowsMutex object.
        :param name: Name of the mutex.
        :param multiuser: If True, create a local mutex; if False, create a global mutex (Shared across all users).
        """
        self.__multiuser = multiuser
        self._friendly_name = name
        __global_prefix = "Global\\" if multiuser else ""
        self._mutex_name = f"{__global_prefix}{name}"
        self._handler = None
        self._exist = False
        self._th_lock = threading.Lock()
        self.timeout = timeout
        atexit.register(self.release)

    def __try_to_lock(self):
        """
        Try to acquire the mutex.
        :return: True if the mutex was acquired, False otherwise.
        """
        with self._th_lock:  # Thread-safe access
            handler = win32event.CreateMutex(None, False, self._mutex_name)
            if handler is None:
                raise RuntimeError("Failed to create mutex.")
            exist = win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS
            if not exist:
                win32api.CloseHandle(handler)
            return exist

    def reinint(self, name, multiuser=None):
        """
        Reinitialize the mutex with a new name.
        :param name: New name for the mutex.
        :param local: If True, create a local mutex; if False, create a global mutex.
        """
        self.release()
        if multiuser is None:
            multiuser = self.__multiuser
        self.__init__(name, multiuser)

    @property
    def settings(self):
        """
        Get the settings of the mutex.
        :return: A dictionary containing the mutex name and existence status.
        """
        return {
            "name": self._mutex_name,
            "exist": self.exist
        }

    @property
    def exist(self):
        """
        Check if the mutex already exists.
        :return: True if the mutex exists, False otherwise.
        """
        if self._handler is None:
            return self.__try_to_lock()
        return self._exist

    def _lock(self):
        """
        Try to lock the mutex.
        :return: True if acquired, False otherwise.
        """
        with self._th_lock:  # Thread-safe access
            if self._handler is None:  # Создаём мутекс только один раз
                self._handler = win32event.CreateMutex(None, False, self._mutex_name)
                self._exist = win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS
                return not self._exist  # True, если удалось захватить мутекс
            return False  # Если мутекс уже создан, значит, его кто-то держит

    def acquire(self, timeout=None, __raw_result=False):
        """
        Wait until the mutex is acquired.
        :param timeout: Timeout in milliseconds. If None, waits indefinitely.
        :param __raw_result:  If True, return the raw result of WaitForSingleObject.
        :return: True if acquired, False if timeout.
        """
        if self._handler is None:
            self._lock()

        wait_time = timeout if timeout is not None else win32event.INFINITE
        result = win32event.WaitForSingleObject(self._handler, wait_time)

        if result != win32event.WAIT_OBJECT_0:
            self._handler = None
            self._exist = False

        if __raw_result:
            return result

        return result == win32event.WAIT_OBJECT_0

    def release(self):
        """
        Release the mutex.
        :return: None
        """
        with self._th_lock:  # Thread-safe access
            if self._handler:
                win32event.ReleaseMutex(self._handler)
                win32api.CloseHandle(self._handler)  # Закрываем _handler!
                self._handler = None
                self._exist = False

    def __enter__(self):
        reason = self.acquire(self.timeout, True)
        if reason == win32event.WAIT_OBJECT_0:
            return self
        elif reason == win32event.WAIT_TIMEOUT:
            raise TimeoutError("Mutex acquisition timed out.")
        elif reason == win32event.WAIT_ABANDONED:
            raise RuntimeError("Mutex was abandoned.")
        else:
            raise RuntimeError("Failed to acquire mutex.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __str__(self):
        return f"{self!r}"

    def __repr__(self):
        return f"<WindowsMutex(name={self._friendly_name!r}, multiuser={self.__multiuser})>"
