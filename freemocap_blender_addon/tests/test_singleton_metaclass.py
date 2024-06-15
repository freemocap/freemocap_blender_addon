from freemocap_blender_addon.utilities.singleton_metaclass import SingletonMetaClass


class TestSingleton(metaclass=SingletonMetaClass):
    """
    Example Singleton class.

    This class demonstrates the Singleton pattern by allowing only one instance of itself to be created.
    It has basic methods to set and get a value, which can be used to observe the singleton behavior.

    Attributes:
        value (any): A value to demonstrate the singleton behavior.
    """

    def __init__(self) -> None:
        """
        Initializes the Singleton instance with a default value of None.
        """
        self.value = None

    def set_value(self, value: any) -> None:
        """
        Sets the value of the Singleton instance.

        Args:
            value (any): The value to set.
        """
        self.value = value

    def get_value(self) -> any:
        """
        Gets the value of the Singleton instance.

        Returns:
            any: The current value of the Singleton instance.
        """
        return self.value

def test_singleton_instance():
    """
    Tests that only one instance of the Singleton class is created.
    """
    instance1 = TestSingleton()
    instance2 = TestSingleton()

    assert instance1 is instance2, "Singleton instances are not the same!"


def test_singleton_value():
    """
    Tests that the value set in one Singleton instance is reflected in another.
    """
    instance1 = TestSingleton()
    instance2 = TestSingleton()

    instance1.set_value(10)
    assert instance1.get_value() == 10, "Singleton value not set correctly"
    assert instance2.get_value() == 10, "Singleton value not shared correctly between instances"


def test_singleton_thread_safety():
    """
    Tests the thread safety of the Singleton pattern implementation.

    This test creates multiple threads that attempt to set the value of the Singleton instance.
    It ensures that the final value is one of the values set by the threads, indicating that
    the Singleton implementation is thread-safe.
    """
    import threading

    def set_singleton_value(value):
        instance = TestSingleton()
        instance.set_value(value)
    instance = TestSingleton()

    threads = []
    for i in range(100):
        t = threading.Thread(target=set_singleton_value, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert instance.get_value() in range(100), "Singleton value may not be thread-safe"

