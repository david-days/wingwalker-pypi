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
    mesh_set.generate_surface_reconstruction_ball_pivoting()

    # Chant the invocation no more than 4 times...
    nm_counts = get_non_manifold_counts(mesh_set)
    clean_count: int = 0
    while clean_count < 4 and (nm_counts[0] > 0 or nm_counts[1] > 0 or nm_counts[2] > 0):
        print(f'\tnon-manifold: vertices={nm_counts[0]}, edges={nm_counts[1]}, holes={nm_counts[2]}')
        if nm_counts[1] > 0:
            mesh_set.meshing_repair_non_manifold_edges(method=1)
        if nm_counts[0] > 0:
            mesh_set.meshing_repair_non_manifold_vertices(vertdispratio=0.0)
        mesh_set.meshing_close_holes(maxholesize=300)
        clean_count += 1
        nm_counts = get_non_manifold_counts(mesh_set)

    print(f'Final non-manifold: vertices={nm_counts[0]}, edges={nm_counts[1]}, holes={nm_counts[2]}, cycles={clean_count}')
    return mesh_set

def get_non_manifold_counts(mesh_set: pymeshlab.MeshSet):
    mesh_set.compute_selection_by_non_manifold_per_vertex()
    nm_vert_count = mesh_set.current_mesh().selected_vertex_number()

    mesh_set.compute_selection_by_non_manifold_edges_per_face()
    nm_edge_count = mesh_set.current_mesh().selected_face_number()

    topo_stats = mesh_set.get_topological_measures()

    return nm_vert_count, nm_edge_count, topo_stats['number_holes']

