from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs, get_lambdas, generate_wing
from wingwalker.models.enums import WingType, Planform, SpecFormat
from wingwalker.models.wing_model import WingModel


def call_gen_wing(wing_req: WingRequest)->WingModel:
    """
    Core process for generating a wing model from the request.

    Standard to all processes, so defined here to avoid code repetition

    Args:
        wing_req:
            WingRequest object
    Returns:
        WingModel of build
    """
    # load specs
    af_specs = get_airfoil_specs(wing_req)
    assert af_specs is not None, 'AirfoilSpecs failed to load'

    # Get lambdas
    c_func, t_func, z_func, area_func = get_lambdas(wing_req)

    assert c_func is not None, 'chord lambda failed to load'
    assert t_func is not None, 'twist lambda failed to load'
    assert z_func is not None, 'z lambda failed to load'
    assert area_func is not None, 'area lambda failed to load'

    # Generate the actual wing model
    wing_model = generate_wing(wing_req, af_specs, c_func, t_func, z_func, area_func)

    return wing_model

def get_standard_elliptical(wing_dir: WingType)->WingModel:
    """
    Generate a standard elliptical wing model
    Args:
        wing_dir:
            WingType.LEFT or WingType.RIGHT
    Returns:
        a standard wing model, elliptical planform
    """
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.ELLIPSE
    wing_req.wing_type = WingType.WING | wing_dir
    wing_req.span = 200
    wing_req.base_chord = 64
    wing_req.end_chord = 0.0
    wing_req.twist = -0.0349066
    wing_req.spec_file = 'data/lednicer_supercritical_nasa-sc2-1010.dat'
    wing_req.spec_format = SpecFormat.LEDNICER
    wing_req.iterations = 300

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Elliptical wing generation failed'
    print(wing_model.__repr__())
    return wing_model


def get_standard_rectangular(wing_dir: WingType) -> WingModel:
    """
    Generate a standard rectangular wing model
    Args:
        wing_dir:
            WingType.LEFT or WingType.RIGHT
    Returns:
        a standard wing model, rectangular planform
    """
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.RECTANGULAR
    wing_req.wing_type = WingType.WING | wing_dir
    wing_req.span = 200
    wing_req.base_chord = 96
    wing_req.end_chord = 0.0
    wing_req.twist = -0.0349066
    wing_req.spec_file = 'data/lednicer_supercritical_nasa-sc2-1010.dat'
    wing_req.spec_format = SpecFormat.LEDNICER
    wing_req.iterations = 100

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Rectangular wing generation failed'
    print(wing_model.__repr__())
    return wing_model

def get_standard_geometric(wing_dir: WingType) -> WingModel:
    """
    Generate a standard rectangular wing model
    Args:
        wing_dir:
            WingType.LEFT or WingType.RIGHT
    Returns:
        a standard wing model, rectangular planform
    """
    wing_req: WingRequest = WingRequest()
    wing_req.planform = Planform.GEOMETRIC
    wing_req.wing_type = WingType.WING | wing_dir
    wing_req.span = 200
    wing_req.base_chord = 128
    wing_req.end_chord = 64
    wing_req.twist = -0.0349066
    wing_req.spec_file = 'data/lednicer_supercritical_nasa-sc2-1010.dat'
    wing_req.spec_format = SpecFormat.LEDNICER
    wing_req.iterations = 100

    wing_model: WingModel = call_gen_wing(wing_req)

    assert wing_model is not None, 'Geometric wing generation failed'
    print(wing_model.__repr__())
    return wing_model

