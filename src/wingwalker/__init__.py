from wingwalker.selig import (
    parse_selig,
    Parser as SeligParser
)
# read version from installed package
from importlib.metadata import version
__version__ = version("wingwalker")