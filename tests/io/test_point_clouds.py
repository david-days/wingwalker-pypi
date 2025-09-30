import pytest
from pyvista import PolyData

from tests.utilities import get_standard_elliptical, get_standard_rectangular, get_standard_geometric
from wingwalker.generators.wing import generate_point_cloud_polydata
from wingwalker.models.enums import WingType
from wingwalker.models.wing_model import WingModel


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_elliptical_point_cloud(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_elliptical(wing_side)
    assert model is not None
    p_cloud: PolyData = generate_point_cloud_polydata(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_rectangular_point_cloud(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_rectangular(wing_side)
    assert model is not None
    p_cloud: PolyData = generate_point_cloud_polydata(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0
    assert p_cloud is not None


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_geometric_point_cloud(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_geometric(wing_side)
    assert model is not None
    p_cloud: PolyData = generate_point_cloud_polydata(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0
    # Try to generate a surface mesh
    surface_mesh = p_cloud.reconstruct_surface()
    assert surface_mesh is not None
    assert surface_mesh.n_points > 0
    assert surface_mesh.n_cells > 0

@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_elliptical_mesh(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_elliptical(wing_side)
    assert model is not None

@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_rectangular_mesh(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_rectangular(wing_side)
    assert model is not None

@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_geometric_mesh(wing_side: WingType):
    """
    Takes a standard model generation and attempts to create a PyVista point cloud out of it
    Args:
        wing_side:
            Left or right
    Returns:
        None
    """
    model: WingModel = get_standard_geometric(wing_side)
    assert model is not None
