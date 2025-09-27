import pytest

from tests.utilities import call_gen_wing
from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs
from wingwalker.io.specs import parse_specfile
from wingwalker.models.enums import SpecFormat, Planform, WingType
from wingwalker.models.wing_model import WingModel


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
@pytest.mark.parametrize('twist', [0.0, -0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0, 100])
@pytest.mark.parametrize('end', [0, 10, 50, 100])
@pytest.mark.parametrize('iterations', [10,20,30])
@pytest.mark.parametrize('planform', [Planform.RECTANGULAR, Planform.ELLIPSE, Planform.GEOMETRIC])
@pytest.mark.parametrize('structure_type', [WingType.WING, WingType.ELEVATOR, WingType.RUDDER])
@pytest.mark.parametrize('structure_position', [WingType.LEFT, WingType.RIGHT, WingType.UNDEFINED])
@pytest.mark.parametrize('structure_orientation', [WingType.VERTICAL, WingType.HORIZONTAL, WingType.UNDEFINED])
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
@pytest.mark.parametrize('twist', [0.0, -0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0, 100])
@pytest.mark.parametrize('end', [0, 10, 50, 100])
@pytest.mark.parametrize('iterations', [10,20,30])
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
@pytest.mark.parametrize('twist', [0.0, -0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0, 100])
@pytest.mark.parametrize('end', [0, 10, 50, 100])
@pytest.mark.parametrize('iterations', [10,20,30])
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
@pytest.mark.parametrize('twist', [0.0, -0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0, 100])
@pytest.mark.parametrize('end', [0, 10, 50, 100])
@pytest.mark.parametrize('iterations', [10,20,30])
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

