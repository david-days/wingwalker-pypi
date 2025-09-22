f"""
Functions to parse Lednicer-formatted airfoil specs
"""
from io import TextIOWrapper

import wingwalker.utils as utils
import re
import wingwalker.base as base
import argparse


def parse_lednicer(stream: TextIOWrapper, x_coords: list[float], y_coords: list[float], c_len: float = 1.0) -> str:
    """
    Parse Selig-formated airfoil specifications
    Args:
        stream: existing file stream
        x_coords:  empty array to hold the X (chord-oriented) coordinates
        y_coords: empty array to hold the Y (chord-perpendicular) coordinates
        c_len: float value denoting the final chord length (units not required)
    Returns:
        Name of the Lednicer-formatted airfoil
    """
    airfoil_desig = 'airfoil'
    upper_len: int = 0
    lower_len: int = 0
    x_upper, y_upper, x_lower, y_lower = [], [], [], []

    lines = stream.readlines()
    # Read the header info
    for i in range(2):
        line = lines[i]
        linetxt = line.decode('utf-8')
        if i == 0:
            airfoil_desig = linetxt
        else:
            upper_len, lower_len = utils.convert_int(linetxt)
    # Start parsing the actual coordinates
    # Use offset value to track position
    offset = 3
    for u in range(upper_len):
        uline = lines[u + offset]
        utxt = uline.decode('utf-8')
        if bool(re.search(utils.coord_patt, utxt)):
            x0, y0 = utils.convert_float(utxt)
            x_upper.append(x0 * c_len)
            y_upper.append(y0 * c_len)
    offset = 4 + upper_len
    for v in range(lower_len):
        vline = lines[v + offset]
        vtxt = vline.decode('utf-8')
        if bool(re.search(utils.coord_patt, vtxt)):
            x0, y0 = utils.convert_float(vtxt)
            x_lower.append(x0 * c_len)
            y_lower.append(y0 * c_len)

    # Compile the results
    for i in range(upper_len):
        x_coords.append(x_upper[i])
        y_coords.append(y_upper[i])
    for j in range(lower_len - 1, -1, -1):
        x_coords.append(x_lower[j])
        y_coords.append(y_lower[j])
    return airfoil_desig.strip()


class Parser(base.Reader):
    """
    Parser for Lednicer-formatted airfoil specifications.

    This class parses the specs, translates them into the common [x],[y] coordinates, and holds onto them for
    further processing.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename

    def read(self, c_len = 1.0):
        with open(self.filename, 'rb') as file:
            xs = []
            ys = []
            chord_len = c_len
            airfoil_desig = parse_lednicer(file, xs, ys, chord_len)
            return xs, ys, airfoil_desig


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Parse Lednicer-formatted airfoil specs')
    arg_parser.add_argument('-f', '--filename', metavar='File', type=str, help='File to be parsed')
    arg_parser.add_argument('-c', '--chord', dest='c_len', type=float, default=1.0,
                            help='Chord length to calculate', required=False)
    args = arg_parser.parse_args()
    fparser = Parser(args.filename)
    x_vals, y_vals, spec = fparser.read(args.c_len)
    print("Airfoil specs for:  %s" % spec)
    print(x_vals, y_vals)
