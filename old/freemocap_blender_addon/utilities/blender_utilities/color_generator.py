from enum import Enum
from typing import Tuple

import numpy as np


class ColorType(Enum):
    RANDOM = "random"
    NEUTRAL = "neutral"
    VIVID = "vivid"
    RIGHT = "right"
    LEFT = "left"
    PASTEL = "pastel"
    JEWEL = "jewel"


def generate_random_hex_color() -> str:
    """
    Generate a random hex color code.

    Returns
    -------
    str
        A string representing a random hex color code in the format '#RRGGBB'.
    """
    return f'#{np.random.randint(0, 0xFFFFFF):06X}'


def adjust_brightness(channels: Tuple[int, int, int], shift: int) -> Tuple[int, int, int]:
    """
    Adjust the brightness of the given RGB channels.

    Parameters
    ----------
    channels : Tuple[int, int, int]
        The RGB channels to adjust.
    shift : int
        The amount to shift the brightness by.

    Returns
    -------
    Tuple[int, int, int]
        The adjusted RGB channels.
    """
    return tuple(min(max(c + shift, 0), 255) for c in channels)


def generate_color_channels(type: ColorType) -> Tuple[int, int, int]:
    """
    Generate RGB color channels based on the provided color type.

    Parameters
    ----------
    type : ColorType
        The type of color to generate.

    Returns
    -------
    Tuple[int, int, int]
        A tuple representing the RGB channels.
    """
    if type == ColorType.NEUTRAL:
        value = np.random.randint(0, 256)
        return value, value, value
    elif type in (ColorType.VIVID, ColorType.PASTEL, ColorType.JEWEL):
        max_index = np.random.choice([0, 1, 2])
        channels = [0] * 3
        channels[max_index] = 255
        min_index = (max_index + 1) % 3
        channels[min_index] = np.random.randint(0, 128)
        mid_index = (max_index + 2) % 3
        channels[mid_index] = np.random.randint(0, 256)
        if type == ColorType.PASTEL:
            return adjust_brightness(tuple(channels), 128)
        elif type == ColorType.JEWEL:
            return adjust_brightness(tuple(channels), -128)
        else:
            return tuple(channels)
    elif type == ColorType.RIGHT:
        return 255, np.random.randint(0, 256), np.random.randint(0, 256)
    elif type == ColorType.LEFT:
        return np.random.randint(0, 256), np.random.randint(0, 256), 255
    else:
        return tuple(np.random.randint(0, 256) for _ in range(3))


def generate_color(type: ColorType) -> str:
    """
    Generate a color based on the provided color type.

    Parameters
    ----------
    type : ColorType
        The type of color to generate.

    Returns
    -------
    str
        A string representing a hex color code in the format '#RRGGBB'.
    """
    r, g, b = generate_color_channels(type)
    return f'#{r:02X}{g:02X}{b:02X}'


if __name__ == "__main__":
    print("Random color:", generate_random_hex_color())
    print("Neutral color:", generate_color(ColorType.NEUTRAL))
    print("Vivid color:", generate_color(ColorType.VIVID))
    print("Right (red-shifted) color:", generate_color(ColorType.RIGHT))
    print("Left (blue-shifted) color:", generate_color(ColorType.LEFT))
    print("Pastel color:", generate_color(ColorType.PASTEL))
    print("Jewel color:", generate_color(ColorType.JEWEL))
