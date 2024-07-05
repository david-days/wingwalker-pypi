"""
 Useful general functions for wingwalker
"""

import wingwalker.selig as selig
import wingwalker.lednicer as lednicer

coord_patt = '(?<=^\\s\\s)[+-]?([0-9]*[.])?[0-9]+\\s+[+-]?([0-9]*[.])?[0-9]+'


def convert_float(inp) -> (float, float):
    """
    Convert a text line into X and Y coordinates
    """
    floats = [float(i) for i in inp.split(' ') if i.count('.') == 1]
    return floats[0], floats[1]


def convert_int(inpt) -> (int, int):
    """
    Convert a text line into integer values
    """
    floats = convert_float(inpt)
    return int(floats[0]), int(floats[1])


def parse_specs(stream, xs, ys, c_len, dat_format: str = "selig") -> str:
    """
    Parses a given airfoil spec file, reads out and converts the shape coordinates, and attempts to return the read name
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
