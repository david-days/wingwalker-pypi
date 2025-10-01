import os

import pytest

from tests.utilities import get_standard_elliptical, get_standard_rectangular, get_standard_geometric
from wingwalker.io.exports import export_stl, export_ply
from wingwalker.models.enums import WingType
from wingwalker.models.wing_model import WingModel

stl_dir = 'out/io/stl/'
ply_dir = 'out/io/ply/'

try:
    os.makedirs(stl_dir)
except FileExistsError as fex:
    print(f'Directories {stl_dir} already exists')

try:
    os.makedirs(ply_dir)
except FileExistsError as fex:
    print(f'Directories {ply_dir} already exists')

@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_elliptical_wing_stl(wing_side: WingType):
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

    f_name = os.path.join(stl_dir, f'elliptical_wing_{wing_side.name}.stl')
    if os.path.exists(f_name):
        os.remove(f_name)
    export_stl(model, f_name)
    assert os.path.exists(f_name)


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_rectangular_wing_stl(wing_side: WingType):
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

    f_name = os.path.join(stl_dir, f'rectangular_wing_{wing_side.name}.stl')
    if os.path.exists(f_name):
        os.remove(f_name)

    export_stl(model, f_name)
    assert os.path.exists(f_name)


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_geometric_wing_stl(wing_side: WingType):
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

    f_name = os.path.join(stl_dir, f'geometric_wing_{wing_side.name}.stl')
    if os.path.exists(f_name):
        os.remove(f_name)

    export_stl(model, f_name)
    assert os.path.exists(f_name)

@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_elliptical_wing_ply(wing_side: WingType):
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

    f_name = os.path.join(ply_dir, f'elliptical_wing_{wing_side.name}.ply')
    if os.path.exists(f_name):
        os.remove(f_name)
    export_ply(model, f_name)
    assert os.path.exists(f_name)


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_rectangular_wing_ply(wing_side: WingType):
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

    f_name = os.path.join(ply_dir, f'rectangular_wing_{wing_side.name}.ply')
    if os.path.exists(f_name):
        os.remove(f_name)

    export_ply(model, f_name)
    assert os.path.exists(f_name)


@pytest.mark.threeD
@pytest.mark.parametrize('wing_side', [WingType.LEFT, WingType.RIGHT])
def test_geometric_wing_ply(wing_side: WingType):
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

    f_name = os.path.join(ply_dir, f'geometric_wing_{wing_side.name}.ply')
    if os.path.exists(f_name):
        os.remove(f_name)

    export_ply(model, f_name)
    assert os.path.exists(f_name)