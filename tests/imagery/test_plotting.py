import pytest
from pyvista import PolyData, Plotter

from tests.utilities import get_standard_elliptical, get_standard_rectangular, get_standard_geometric
from wingwalker.generators.wing import generate_point_cloud
from wingwalker.models.enums import WingType
from wingwalker.models.wing_model import WingModel


def plot_results(model: WingModel, points: PolyData, mesh: PolyData):
    title = f'{model.wing_params.wing_type} - {model.wing_params.planform.name}'
    pl = Plotter(shape=(1,2))
    pl.add_title(title)
    mesh_view = pl.add_mesh(mesh, color='yellow', line_width=0.5, show_edges=True)
    pl.subplot(0,1)
    point_view = pl.add_mesh(points, color='blue')
    pl.show()

@pytest.mark.display
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_elliptical_plots(wing_side: WingType):
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
    p_cloud: PolyData = generate_point_cloud(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0
    # Try to generate a surface mesh
    surface_mesh = p_cloud.reconstruct_surface()
    assert surface_mesh is not None
    assert surface_mesh.n_points > 0
    assert surface_mesh.n_cells > 0
    plot_results(model, p_cloud, surface_mesh)

@pytest.mark.display
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_rectangular_plots(wing_side: WingType):
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
    p_cloud: PolyData = generate_point_cloud(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0
    assert p_cloud is not None
    # Try to generate a surface mesh
    surface_mesh = p_cloud.reconstruct_surface()
    assert surface_mesh is not None
    assert surface_mesh.n_points > 0
    assert surface_mesh.n_cells > 0
    plot_results(model, p_cloud, surface_mesh)

@pytest.mark.display
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_geometric_plots(wing_side: WingType):
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
    p_cloud: PolyData = generate_point_cloud(model)
    assert p_cloud is not None
    assert p_cloud.n_points > 0
    # Try to generate a surface mesh
    surface_mesh = p_cloud.reconstruct_surface()
    assert surface_mesh is not None
    assert surface_mesh.n_points > 0
    assert surface_mesh.n_cells > 0
    plot_results(model, p_cloud, surface_mesh)