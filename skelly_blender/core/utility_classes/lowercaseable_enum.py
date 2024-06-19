from enum import Enum
from typing import List


class LowercaseableEnum(Enum):
    def lower(self) -> str:
        return self.name.lower()

    @classmethod
    def to_lowercase_list(cls) -> List[str]:
        """Return a list of the names of each member converted to lowercase."""
        return [member.name.lower() for member in cls]


if __name__ == "__main__":
    class TestEnum(LowercaseableEnum):
        FOO = 1
        BAR = 2
        BAZ = 3

    assert TestEnum.FOO.lower() == "foo"
    assert TestEnum.BAR.lower() == "bar"
    assert TestEnum.BAZ.lower() == "baz"
    assert TestEnum.to_lowercase_list() == ["foo", "bar", "baz"]
    print("All tests passed!")