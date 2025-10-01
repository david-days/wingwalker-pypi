"""
Module wingwalker is an airfoil designed library, providing tools and processes to ease creating custom airfoils (wings,
stabilizers, and control surfaces)

__version__ = '0.9.0'
__author__ = 'David Days'
__email__ = 'david.c.days@gmail.com'
"""

from wingwalker.selig import (
    parse_selig,
    Parser as SeligParser
)
from wingwalker.lednicer import (
    parse_lednicer,
    Parser as LednicerParser
)
from wingwalker.utils import (
    parse_specs
)
from wingwalker.svg import (
    substitute_placeholders,
    from_svg_template,
    trace_airfoil_path,
    draw_airfoil_poly
)
import wingwalker.output_templates as templates

# read version from installed package
from importlib.metadata import version
__version__ = version("wingwalker")
