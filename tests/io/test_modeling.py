import json
from datetime import datetime

import pytest
import os

from numpy import long

from tests.utilities import call_gen_wing
from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs
from wingwalker.io.specs import parse_specfile
from wingwalker.models.enums import SpecFormat, Planform, WingType
from wingwalker.models.wing_model import WingModel

persist_dir = "out/io/persist"

try:
    os.makedirs(persist_dir)
except FileExistsError as fex:
    print(f'Directories {persist_dir} already exists')


def ticks():
    dt = datetime.now()
    return long((dt - datetime(1, 1, 1)).total_seconds() * 10000000)

@pytest.mark.io
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', 'lednicer'),
    ('data/lednicer_symmetrical_n0011sc-il.dat', 'lednicer'),
    ('data/selig_supercritical_nasa-sc2-1010.dat', 'selig'),
    ('data/selig_symmetrical_n0011sc-il.dat', 'selig')
])
def test_parse_specfile(spec_file, spec_format):
    dat_format = SpecFormat.LEDNICER if spec_format == 'lednicer' else SpecFormat.SELIG
    airfoil_data = parse_specfile(spec_file, dat_format)
    assert airfoil_data is not None, "AirfoilSpecs failed to load"
    assert airfoil_data.designation is not None, "Spec name was not read from the spec file"
    trace_pts = []
    for p in airfoil_data.trace(10.0, 0.0, False):
        trace_pts.append(p)

    assert len(trace_pts) > 0, "Failed to read trace points from spec"


@pytest.mark.io
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_elliptical_wing(
        spec_file: str,
        spec_format: SpecFormat
    ):

    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.ELLIPSE
    wing_req.wing_type = WingType.WING | WingType.RIGHT
    wing_req.span = 256.0
    wing_req.base_chord = 100.0
    wing_req.twist = -0.0349066
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = 10

    af_specs = get_airfoil_specs(wing_req)
    assert af_specs is not None, f'AirfoilSpecs failed to load with get_airfoil_specs({spec_file}) call'


@pytest.mark.io
@pytest.mark.parametrize('twist', [0.0, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 50])
@pytest.mark.parametrize('iterations', [10,20])
@pytest.mark.parametrize('planform', [Planform.RECTANGULAR, Planform.ELLIPSE, Planform.GEOMETRIC])
@pytest.mark.parametrize('structure_type', [WingType.WING, WingType.RUDDER])
@pytest.mark.parametrize('structure_position', [WingType.LEFT, WingType.RIGHT])
@pytest.mark.parametrize('structure_orientation', [WingType.VERTICAL, WingType.HORIZONTAL])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_wing_request(
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
        iterations: int
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

    """
    # Set up request
    req: WingRequest = WingRequest()
    req.planform = planform
    req.wing_type = structure_type | structure_position | structure_orientation
    req.span = span
    req.base_chord = base
    req.end_chord = end
    req.twist = twist
    req.spec_file = spec_file
    req.spec_format = spec_format
    req.iterations = iterations

    assert req.planform == planform, "Planform was not correct"
    assert req.wing_type == structure_type | structure_position | structure_orientation, "Wing type was not correct"
    assert req.span == span, "Span was not correct"
    assert req.base_chord == base, "Base chord was not correct"
    assert req.end_chord == end, "End chord was not correct"
    assert req.twist == twist, "Twist was not correct"
    assert req.iterations == iterations, "Iterations was not correct"
    assert req.spec_file == spec_file, "Spec file was not correct"
    assert req.spec_format == spec_format, "Spec format was not correct"


@pytest.mark.io
@pytest.mark.parametrize('is_left', [True, False])
@pytest.mark.parametrize('twist', [0.0, -0.0174533])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 50])
@pytest.mark.parametrize('iterations', [10,20])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_elliptical_permutations(
        spec_file: str,
        spec_format: SpecFormat,
        is_left: bool,
        twist: float,
        span: float,
        base: float,
        end: float,
        iterations: int
    ):
    """
    Test the full process of elliptical wing generation, from specs to 3D STL and screenshot files
    Args:
        spec_file:
        spec_format:
        is_left:
        twist:
        span:
        base:
        iterations:

    """
    # Set up request
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.ELLIPSE
    wing_req.wing_type = WingType.WING | (WingType.LEFT if is_left else WingType.RIGHT)
    wing_req.span = span
    wing_req.base_chord = base
    wing_req.end_chord = end
    wing_req.twist = twist
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = iterations

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Wing model failed to generate'

@pytest.mark.io
@pytest.mark.parametrize('is_left', [True, False])
@pytest.mark.parametrize('twist', [-0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [512.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 100])
@pytest.mark.parametrize('iterations', [10,20])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_rectangular_permutations(
        spec_file: str,
        spec_format: SpecFormat,
        is_left: bool,
        twist: float,
        span: float,
        base: float,
        end: float,
        iterations: int
    ):
    """
    Test the full process of elliptical wing generation, from specs to 3D STL and screenshot files
    Args:
        spec_file:
        spec_format:
        is_left:
        twist:
        span:
        base:
        iterations:

    """
    # Set up request
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.RECTANGULAR
    wing_req.wing_type = WingType.WING | (WingType.LEFT if is_left else WingType.RIGHT)
    wing_req.span = span
    wing_req.base_chord = base
    wing_req.end_chord = end
    wing_req.twist = twist
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = iterations

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Wing model failed to generate'

@pytest.mark.io
@pytest.mark.parametrize('is_left', [True, False])
@pytest.mark.parametrize('twist', [-0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 100])
@pytest.mark.parametrize('iterations', [20,30])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_geometric_permutations(
        spec_file: str,
        spec_format: SpecFormat,
        is_left: bool,
        twist: float,
        span: float,
        base: float,
        end: float,
        iterations: int
    ):
    """
    Test the full process of elliptical wing generation, from specs to 3D STL and screenshot files
    Args:
        spec_file:
        spec_format:
        is_left:
        twist:
        span:
        base:
        iterations:

    """
    # Set up request
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.GEOMETRIC
    wing_req.wing_type = WingType.WING | (WingType.LEFT if is_left else WingType.RIGHT)
    wing_req.span = span
    wing_req.base_chord = base
    wing_req.end_chord = end
    wing_req.twist = twist
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = iterations

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Wing model failed to generate'

@pytest.mark.io
@pytest.mark.disk
@pytest.mark.parametrize('planform', [Planform.RECTANGULAR, Planform.ELLIPSE, Planform.GEOMETRIC])
@pytest.mark.parametrize('side', [WingType.LEFT, WingType.RIGHT])
@pytest.mark.parametrize('wing_type', [WingType.WING, WingType.RUDDER, WingType.ELEVATOR])
@pytest.mark.parametrize('twist', [-0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [512.0])
@pytest.mark.parametrize('base', [128.0])
@pytest.mark.parametrize('end', [0, 10, 100])
@pytest.mark.parametrize('iterations', [10,20])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_wing_request_io(
        spec_file: str,
        spec_format: SpecFormat,
        planform: Planform,
        side: WingType,
        wing_type: WingType,
        twist: float,
        span: float,
        base: float,
        end: float,
        iterations: int
    ):
    """
    Test the full process of elliptical wing generation, from specs to 3D STL and screenshot files
    Args:
        spec_file: input file,
        spec_format: airfoil format,
        planform: shape of wing,
        side: left or right structure,
        wing_type: wing, rudder, or elevator,
        twist: aerodynamic twist,
        span: length of wing,
        base: base chord length,
        end: end chord length,
        iterations: number of iterations between base and end

    """
    # Set up request
    wing_req: WingRequest = WingRequest()
    wing_req.planform = planform
    wing_req.wing_type = side | wing_type
    wing_req.span = span
    wing_req.base_chord = base
    wing_req.end_chord = end
    wing_req.twist = twist
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = iterations

    curr_ticks = ticks()
    outfile = f'{persist_dir}/{ticks()}.json'

    with open(outfile, 'w', encoding='utf-8') as fout:
        fout.write(wing_req.to_json())

    stored_req: WingRequest
    with open(outfile, 'r', encoding='utf-8') as fin:
        json_str = fin.read()
        stored_req = WingRequest.from_json(json_str)

    assert wing_req is not None, 'Wing request was null'
    assert stored_req is not None, 'Stored request failed to reload'

    assert wing_req == stored_req, 'Stored wing request is not the same as the original request'
    # cleanup
    os.remove(outfile)