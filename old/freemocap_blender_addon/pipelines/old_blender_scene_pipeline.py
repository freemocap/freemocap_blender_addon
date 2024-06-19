from pathlib import Path

import bpy
import numpy as np
from freemocap_blender_addon.core_functions.create_video.create_video import create_video
from freemocap_blender_addon.core_functions.empties.creation.create_freemocap_empties import create_freemocap_empties
from freemocap_blender_addon.core_functions.load_videos.load_videos import load_videos
from freemocap_blender_addon.core_functions.meshes.attach_mesh_to_rig import attach_mesh_to_rig
from freemocap_blender_addon.core_functions.meshes.center_of_mass.center_of_mass_mesh import create_center_of_mass_mesh
from freemocap_blender_addon.core_functions.meshes.center_of_mass.center_of_mass_trails import \
    create_center_of_mass_trails
from freemocap_blender_addon.core_functions.meshes.skelly_mesh.attach_skelly_mesh import attach_skelly_mesh_to_rig
from freemocap_blender_addon.core_functions.rig.add_rig import generate_rig, AddRigMethods
from freemocap_blender_addon.core_functions.rig.save_bone_and_joint_angles_from_rig import \
    save_bone_and_joint_angles_from_rig
from freemocap_blender_addon.core_functions.setup_scene.make_parent_empties import create_parent_empty
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.utilities.singleton_metaclass import SingletonMetaClass


class OldBlenderController(metaclass=SingletonMetaClass):
    def __init__(self, recording_path: str, blend_file_path_str: str, pipeline_config: PipelineConfig):
        self.pipeline_config: PipelineConfig = pipeline_config
        self.blend_file_path_str: str = blend_file_path_str
        self.origin_name = f"{self.recording_name}_origin"
        self.rig_name = f"{self.recording_name}_rig"
        self._create_parent_empties()

    def _create_parent_empties(self):
        self._data_parent_object = create_parent_empty(name=self.origin_name, display_scale=1.0, type="ARROWS")
        self._empty_parent_object = create_parent_empty(name="empties_parent", parent_object=self._data_parent_object,
                                                        type="PLAIN_AXES", display_scale=0.3)
        self._rigid_body_meshes_parent_object = create_parent_empty(name="rigid_body_meshes_parent",
                                                                    parent_object=self._data_parent_object, type="CUBE",
                                                                    display_scale=0.2)
        self._video_parent_object = create_parent_empty(name="videos_parent", parent_object=self._data_parent_object,
                                                        type="IMAGE", display_scale=0.1)
        self._center_of_mass_parent_object = create_parent_empty(name="center_of_mass_data_parent",
                                                                 parent_object=self._data_parent_object, type="SPHERE",
                                                                 display_scale=0.1)

    def create_empties(self):
        try:
            print("Creating keyframed empties....")
            self.empties = create_freemocap_empties(
                handler=self.freemocap_data_handler,
                parent_object=self._empty_parent_object,
                center_of_mass_data_parent=self._center_of_mass_parent_object,

            )
            print(f"Finished creating keyframed empties: {self.empties.keys()}")
        except Exception as e:
            print(f"Failed to create keyframed empties: {e}")

    def add_rig(self):
        try:
            print("Adding rig...")
            self.rig = generate_rig(
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig_name=self.rig_name,
                parent_object=self._data_parent_object,
                add_rig_method=AddRigMethods.BY_BONE,
                keep_symmetry=self.pipeline_config.add_rig.keep_symmetry,
                add_fingers_constraints=self.pipeline_config.add_rig.add_fingers_constraints,
                use_limit_rotation=self.pipeline_config.add_rig.use_limit_rotation,
            )
        except Exception as e:
            print(f"Failed to add rig: {e}")
            print(e)
            raise e

    def save_bone_and_joint_data_from_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Saving joint angles...")
            csv_file_path = str(
                Path(self.blend_file_path_str).parent / "saved_data" / f"{self.recording_name}_bone_and_joint_data.csv")
            save_bone_and_joint_angles_from_rig(
                rig=self.rig,
                csv_save_path=csv_file_path,
                start_frame=0,
                end_frame=self.freemocap_data_handler.number_of_frames,
            )
        except Exception as e:
            print(f"Failed to save joint angles: {e}")
            print(e)
            raise e

    def attach_rigid_body_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")

        if self.empties is None:
            raise ValueError("Empties have not been created yet!")

        try:
            print("Adding rigid_body_bone_meshes...")
            attach_mesh_to_rig(
                body_mesh_mode=self.pipeline_config.add_body_mesh.body_mesh_mode,
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig=self.rig,
                empties=self.empties,
                parent_object=self._rigid_body_meshes_parent_object,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def attach_skelly_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Adding Skelly mesh!!! :D")
            body_dimensions = self.freemocap_data_handler.get_body_dimensions()
            attach_skelly_mesh_to_rig(
                rig=self.rig,
                body_dimensions=body_dimensions,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_mesh(self):
        try:
            print("Adding Center of Mass Mesh")
            create_center_of_mass_mesh(
                parent_object=self._center_of_mass_parent_object,
                center_of_mass_empty=self.center_of_mass_empty,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_trails(self):
        try:
            print("Adding Center of Mass trail meshes")
            create_center_of_mass_trails(
                center_of_mass_trajectory=np.squeeze(self.freemocap_data_handler.center_of_mass_trajectory),
                parent_empty=self._center_of_mass_parent_object,
                tail_past_frames=30,
                trail_future_frames=30,
                trail_starting_width=0.045,
                trail_minimum_width=0.01,
                trail_size_decay_rate=0.8,
                trail_color=(1.0, 0.0, 1.0, 1.0),
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def add_videos(self):
        try:
            print("Loading videos as planes...")
            load_videos(
                recording_path=self.recording_path_str,
                parent_object=self._video_parent_object,
            )
        except Exception as e:
            print(e)
            print(e)
            raise e

    def setup_scene(self):
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == "VIEW_3D":
                    for space in area.spaces:
                        if space.type == "VIEW_3D":
                            space.shading.type = "MATERIAL"

        self._empty_parent_object.hide_set(True)
        self._rigid_body_meshes_parent_object.hide_set(True)
        self._video_parent_object.hide_set(True)
        self._center_of_mass_parent_object.hide_set(True)

        if "Cube" in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects["Cube"])

    def create_video(self):
        print("Creating export video...")
        create_video(
            scene=bpy.context.scene,
            recording_folder=self.recording_path_str,
            start_frame=bpy.context.scene.frame_start,
            end_frame=bpy.context.scene.frame_end,
        )

    def save_blender_file(self):
        print("Saving blender file...")
        bpy.ops.wm.save_as_mainfile(filepath=str(self.blend_file_path_str))
        print(f"Saved .blend file to: {self.blend_file_path_str}")

    def run_all(self):
        print("Running all Blender stages...")

        self.create_empties()
        self.add_rig()
        self.save_bone_and_joint_data_from_rig()
        self.attach_rigid_body_mesh_to_rig()
        self.attach_skelly_mesh_to_rig()
        self.create_center_of_mass_mesh()
        self.add_videos()
        self.setup_scene()
        self.save_blender_file()
