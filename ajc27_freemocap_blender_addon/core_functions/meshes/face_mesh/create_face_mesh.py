from typing import Tuple, List

import bpy
import numpy as np

from ajc27_freemocap_blender_addon.data_models.mediapipe_names.face_mesh_connections import  get_mediapipe_face_mesh_connections, create_mediapipe_face_mesh_faces


def create_face_mesh(file_path: str):
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.endswith(".npy"):
        raise ValueError(f"File must be a .npy file: {file_path}")

    face_frame_id_xyz = np.load(file_path) * .001  # convert from mm to m

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name="FaceMesh")
    obj = bpy.data.objects.new(name="FaceMeshObject", object_data=mesh)

    # Link the object to the current scene
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # Set the object as the active object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    verticies = []
    frame_number = 100  # just use a random frame from the middle for now
    for vertex_id in range(face_frame_id_xyz.shape[1]):
        # blender defines vertices as tuples of 3 floats - (x, y, z)
        verticies.append(tuple(face_frame_id_xyz[frame_number, vertex_id, :]))
    edges = get_mediapipe_face_mesh_connections()
    faces = create_mediapipe_face_mesh_faces()
    # Create the mesh with the vertices
    mesh.from_pydata(verticies, edges, faces)

    # Update the mesh with new data
    mesh.update()

    print("Vertices loaded successfully!")


if __name__ == "__main__":
    from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path
    from pathlib import Path

    test_data_path = get_test_recording_path()
    face_mesh_npy_file = str(Path(test_data_path) / "output_data" / "mediapipe_face_3d_xyz.npy")
    # Call the function to load vertices
    create_face_mesh(file_path=face_mesh_npy_file)
