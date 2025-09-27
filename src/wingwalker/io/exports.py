import os

from wingwalker.generators.wing import generate_surface_mesh, generate_point_cloud
from wingwalker.models.wing_model import WingModel


def export_stl(wing_model: WingModel, stl_filename: str) -> None:
    """
    Given a wing model, go through the process to generate and export a surface mesh as an STL
    Args:
        wing_model: Model data to be exported
        stl_filename: file name to save the stl_file

    Returns:
        None
    """
    print(f'Exporting wing model to {stl_filename}')
    print(wing_model.__repr__())

    if not stl_filename.endswith('.stl'):
        stl_filename += '.stl'

    surface_mesh = generate_surface_mesh(wing_model)
    surface_mesh.save(filename=stl_filename, binary=True)

    stats = os.stat(stl_filename)
    print(f'Wing model saved to {stl_filename}')
    print(stats)

def export_vtk(wing_model: WingModel, vtk_filename: str) -> None:
    """
    Given a wing model, got through the process to generate a VTP point cloud file
    Args:
        wing_model: model to be exported
        vtk_filename: path and file name for the VTP file

    Returns:
        None
    """
    print(f'Exporting wing model to {vtk_filename}')
    print(wing_model.__repr__())

    if not vtk_filename.endswith('.vtk'):
        vtk_filename += '.vtk'

    point_cloud = generate_point_cloud(wing_model)
    point_cloud.save(filename=vtk_filename, binary=True)

    stats = os.stat(vtk_filename)
    print(f'Wing model saved to {vtk_filename}')
    print(stats)
    print()

def export_ply(wing_model: WingModel, ply_filename: str) -> None:
    """
    Given a wing model, got through the process to generate a PLY file
    Args:
        wing_model: model to be exported
        ply_filename: path and file name for the PLY file

    Returns:
        None
    """
    print(f'Exporting wing model to {ply_filename}')
    print(wing_model.__repr__())

    if not ply_filename.endswith('.ply'):
        ply_filename += '.ply'

    point_cloud = generate_point_cloud(wing_model)
    point_cloud.save(filename=ply_filename, binary=True)

    stats = os.stat(ply_filename)
    print(f'Wing model saved to {ply_filename}')
    print(stats)
    print()