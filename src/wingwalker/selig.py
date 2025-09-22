"""
Functions to parse Selig-formatted data
"""

import re
from io import TextIOWrapper

import wingwalker.base as base
import wingwalker.utils as utils
import argparse


def parse_selig(stream: TextIOWrapper, x_coords: list[float], y_coords: list[float], c_len: float = 1.0) -> str:
    """
    Parse Selig-formated airfoil specifications
    Args:
        stream: existing file stream
        x_coords:  empty array to hold the X (chord-oriented) coordinates
        y_coords: empty array to hold the Y (chord-perpendicular) coordinates
        c_len: float value denoting the final chord length (units not required)
    Returns:
        Name of the Selig-formatted airfoil
    """
    airfoil_desig = 'airfoil'
    lines = stream.readlines()
    for line in lines:
        linetxt = line.decode('utf-8')
        if bool(re.search(utils.coord_patt, linetxt)):
            x0, y0 = utils.convert_float(linetxt)
            x_coords.append(x0 * c_len)
            y_coords.append(y0 * c_len)
        elif (not str.isspace(linetxt)) and len(linetxt) != 0:
            print("Found airfoil id: " + linetxt)
            airfoil_desig = linetxt

    return airfoil_desig.strip()


class Parser(base.Reader):
    """
    Parser for Selig-formatted airfoil specifications.

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
            airfoil_desig = parse_selig(file, xs, ys, chord_len)
            return xs, ys, airfoil_desig


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Parse Selig-formatted airfoil specs')
    arg_parser.add_argument('-f', '--filename', metavar='File', type=str, help='File to be parsed')
    arg_parser.add_argument('-c', '--chord', dest='c_len', type=float, default=1.0,
                            help='Chord length to calculate', required=False)
    args = arg_parser.parse_args()
    fparser = Parser(args.filename)
    x_vals, y_vals, spec = fparser.read(args.c_len)
    print("Airfoil specs for:  %s" % spec)
    print(x_vals, y_vals)
