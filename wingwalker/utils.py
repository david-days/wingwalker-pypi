"""
 Useful functions for wingwalker
"""

import wingwalker.selig as selig
import wingwalker.lednicer as lednicer


def parse_specs(stream, xs, ys, c_len, dat_format: str = "selig") -> str:
    """
    Parses a given airoil spec file, reads out and converts the shape coordinates, and attempts to return the read name
    Args:
        stream (IO): I/O stream of file
        xs (list): list to be filled with x-coordinate values
        ys (list): list to be filled with y-coordinate values
        c_len (float): chord length in required units
        dat_format (str): data format.  If not supplied, defaults to 'selig'
    Returns:
        The name of the airfoil from the spec file, if found
    Raises:
        Exception: If the spec format is unrecognized
    """
    spec_name = "airfoil"
    match dat_format:
        case "selig":
            spec_name = selig.parse_selig(stream, xs, ys, c_len)
        case "lednicer":
            spec_name = lednicer.parse_lednicer(stream, xs, ys, c_len)
        case _:
            raise Exception("Unknown file format: " + dat_format)
    return spec_name
