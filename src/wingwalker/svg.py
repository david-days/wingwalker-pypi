"""
Functions to manipulate SVG files.
"""

import xml.etree.ElementTree as ET
import argparse
from wingwalker.output_templates import svg_template
import wingwalker.utils as utils

X, Y = range(2)

ET.register_namespace('', 'http://www.w3.org/2000/svg')

def substitute_placeholders(width: float, height: float, units: str, str_tpl: str = svg_template) -> str:
    """
    Substitutes the placeholders in the template string with given values.
    Args:
        height (float): The height of the SVG image
        width (float): The width of the SVG image
        units (str): The units of the SVG image
        str_tpl (str): The template string.  Optional, if not provided, the default svg template will be used.
    Returns:
        The string with substituted placeholders
    """
    str_xml = str_tpl.replace('{width}', str(width))
    str_xml = str_xml.replace('{height}', str(height))
    str_xml = str_xml.replace('{unit}', units)
    return str_xml


def from_svg_template(width: float, height: float, units: str, str_tpl: str = svg_template) -> ET.Element:
    """
    Creates an SVG element from the given template string
    This method uses the template (passed as a string) and returns the
    Args:
        height (int): The height of the SVG image
        width (int): The width of the SVG image
        units (str): The units of the SVG image
        str_tpl (str): The template string.  Optional, if not provided, the default svg template will be used.
    Returns:
        The root SVG element of the converted template
    """
    xml_str = substitute_placeholders(width, height, units, str_tpl)
    return ET.fromstring(xml_str)


def trace_airfoil_path(svg_root: ET.Element, xs: list[float], ys: list[float],
                       offset: list[float], l_width: float = 0.5):
    """
    Trace out the airfoil outline as a path, looping around and back to the starting point.

    Draws a path that traces the shape of the airfoil, completing the circuit and closing the loop
    back at the origin of the path.
    Args:
        svg_root (ElementTree.Element): The SVG tree containing the drawing
        xs (list): A list of x coordinates
        ys (list): A list of y coordinates
        offset (list): x- and y-offset from [0,0] to align the trace
        l_width (float): width of the path line. Default is 1.0
    """
    path_def = ""
    path_def += "M %f,%f" % (xs[0] + offset[X], ys[0] + offset[Y])
    for i in range(1, len(xs)):
        path_def += " L %f,%f" % (xs[i] + offset[X], ys[i] + offset[Y])
    path_def += " L %f,%f" % (xs[0] + offset[X], ys[0] + offset[Y])
    path = ET.SubElement(svg_root, 'path', {})
    path.set('id', 'airfoil_trace')
    path.set('d', path_def)
    path.set('fill', 'none')
    path.set('stroke', 'black')
    path.set('stroke-width', str(l_width))
    return svg_root


def trace_fill_path(svg_root: ET.Element, xs: list[float], ys: list[float], offset: list[float],
                    l_width: float = 0.5, factor: int = 7):
    path_def = ""
    path_def += "M %f,%f" % (xs[0] + offset[X], ys[0] + offset[Y])
    i = 0
    x_len: int = len(xs) - factor
    x_mid: int = int(len(xs) / 2)
    while i < (x_len - (2.0 * factor)):
        l_offset = int(i + factor)
        end_i = x_len - l_offset
        path_def += " L %f,%f" % (xs[end_i] + offset[X], ys[end_i] + offset[Y])
        next_i = i + factor
        path_def += " L %f,%f" % (xs[next_i] + offset[X], ys[next_i] + offset[Y])
        i = next_i
    # Trace the chord
    path_def += " M %f,%f" % (xs[0] + offset[X], ys[0] + offset[Y])
    x_len = len(xs) - 1
    for i in range(0,x_mid):
        path_def += " L %f,%f" % ((xs[i] + xs[x_len - i])/2.0 + offset[X], (ys[i] + ys[x_len - i])/2.0 + offset[Y])
    path = ET.SubElement(svg_root, 'path', {})
    path.set('id', 'airfoil_fill')
    path.set('d', path_def)
    path.set('fill', 'none')
    path.set('stroke', 'black')
    path.set('stroke-width', str(l_width))
    return svg_root


def draw_airfoil_poly(svg_root: ET.Element, xs, ys, offset, l_width: float = 0.5) -> ET.Element:
    """
    Creates the airfoil as a polygon with the given coordinates
    Args:
        xs (list): A list of x coordinates
        ys (list): A list of y coordinates
        offset (list): x- and y-offset from [0,0] to align the polygon line
        l_width (float): width of the polygon line
        svg_root (ET.Element): SVG root element
    """
    poly = ET.SubElement(svg_root, 'polygon', {})
    poly.set('points', ' '.join([f'{x + offset[X]},{y + offset[Y]}' for x, y in zip(xs, ys)]))
    poly.set('fill', 'none')
    poly.set('stroke', 'black')
    poly.set('stroke-width', str(l_width))
    return svg_root


def main(infile: str, outbase: str, c_len, units: str='mm', lednicer=False, trace=True, fill=False, poly=False, mirror=False) -> None:
    """
    Main function for generating SVG file from airfoil specifications and requirements.
    Args:
        infile: Input file
        outbase: Output file base name
        c_len: chord length in units
        units: chord length units.  default is 'mm'
        lednicer: true if the input file is lednicer formatted; otherwise, false and selig-format is assumed
        trace: create a trace SVG
        fill: create a fill SVG
        poly: create a poly SVG
        mirror: create a mirror for any of the outputs requested
    """
    x = []
    y = []
    with open(infile, 'rb') as f:
        dat_format = 'lednicer' if lednicer else 'selig'
        spec_name = utils.parse_specs(f, x, y, c_len, dat_format)
        print('Airfoil:  %s' % spec_name)
        print('\tFormat:  %s' % dat_format)
        print('\tChord length:  %f %s' % (c_len, units))
        print('\tTotal Coordinates:  %i' % len(x))
        print('\tTrace:  %s' % str(trace))
        print('\tFill:  %s' % str(fill))
        print('\tPoly:  %s' % str(poly))
        print('\tMirror:  %s' % str(mirror))
        if trace or fill or poly:
            svg_writer = SvgWriter(x, y, c_len, units)
            base_file = outbase
            if trace:
                svg_writer.generate_trace(base_file + '_shape', mirror=mirror, filled=False, l_width=1.0)
            if fill:
                svg_writer.generate_trace(base_file + '_filled', mirror=mirror, filled=True, l_width=0.75)
            if poly:
                svg_writer.generate_poly(base_file + '_poly', mirror=mirror)


class SvgWriter:

    x_coords: list[float] = []
    y_coords: list[float] = []
    c_len: float = 128.0
    units: str = 'mm'
    """
    Utility class to generate required sets of SVG files from specifications that have been read in
    """
    def __init__(self, xs: [float], ys: [float], clen: float = 128.0, unitval: str = "mm"):
        """
        Instantiates a new SvgWriter instance
        Args:
            xs (list): A list of x coordinates
            ys (list): A list of y coordinates
            clen (float): Length of the chord; default is 128
            unitval (str): The units of the SVG image; default is 'mm'
        """
        super().__init__()
        self.x_coords = xs
        self.y_coords = ys
        self.c_len = clen
        self.units = unitval

    def generate_trace(self, base_name: str = 'airfoil', mirror: bool = False, filled: bool = False, l_width: float = 0.5):
        xoff: float = self.c_len/10.0
        dim: float = self.c_len + (2.0 * xoff)
        t_offset: list[float] = [xoff, dim/2.0]
        trace_file = base_name + '.svg'
        svg_trace = from_svg_template(dim, dim, self.units)
        trace_airfoil_path(svg_trace, self.x_coords, self.y_coords, t_offset, l_width)
        if filled:
            trace_fill_path(svg_trace, self.x_coords, self.y_coords, t_offset, l_width)
        trace_tree = ET.ElementTree(svg_trace)
        trace_tree.write(trace_file, xml_declaration=True, encoding='utf-8')
        if mirror:
            # Create mirror image using flipped y-coords
            flip_y = [j * -1.0 for j in self.y_coords]
            mirror_file = base_name + '_mirror.svg'
            mirror_trace = from_svg_template(dim, dim, self.units)
            trace_airfoil_path(mirror_trace, self.x_coords, flip_y, t_offset, l_width)
            if filled:
                trace_fill_path(mirror_trace, self.x_coords, flip_y, t_offset, l_width)
            mirror_tree = ET.ElementTree(mirror_trace)
            mirror_tree.write(mirror_file, xml_declaration=True, encoding='utf-8')

    def generate_poly(self, base_name: str = 'airfoil', mirror: bool = False, l_width: float = 0.5):
        xoff: float = self.c_len/10.0
        dim: float = self.c_len + (2.0 * xoff)
        t_offset: list[float] = [xoff, dim/2.0]
        svg_root = from_svg_template(dim, dim, self.units)
        draw_airfoil_poly(svg_root, self.x_coords, self.y_coords, t_offset, 0.5)
        tree = ET.ElementTree(svg_root)
        poly_file = base_name + '.svg'
        tree.write(poly_file, xml_declaration=True, encoding='utf-8')
        if mirror:
            flip_y = [j * -1.0 for j in self.y_coords]
            mirror_root = from_svg_template(dim, dim, self.units)
            draw_airfoil_poly(mirror_root, self.x_coords, flip_y, t_offset, 0.5)
            mirror_file = base_name + '_mirror.svg'
            mirror_tree = ET.ElementTree(mirror_root)
            mirror_tree.write(mirror_file, xml_declaration=True, encoding='utf-8')

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Parse airfoil spec and generate SVG files')
    arg_parser.add_argument('-i', '--input', dest='input', type=str,
                            help='Airfoil spec file', required=True)
    arg_parser.add_argument('-o', '--output', dest='output', type=str,
                            help='Base filename to be written', default='airfoil', required=False)
    arg_parser.add_argument('-s', '--selig', dest='selig', action='store_true',
                            default=True, help='File is in Selig format (default true)', required=False)
    arg_parser.add_argument('-l', '--lednicer', dest='lednicer', action='store_true',
                            default=False, help='File is in Lednicer format (default false)', required=False)
    arg_parser.add_argument('-c', '--chord', dest='c_len', type=float, default=1.0,
                            help='Chord length to generate', required=False)
    arg_parser.add_argument('-u', '--units', dest='units', type=str, default='mm',
                            help='Chord units; defaults to mm', required=False)
    arg_parser.add_argument('-t', dest='trace', action='store_true',
                            help='Generate trace of the airfoil', required=False)
    arg_parser.add_argument('-f', dest='fill', action='store_true',
                            help='Generate fill of the airfoil trace', required=False)
    arg_parser.add_argument('-p', dest='poly', action='store_true',
                            help='Generate polygon trace', required=False)
    arg_parser.add_argument('-m', dest='mirror', action='store_true',
                            help='Generate mirror images with each type', required=False)
    # parse arguments
    args = arg_parser.parse_args()
    main(args.input, args.output, args.c_len, args.units, args.lednicer, args.trace, args.fill, args.poly, args.mirror)
