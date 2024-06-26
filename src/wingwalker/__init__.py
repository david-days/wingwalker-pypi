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
    open_svg,
    trace_airfoil_path,
    draw_airfoil_poly
)
import output_templates as templates

# read version from installed package
from importlib.metadata import version
__version__ = version("wingwalker")