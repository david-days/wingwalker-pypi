import os
import pymeshlab

from wingwalker.generators.wing import generate_point_cloud_polydata, generate_point_cloud_array
from wingwalker.models.wing_model import WingModel
from wingwalker.processing.mesh import generate_closed_mesh


def export_stl(wing_model: WingModel, stl_filename: str) -> None:
    """
    Given a wing model, go through the process to generate and export a closed mesh as an STL
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

    mesh_set: pymeshlab.MeshSet = generate_closed_mesh(model=wing_model)
    mesh_set.save_current_mesh(file_name=stl_filename)
    stats = os.stat(stl_filename)
    print(f'Wing model processed and saved to {stl_filename}')
    print(stats)


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

    point_cloud = generate_point_cloud_polydata(wing_model)
    point_cloud.save(filename=ply_filename, binary=True)

    stats = os.stat(ply_filename)
    print(f'Wing model saved to {ply_filename}')
    print(stats)
    print()