class FreemocapError(Exception):
    """Base class for FreeMoCap errors."""
    pass


class DataFileNotFoundError(FreemocapError):
    """Raised when a specified data file is not found."""

    def __init__(self, path):
        super().__init__(f"Path not found: {path}")
