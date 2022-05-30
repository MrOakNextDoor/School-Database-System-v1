#   Provides miscellaneous functionality.

#   Libraries
from typing import Tuple


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
