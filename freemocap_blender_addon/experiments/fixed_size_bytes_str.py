import codecs
from typing import Union

import numpy as np

FIXED_SIZE_REFERENCE_DTYPE = np.complex128
DEFAULT_FIXED_SIZE = np.dtype(FIXED_SIZE_REFERENCE_DTYPE).itemsize


class FixedSizeBytes:
    def __init__(self, content: bytes, fixed_size: int = DEFAULT_FIXED_SIZE):
        if len(content) > fixed_size:
            raise ValueError(f"Bytes content exceeds fixed size of {fixed_size} bytes")
        self.content = content
        self.fixed_size = fixed_size

    def to_fixed_size(self) -> bytes:
        return self.content.ljust(self.fixed_size, b'\0')

    @classmethod
    def from_fixed_size(cls, fixed_size_element: bytes, fixed_size: int = DEFAULT_FIXED_SIZE):
        return cls(fixed_size_element.rstrip(b'\0'), fixed_size)


DEFAULT_FIXED_SIZE_STRING_ENCODING = codecs.BOM_UTF32


class FixedSizeStr:
    def __init__(self,
                 content: str,
                 fixed_size: int = DEFAULT_FIXED_SIZE,
                 encoding_format: Union[str, codecs.CodecInfo] = 'utf-8'):
        self.encoding_format = encoding_format
        encoded_content = content.encode(encoding_format)
        if len(encoded_content) > fixed_size:
            raise ValueError(f"String exceeds fixed size of {fixed_size} bytes - {content}")
        self.fixed_size_bytes = FixedSizeBytes(encoded_content, fixed_size)
        self.fixed_size = fixed_size

    def to_fixed_size_bytes(self) -> bytes:
        return self.fixed_size_bytes.to_fixed_size()

    @classmethod
    def from_fixed_size_bytes(cls, fixed_size_element: bytes, fixed_size: int = DEFAULT_FIXED_SIZE):
        decoded_str = fixed_size_element.rstrip(b'\0').decode('utf-8')
        return cls(decoded_str, fixed_size)

    def __str__(self) -> str:
        return self.fixed_size_bytes.content.decode(self.encoding_format)