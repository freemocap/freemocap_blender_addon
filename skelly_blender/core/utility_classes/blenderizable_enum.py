import re
from copy import copy
from enum import Enum

from skelly_blender.core.custom_type_hints import BlenderizedName


class BlenderizableEnumABC(Enum):
    def blenderize(self) -> BlenderizedName:
        return blenderize_name(self.name)


def blenderize_name(original_name: str) -> BlenderizedName:
    """
    Create a Blender formatted name from the original name.

    Parameters
    ----------
    original_name : str
        The original name to be converted.

    Returns
    -------
    str
        The Blender formatted name.

    Examples
    --------
    >>> blenderize_name("Upper Arm Right")
    'upper_arm.R'

    >>> blenderize_name("Lower-Leg (Left)")
    'lower-leg.L'
    """
    name = copy(original_name)
    if ".R" in original_name:
        name = original_name.replace(".R", "")
        name += ".R"
    elif ".L" in original_name:
        name = original_name.replace(".L", "")
        name += ".L"

    name = camel_to_snake(name)

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove disallowed special characters, allow only alphanumerics, underscores, periods, and hyphens
    name = re.sub(r'[^a-zA-Z0-9_.-]', '', name)

    # Make all characters lower case
    name = name.lower()

    # Check for "right" or "left" and move ".R" or ".L" to the end
    name = convert_right_left_naming_to_blender_style(name)

    # Remove double underscores
    name = name.replace("__", "_")
    name = name.replace("..", ".")

    return name


def convert_right_left_naming_to_blender_style(name: str) -> str:
    # Updated regex to handle underscores and other delimiters
    if re.search(r'(?<![a-zA-Z0-9])(right|r)(?![a-zA-Z0-9])', name):
        name = re.sub(r'(?<![a-zA-Z0-9])(right|r)(?![a-zA-Z0-9])', '', name)
        name = name.strip('_-')
        name += '.R'
    elif re.search(r'(?<![a-zA-Z0-9])(left|l)(?![a-zA-Z0-9])', name):
        name = re.sub(r'(?<![a-zA-Z0-9])(left|l)(?![a-zA-Z0-9])', '', name)
        name = name.strip('_-')
        name += '.L'
    return name


def camel_to_snake(name: str) -> str:
    """
    Convert a camelCase or PascalCase string to snake_case.

    Parameters
    ----------
    name : str
        The original camelCase or PascalCase string.

    Returns
    -------
    str
        The snake_case formatted string.

    Examples
    --------
    >>> camel_to_snake("CamelCase")
    'camel_case'

    >>> camel_to_snake("camelCase")
    'camel_case'
    """
    # Add underscores between lowercase followed by uppercase letters
    name = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name)
    # Convert the entire string to lowercase
    return name.lower()


if __name__ == "__main__":
    print(camel_to_snake("CamelCase"))  # Expected Output: camel_case
    print(camel_to_snake("camelCase"))  # Expected Output: camel_case
    print(camel_to_snake("PascalCaseExample"))  # Expected Output: pascal_case_example
    print(camel_to_snake("exampleWithNumbers123"))  # Expected Output: example_with_numbers123
    print(blenderize_name("Upper Arm Right"))  # Expected Output: upper_arm.R
    print(blenderize_name("Lower-Leg (Left)"))  # Expected Output: lower-leg.L
    print(blenderize_name("ELBOW_LEFT"))  # Expected Output: elbow.L
    print(blenderize_name("left_elbow"))  # Expected Output: elbow.L
    print(blenderize_name("RightArm"))  # Expected Output: arm.R
    print(blenderize_name("LEFT_ARM"))  # Expected Output: arm.L
    print(blenderize_name("arm-Right"))  # Expected Output: arm.R
    print(blenderize_name("upper_right_arm"))  # Expected Output: upper_arm.R
    print(blenderize_name("upper_.R_arm"))  # Expected Output: upper_arm.R
