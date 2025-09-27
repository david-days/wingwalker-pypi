from wingwalker.base import Reader
from wingwalker.lednicer import Parser as LednicerParser, parse_lednicer
from wingwalker.models.airfoil_specs import AirfoilSpecs
from wingwalker.selig import Parser as SeligParser, parse_selig
from wingwalker.models.enums import SpecFormat

reader: Reader

def parse_specfile(src: str, spec_format: SpecFormat)-> AirfoilSpecs:
    global reader
    match spec_format:
        case SpecFormat.SELIG:
            reader = SeligParser(src)
        case SpecFormat.LEDNICER:
            reader = LednicerParser(src)
        case SpecFormat.UNDEFINED:
            raise NotImplementedError("input file format must be defined as SELIG or LEDNICER")

    xarr, yarr, spec_name = reader.read()
    return AirfoilSpecs(src, spec_name, xarr, yarr)
