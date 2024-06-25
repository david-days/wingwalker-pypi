"""
Functions to manipulate SVG files.
"""

import cairo
import xml.etree.ElementTree as ET
from wingwalker.output_templates import svg_template

X, Y = range(2)


def substitute_placeholders(width: int, height: int, units: str, str_tpl: str = svg_template) -> str:
    """
    Substitutes the placeholders in the template string with given values.
    Args:
        height (int): The height of the SVG image
        width (int): The width of the SVG image
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


def open_svg(width: float, height: float) -> cairo.SVGSurface:
    """
    Creates a Cairo.SVGSurface, of the given dimensions
    Args:
        width (float): The width of the SVG image
        height (float): The height of the SVG image
    """
    return cairo.SVGSurface(cairo.FORMAT_ARGB32, width, height)


def trace_airfoil_path(surface: cairo.SVGSurface, width: float, height: float, xs: list[float], ys: list[float],
                       offset: list[float], l_width: float, close_loop: bool = True):
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
        l_width (float): width of the path line
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
