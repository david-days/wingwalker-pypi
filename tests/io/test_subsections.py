import os

import pytest

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import create_wing
from wingwalker.models.enums import WingType, Planform, SpecFormat
from wingwalker.models.wing_model import WingModel

@pytest.mark.threeD
@pytest.mark.parametrize('twist', [-0.0174533])
@pytest.mark.parametrize('span', [512.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 50])
@pytest.mark.parametrize('iterations', [10, 20])
@pytest.mark.parametrize('planform', [Planform.RECTANGULAR, Planform.ELLIPSE, Planform.GEOMETRIC])
@pytest.mark.parametrize('structure_type', [WingType.WING, WingType.RUDDER])
@pytest.mark.parametrize('structure_position', [WingType.LEFT, WingType.RIGHT])
@pytest.mark.parametrize('structure_orientation', [WingType.VERTICAL, WingType.HORIZONTAL])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
@pytest.mark.parametrize('sections', [None, [], [400], [1,1,2]])
def test_sectioned_request(
        spec_file: str,
        spec_format: SpecFormat,
        planform: Planform,
        structure_type: WingType,
        structure_position: WingType,
        structure_orientation: WingType,
        twist: float,
        span: float,
        base: float,
        end: float,
        iterations: int,
        sections: list[float]
    ):
    """
    Test the setup of the wing request
    Args:
        spec_file:
        spec_format:
        twist:
        span:
        base:
        iterations:
        sections:
    """
    # Set up request
    sect_req: WingRequest = WingRequest()
    sect_req.planform = planform
    sect_req.wing_type = structure_type | structure_position | structure_orientation
    sect_req.span = span
    sect_req.base_chord = base
    sect_req.end_chord = end
    sect_req.twist = twist
    sect_req.spec_file = spec_file
    sect_req.spec_format = spec_format
    sect_req.iterations = iterations
    sect_req.sections = sections

    wing_result = create_wing(sect_req)
    assert wing_result is not None, 'Received None for the wing generation'
    # If no section info, we expect a WingModel, otherwise we expect an array
    if sections is not None and len(sections) > 0:
        assert isinstance(wing_result,list), 'Expected array of subsections'
        piece_count = len(wing_result)
        section_count = len(sections)
        assert piece_count == section_count, f'Expected {section_count} subsections but got {piece_count}'
    else:
        assert isinstance(wing_result, WingModel), 'Expected a single wingmodel but got something else'


