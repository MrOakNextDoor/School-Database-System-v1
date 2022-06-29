#   Provides miscellaneous functionality.

#   Libraries
from typing import Tuple, Optional


#   Code
def extract_geometry(geometry: str) -> Tuple[int, int, int, int]:
    """Extract the width, height, x, and y from a tkinter string geometry.
    Args:
        geometry (str): The geometry used to extract the information.
    Returns:
        Tuple[int, int, int, int]: The extracted width, height, x, and y.
    """
    
    w = geometry.split('x')
    hxy = w[1].split('+')
    hxy.insert(0, w[0])
    return tuple(hxy)

def convert_blank(value: str) -> Optional[str]:
    """Converts a blank string into None.
    Args:
        value: The string to be converted
    Returns:
        Optional[str]: The converted string.
    """

    try:
        if value.strip() == '':
            return None
    except AttributeError:
        return None
    return value
