import bpy
import numpy as np

from ajc27_freemocap_blender_addon.data_models.mediapipe_names.face_mesh_connections import \
    get_mediapipe_face_mesh_connections, create_mediapipe_face_mesh_faces


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
    reference_frame = 100
    mean_vertex_position = np.nanmean(face_frame_id_xyz[reference_frame, :, :], axis=0)
    vertices = [tuple(face_frame_id_xyz[100, vertex_id, :] + mean_vertex_position) for vertex_id in
                range(face_frame_id_xyz.shape[1])]

    edges = get_mediapipe_face_mesh_connections()
    faces = create_mediapipe_face_mesh_faces()
    # Create the initial mesh with the vertices
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    # Create shape keys for each frame
    obj.shape_key_add(name="Basis")  # Add the basis/key 0 shape key
    for frame_number in range(face_frame_id_xyz.shape[0]):
        shape_key = obj.shape_key_add(name=f"Frame_{frame_number}")
        for vertex_id in range(face_frame_id_xyz.shape[1]):
            shape_key.data[vertex_id].co = face_frame_id_xyz[frame_number, vertex_id, :]

        # Insert keyframe for this shape key
        shape_key.value = 1.0
        shape_key.keyframe_insert(data_path="value", frame=frame_number)

    print("Face mesh animation created successfully!")


if __name__ == "__main__":
    from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path
    from pathlib import Path

    test_data_path = get_test_recording_path()
    face_mesh_npy_file = str(Path(test_data_path) / "output_data" / "mediapipe_face_3d_xyz.npy")
    # Call the function to load vertices
    create_face_mesh(file_path=face_mesh_npy_file)
