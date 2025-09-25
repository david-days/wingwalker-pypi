import pytest
import os
from pyvista import PolyData, Plotter

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs, get_lambdas, generate_wing, generate_mesh
from wingwalker.io.specs import parse_specfile
from wingwalker.models.enums import SpecFormat, Planform, WingType


@pytest.mark.threeD
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
    wing_req.planform = Planform.RECTANGULAR
    wing_req.wing_type = WingType.WING | WingType.RIGHT
    wing_req.span = 256.0
    wing_req.base_cord = 100.0
    wing_req.twist = -0.0349066
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = 10

    af_specs = get_airfoil_specs(wing_req)
    assert af_specs is not None, f'AirfoilSpecs failed to load with get_airfoil_specs({spec_file}) call'


@pytest.mark.threeD
@pytest.mark.io
@pytest.mark.parametrize('is_left', [True, False])
@pytest.mark.parametrize('twist', [0.0, -0.0174533, -0.0349066])
@pytest.mark.parametrize('span', [256.0, 512.0])
@pytest.mark.parametrize('base', [128.0, 100])
@pytest.mark.parametrize('iterations', [10,20,30])
@pytest.mark.parametrize('spec_file,spec_format', [
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', SpecFormat.LEDNICER),
    ('data/selig_symmetrical_n0011sc-il.dat', SpecFormat.SELIG),
])
def test_elliptical_wing(
        spec_file: str,
        spec_format: SpecFormat,
        is_left: bool,
        twist: float,
        span: float,
        base: float,
        iterations: int,
        write_dir: str = 'out/io/wings'
    ):
    try:
        os.makedirs(write_dir)
    except FileExistsError:
        pass

    # Set up request
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.ELLIPSE
    wing_req.wing_type = WingType.WING | (WingType.LEFT if is_left else WingType.RIGHT)
    wing_req.span = span
    wing_req.base_cord = base
    wing_req.twist = twist
    wing_req.spec_file = spec_file
    wing_req.spec_format = spec_format
    wing_req.iterations = iterations

    # load specs
    af_specs = get_airfoil_specs(wing_req)
    assert af_specs is not None, f'AirfoilSpecs failed to load'

    # Get lambdas
    c_func, t_func, z_func, area_func = get_lambdas(wing_req)

    assert c_func is not None, f'chord lambda failed to load'
    assert t_func is not None, f'twist lambda failed to load'
    assert z_func is not None, f'z lambda failed to load'
    assert area_func is not None, f'area lambda failed to load'

    # Generate the actual wing model
    elliptical_wing = generate_wing(wing_req, af_specs, c_func, t_func, z_func, area_func)

    assert elliptical_wing is not None, f'Wing model failed to generate'

    # Get the mesh
    wing_mesh: PolyData = generate_mesh(elliptical_wing)

    assert wing_mesh is not None, f'Mesh from model failed to generate'
    # Write out .stl
    outbase = f'{write_dir}/elliptical_{spec_format.name}_{is_left}_{twist}_{span}_{base}_{iterations}'
    wing_mesh.save(filename=f'{outbase}.stl',recompute=True)
    assert os.path.isfile(f'{outbase}.stl'), f'Wing mesh failed save to {outbase}.stl'

    # Save screenshot
    plotter = Plotter(off_screen=True)
    plotter.add_mesh(wing_mesh, color='blue')
    plotter.show(screenshot=f'{outbase}.png')
    assert os.path.isfile(f'{outbase}.png'), f'Wing mesh failed save screenshot to {outbase}.png'