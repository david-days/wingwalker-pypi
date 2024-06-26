"""
Functions to manipulate SVG files.
"""

import cairo
import xml.etree.ElementTree as ET
import argparse
from output_templates import svg_template
import utils

X, Y = range(2)


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


def from_svg_template(width: int, height: int, units: str, str_tpl: str = svg_template) -> ET.Element:
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


def trace_airfoil_path(surface: cairo.SVGSurface, width: float, height: float, xs: list[float], ys: list[float],
                       offset: list[float], l_width: float = 1.0, close_loop: bool = True):
    """
    Trace out the airfoil outline as a path, looping around and back to the starting point.

    Draws a path that traces the shape of the airfoil, completing the circuit and closing the loop
    back at the origin of the path.
    Args:
        surface (cairo.SVGSurface): The SVG surface for drawing
        width (float): The width of the SVG image
        height (float): The height of the SVG image
        xs (list): A list of x coordinates
        ys (list): A list of y coordinates
        offset (list): x- and y-offset from [0,0] to align the trace
        l_width (float): width of the path line. Default is 1.0
        close_loop (bool): Optional, whether to close the loop.  Defaults to true
    """
    with cairo.Context(surface) as c:
        c.scale(width, height)
        c.set_source_rgb(0, 0, 0)
        c.move_to(xs[0] + offset[X], ys[0] + offset[Y])
        for i in range(1, len(xs)):
            c.line_to(xs[i] + offset[X], ys[i] + offset[Y])
        if close_loop:
            c.line_to(xs[0] + offset[X], ys[0] + offset[Y])
        c.set_line_width(l_width)
        c.stroke()


def trace_fill_path(surface:cairo.SVGSurface, width: float, height: float, xs: list[float], ys: list[float],
                    offset: list[float], l_width: float = 1.0, factor: int = 7):
    with cairo.Context(surface) as c:
        c.scale(width, height)
        c.set_source_rgb(0, 0, 0)
        c.move_to(xs[0] + offset[X], ys[0] + offset[Y])
        i = 0
        x_len: int = len(xs) - factor
        x_mid: int = int(len(xs) / 2)
        while i < x_len:
            l_offset = int(-1 * (i + factor))
            end_i = x_len - l_offset
            c.line_to(xs[end_i] + offset[X], ys[end_i] + offset[Y])
            next_i = i + factor
            c.line_to(xs[next_i] + offset[X], ys[next_i] + offset[Y])
            i = next_i
        c.set_line_width(l_width)
        c.stroke()


def draw_airfoil_poly(xs, ys, offset, l_width, svg_root: ET.Element) -> ET.Element:
    """
    Creates the airfoil as a polygon with the given coordinates
    Args:
        xs (list): A list of x coordinates
        ys (list): A list of y coordinates
        offset (list): x- and y-offset from [0,0] to align the polygon line
        l_width (float): width of the polygon line
        svg_root (ET.Element): SVG root element
    """
    g_elem = ET.SubElement(svg_root, 'g', {})
    poly = ET.SubElement(g_elem, 'polygon', {})
    poly.set('points', ' '.join([f'{x + offset[X]},{y + offset[Y]}' for x, y in zip(xs, ys)]))
    poly.set('fill', 'none')
    poly.set('stroke', 'black')
    poly.set('stroke-width', str(l_width))
    return svg_root


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

    def generate_trace(self, base_name: str = 'airfoil', mirror: bool = False, filled: bool = False):
        xoff: float = self.c_len/10.0
        dim: float = self.c_len + (2.0 * xoff)
        t_offset: list[float] = [xoff, dim/2.0]
        base_file = base_name + '_trace.svg'
        with cairo.SVGSurface(base_file, dim, dim) as surface:
            trace_airfoil_path(surface, dim, dim, self.x_coords, self.x_coords, t_offset)
            if filled:
                trace_fill_path(surface, dim, dim, self.y_coords, self.y_coords, t_offset)
        if mirror:
            # Create mirror image using flipped y-coords
            flip_y = [j * -1.0 for j in self.y_coords]
            mirror_file = base_name + '_trace_mirror.svg'
            with cairo.SVGSurface(mirror_file, dim, dim) as surface:
                trace_airfoil_path(surface, dim, dim, self.x_coords, flip_y, t_offset)
                if filled:
                    trace_fill_path(surface, dim, dim, self.x_coords, flip_y, t_offset)

    def generate_poly(self, base_name: str = 'airfoil', mirror: bool = False):
        xoff: float = self.c_len/10.0
        dim: float = self.c_len + (2.0 * xoff)
        t_offset: list[float] = [xoff, dim/2.0]
        svg_root = from_svg_template(dim, dim)
        draw_airfoil_poly(self.x_coords, self.y_coords, t_offset, 1.0, svg_root)
        tree = ET.ElementTree(svg_root)
        poly_file = base_name + '_polygon.svg'
        tree.write(poly_file)
        if mirror:
            flip_y = [j * -1.0 for j in self.y_coords]
            mirror_root = from_svg_template(dim, dim)
            draw_airfoil_poly(self.x_coords, flip_y, t_offset, 1.0, mirror_root)
            mirror_file = base_name + '_polygon_mirror.svg'
            mirror_tree = ET.ElementTree(mirror_root)
            mirror_tree.write(mirror_file)


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
    x = []
    y = []
    with open(args.input, 'rb') as f:
        dat_format = 'lednicer' if args.lednicer else 'selig'
        spec_name = utils.parse_specs(f, x, y, args.c_len, dat_format)
        print('Airfoil:  %s' % spec_name)
        print('Format:  %s' % dat_format)
        print('\tChord length:  %f %s' % (args.c_len, args.units))
        print('\tTotal Coordinates:  %i' % len(x))
        print('\tTrace:  %s' % str(args.trace))
        print('\t\tFill:  %s' % str(args.fill))
        print('\tPoly:  %s' % str(args.poly))
        print('\tMirror:  %s' % str(args.mirror))
        if args.trace or args.fill or args.poly:
            svg_writer = SvgWriter(x, y, args.c_len, args.units)
            base_file = args.output
            if args.trace:
                svg_writer.generate_trace(base_file, mirror=args.mirror, filled=False)
            if args.fill:
                svg_writer.generate_trace(base_file, mirror=args.mirror, filled=True)
            if args.poly:
                svg_writer.generate_poly(base_file, mirror=args.mirror)
