import pymeshlab
import numpy as np

from wingwalker.generators.wing import generate_point_cloud_array
from wingwalker.models.wing_model import WingModel


def transform_to_pml_mesh(model: WingModel)->pymeshlab.Mesh:
    """
    Utility function to generate a pymeshlab.Mesh object from a wing model's point cloud
    Args:
        model: Input airfoil model

    Returns:
        An unprocessed pymeshlab.Mesh instance with the raw vertices from the model's point cloud
    """
    vert_array: np.ndarray = generate_point_cloud_array(model)
    mesh = pymeshlab.Mesh(vertex_matrix=vert_array)
    return mesh

def generate_closed_mesh(model: WingModel)->pymeshlab.MeshSet:
    """
    Takes a wing model, converts it to a pymeshlab.Mesh, and then adds that to a pymeshlab.MeshSet.

    The MeshSet has a standard set of filters applied to turn the point cloud into a closed model, suitable for exporting as
    an STL file.
    Args:
        model:  The input airfoil model

    Returns:
        A filtered and closed pymeshlab.MeshSet instance, containing a single Mesh.
    """
    mesh_set: pymeshlab.MeshSet = pymeshlab.MeshSet()
    model_mesh = transform_to_pml_mesh(model)
    mesh_set.add_mesh(model_mesh, model.identifier)
    mesh_set.compute_normal_for_point_clouds(k=10)
    mesh_set.meshing_close_holes(maxholesize=300)
    return mesh_set
