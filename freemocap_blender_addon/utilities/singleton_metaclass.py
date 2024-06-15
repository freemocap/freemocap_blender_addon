from threading import Lock
from typing import Type, TypeVar, Optional

# Create a generic type variable to be used for type hints in SingletonMeta
SingletonClass = TypeVar('SingletonClass', bound='SingletonMeta')

class SingletonMetaClass(type):
    """
    A thread-safe implementation of Singleton pattern.

    A Singleton ensures that a class has only one instance and provides a global point of access to it.
    This implementation is thread-safe, meaning it handles concurrent access correctly.

    Attributes:
        _instances (Optional[dict[Type, object]]): A dictionary to store singleton instances.
        _lock (Lock): A lock object to ensure thread safety during instance creation.
    """
    _instances: Optional[dict[Type, object]] = None
    _lock: Lock = Lock()

    def __init__(cls, *args, **kwargs) -> None:
        """
        Initializes the metaclass. Ensures _instances is a dictionary.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if cls._instances is None:
            cls._instances = {}
        super().__init__(*args, **kwargs)

    def __call__(cls: Type[SingletonClass], *args, **kwargs) -> SingletonClass:
        """
        Controls the instantiation process to ensure only one instance is created.

        This is achieved by checking if an instance of the class already exists in the
        _instances dictionary. If not, it creates one in a thread-safe manner and stores it.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            SingletonClass: The singleton instance.
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # Double-checked locking
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]
