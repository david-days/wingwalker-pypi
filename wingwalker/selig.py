"""
Functions to parse Selig-formatted data
"""

import re

selig_coord_patt = '(?<=^\\s\\s)[+-]?([0-9]*[.])?[0-9]+\\s+[+-]?([0-9]*[.])?[0-9]+'
airfoil_desig = 'airfoil'


def convert_float(inp) -> (float, float):
    """
    Convert a text line into X and Y coordinates
    """
    floats = [float(i) for i in inp.split(' ') if i.count('.') == 1]
    return floats[0], floats[1]


def parse_selig(stream, xs, ys, chord_len) -> str:
    """
    Parse Selig-formated airfoil specifications
    Args:
        stream: existing file stream
        xs:  empty array to hold the X (chord-oriented) coordinates
        ys: empty array to hold the Y (chord-perpendicular) coordinates
        chord_len: float value denoting the final chord length (units not required)
    Returns:
        Name of the Selig-formatted airfoil
    """
    global airfoil_desig
    lines = stream.readlines()
    for line in lines:
        linetxt = line.decode('utf-8')
        if bool(re.search(selig_coord_patt, linetxt)):
            x0, y0 = convert_float(linetxt)
            xs.append(x0 * chord_len)
            ys.append(y0 * chord_len)
        elif (not str.isspace(linetxt)) & len(linetxt) != 0:
            print("Found airfoil id: " + linetxt)
            airfoil_desig = linetxt

    return airfoil_desig
