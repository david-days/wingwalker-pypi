import numpy as np
from pyvista import PolyData
from shapely.geometry import Point
import pyvista as pv

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.elliptical import EllipticalFunctor, EllipticalSectionFunctor
from wingwalker.generators.geometric import GeometricFunctor, GeometricSectionFunctor
from wingwalker.generators.iterators import TIterator
from wingwalker.generators.rectangular import RectangularFunctor, RectangularSectionFunctor
from wingwalker.models.airfoil_section import AirfoilSection
from wingwalker.models.airfoil_specs import AirfoilSpecs
from wingwalker.models.enums import Planform
from wingwalker.io import specs
from wingwalker.models.wing_model import WingModel


def get_lambdas(build_params: WingRequest):
    """
    Function to return the correct set of chord(t), twist(t), and z(t) lambdas for the
    given request
    Args:
        build_params: Specifications for the wing to be built

    Returns:
        Tuple of (in order): chord(t), twist(t), z(t), area()
    """
    match build_params.planform:
        case Planform.RECTANGULAR:
            rect = RectangularFunctor(build_params)
            return rect.chord_func(), rect.twist_func(), rect.z_func(), rect.area_func()
        case Planform.ELLIPSE:
            ell = EllipticalFunctor(build_params)
            return ell.chord_func(), ell.twist_func(), ell.z_func(), ell.area_func()
        case Planform.GEOMETRIC:
            geo = GeometricFunctor(build_params)
            return geo.chord_func(), geo.twist_func(), geo.z_func(), geo.area_func()
        case _:
            raise ValueError(f'Unknown planform {build_params.planform.name}')

def get_section_lambdas(build_params: WingRequest, idx: int):
    """
    Functino to return the correct set of chord(t), twist(t), z(t) lambdas for the given subsection of the request
    Args:
        build_params: Specifications for the entire wing to be built
        sections: array of section size/weight values.  Will be normalized under the hood
        idx: Index of the current subsection

    Returns:
        tuple of (in order): chord(t), twist(t), z(t), area()
    """
    match build_params.planform:
        case Planform.RECTANGULAR:
            rect = RectangularSectionFunctor(build_params=build_params, idx=idx)
            return rect.chord_func(), rect.twist_func(), rect.z_func(), rect.area_func()
        case Planform.ELLIPSE:
            ell = EllipticalSectionFunctor(build_params=build_params, idx=idx)
            return ell.chord_func(), ell.twist_func(), ell.z_func(), ell.area_func()
        case Planform.GEOMETRIC:
            geo = GeometricSectionFunctor(build_params=build_params, idx=idx)
            return geo.chord_func(), geo.twist_func(), geo.z_func(), geo.area_func()
        case _:
            raise ValueError(f'Unknown planform {build_params.planform.name}')


def get_airfoil_specs(build_params: WingRequest)->AirfoilSpecs:
    """
    Reads in specifications from the given source
    Args:
        build_params: Wing specifications

    Returns:
        AirfoilSpecs: AirfoilSpecs object
    """
    src_file = build_params.spec_file
    src_format = build_params.spec_format
    spec_data = specs.parse_specfile(src_file, src_format)
    print(spec_data.__repr__())
    return spec_data

def transform_matrix_z(theta_rad: float, centroid: Point)-> np.ndarray[tuple[float, float]]:
    """
    Create the rotations/translation matrix about the z-axis.  The resulting matrix will
    rotate the points about the z axis by the given angle (in radians), and translate from the centroid back
    to [0,0,z]
    Args:
        theta_rad: angle in radians to rotate about the z-axis
        centroid: centroid of the airfoil, used to translate the centroid back to 0,0,z

    Returns:
        A numpy transformation matrix that rotates about the z-axis by the given angle and translates
        all positions by origin - centroid
    """
    transform_matrix = [
        [np.cos(theta_rad), -np.sin(theta_rad), 0, -1.0*centroid.x],
        [np.sin(theta_rad), np.cos(theta_rad), 0, -1.0*centroid.y],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    return np.array(transform_matrix, dtype=float)

def generate_section(chord: float, twist: float, z: float, mirror: bool, af_specs: AirfoilSpecs)->AirfoilSection:
    """
    Generated an airfoil section from the given specs and parameters
    Args:
        chord: length of the section chord
        twist: twist relative to the base
        z: distance from the base
        mirror: mirrored (left)
        af_specs: airfoil specifications

    Returns:
        AirfoilSection meeting the requirements
    """
    centroid = af_specs.centroid(chord, z, mirror)
    tform = transform_matrix_z(twist, centroid)
    coords: list[Point] = []
    for p in af_specs.trace(chord, z, mirror):
        vect = np.array([ p.x, p.y, p.z, 1.0], dtype=float)
        vect_prime = tform @ vect
        coords.append(Point(vect_prime[0], vect_prime[1], vect_prime[2]))

    return AirfoilSection(coords=coords, chord=chord, z_index=z, twist=twist, spec_name=af_specs.designation)

def generate_wing(wing_params: WingRequest, af_specs: AirfoilSpecs, c_func, twist_func, z_func, area_func)->WingModel:
    """
    Produces a wing from the given specs, parametrized functions, and requirements.
    Args:
        wing_params: requirements for the wing
        af_specs: airfoil specifications
        c_func: function(t) for chord length at param t
        twist_func: function(t) for twist at param t
        z_func: function(t) for z at param t
        area_func: function to calculate area of the wing

    Returns:
        WingModel instance containing the 3D sections and basic parameters for the wing
    """
    # Set up iteration outward along the length of the wing span
    t_iter = TIterator(wing_params)
    sections: list[AirfoilSection] = []
    # Iterate for t from the base to the end of the wing, collecting up the transformed coordinates
    for t in t_iter:
        c = c_func(t)
        twist = twist_func(t)
        z = z_func(t)
        sect = generate_section(c, twist, z, wing_params.mirrored, af_specs)
        sections.append(sect)

    # Compile everything into a WingModel instance
    wing_model = WingModel(wing_params, af_specs, sections)
    wing_model.base_chord = wing_params.base_chord
    wing_model.end_chord = wing_params.end_chord
    wing_model.span = wing_params.span
    wing_model.area = area_func()

    print('Wing generation complete')
    print(wing_model.__repr__())
    return wing_model


def generate_wing_model(wing_req)->WingModel:
    """
    Generate a wing model from the given request
    Args:
        wing_req:
            WingRequest object representing the required specs
    Returns:
        a standard wing model
    """
    # load specs
    af_specs = get_airfoil_specs(wing_req)
    # Get lambdas
    c_func, t_func, z_func, area_func = get_lambdas(wing_req)
    # Generate the actual wing model
    wing_model = generate_wing(
        wing_params=wing_req,
        af_specs=af_specs,
        c_func=c_func,
        twist_func=t_func,
        z_func=z_func,
        area_func=area_func
    )
    return wing_model

def generate_wing_subsection(wing_req: WingRequest, idx: int)->WingModel:
    """
    Generate a wing subsection from the given specs
    Args:
        wing_req: WingRequest object representing the required specs
        idx: Current subsection index to be generated

    Returns:
        WingModel containing the subsection values and specs
    """
    # load specs
    af_specs = get_airfoil_specs(wing_req)
    # get lambdas
    c_func, t_func, z_func, area_func = get_section_lambdas(wing_req, idx)
    # generate section of wing
    wing_section = generate_wing(
        wing_params=wing_req,
        af_specs=af_specs,
        c_func=c_func,
        twist_func=t_func,
        z_func=z_func,
        area_func=area_func
    )
    return wing_section

def create_wing(wing_req: WingRequest) -> WingModel | list[WingModel]:
    """
    Convenience function for creating a wing, either whole or in subsections, from the given specs
    Args:
        wing_req:
            WingRequest object representing the required specs
    Returns:
        If wing_req.sections is null or empty, WingModel instance containing the entire 3D model; otherwise,
        returns a list of WingModels representing the sections
    """
    af_specs = get_airfoil_specs(wing_req)
    if wing_req.sections is None or wing_req.sections == [] or len(wing_req.sections) == 0:
        whole_model = generate_wing_model(wing_req)
        return whole_model
    else:
        # Gather up the subsections
        wing_sections: list[WingModel] = []
        for idx, part in enumerate(wing_req.sections):
            section = generate_wing_subsection(wing_req, idx)
            wing_sections.append(section)
        # Give back the model pieces
        return wing_sections

def generate_point_cloud_array(model: WingModel)->np.ndarray:
    """
    Generate a numpy array holding the vertices from the given wing model data
    Args:
        model: Wing model to be converted to a mesh

    Returns:
        Numpy array holding the vertices from the given wing model
    """
    # Compile point values
    x_coords = []
    y_coords = []
    z_coords = []
    for s in model:
        for p in s:
            x_coords.append(p.x)
            y_coords.append(p.y)
            z_coords.append(p.z)
    # Create numpy mesh array
    xarr = np.array(x_coords)
    yarr = np.array(y_coords)
    zarr = np.array(z_coords)
    wing_points = np.c_[xarr.reshape(-1), yarr.reshape(-1), zarr.reshape(-1)]
    return wing_points

def generate_point_cloud_polydata(model: WingModel)->PolyData:
    """
    Generate a 3D mesh from the given wing model data
    Args:
        model: Wing model to be converted to a mesh

    Returns:
        PyVista PolyData instance containing the 3D mesh
    """
    wing_points = generate_point_cloud_array(model)
    wing_cloud = pv.PolyData(wing_points)
    return wing_cloud

