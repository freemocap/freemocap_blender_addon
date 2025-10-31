import traceback
from pathlib import Path
from typing import List

import numpy as np
from ajc27_freemocap_blender_addon.core_functions.load_videos.load_videos import load_videos_as_planes
from ajc27_freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.attach_rigid_body_meshes_to_rig import create_rigid_body_meshes
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.get_or_create_freemocap_data_handler import (
    get_or_create_freemocap_data_handler,
)
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import load_freemocap_data
from .create_rig.add_rig_method_enum import AddRigMethods
from .create_rig.create_rig import create_rig

from .export_video.export_video import export_video
from .calculate_joint_angles.calculate_joint_angles import calculate_joint_angles
from .calculate_joint_angles.joint_angle_definitions import joint_angles_definitions


from .export_3d_model.export_3d_model import export_3d_model
from .empties.creation.create_freemocap_empties import create_freemocap_empties
from .meshes.center_of_mass.center_of_mass_mesh import create_center_of_mass_mesh
from .meshes.center_of_mass.center_of_mass_trails import create_center_of_mass_trails
from .meshes.skelly_mesh.attach_skelly_mesh import attach_skelly_mesh_to_rig
from .create_rig.save_bone_and_joint_angles_from_rig import save_bone_and_joint_angles_from_rig
from .setup_scene.make_parent_empties import create_parent_empty
from .setup_scene.set_start_end_frame import set_start_end_frame
from ..data_models.bones.bone_constraints import get_bone_constraint_definitions
from ..data_models.bones.bone_definitions import get_bone_definitions
from ..data_models.parameter_models.parameter_models import Config
from ..freemocap_data_handler.helpers.saver import FreemocapDataSaver
from ..freemocap_data_handler.operations.enforce_rigid_bodies.enforce_rigid_bodies import enforce_rigid_bodies
from ..freemocap_data_handler.operations.fix_hand_data import fix_hand_data
from ..freemocap_data_handler.operations.put_skeleton_on_ground import put_skeleton_on_ground

from ajc27_freemocap_blender_addon.core_functions.add_capture_cameras.add_capture_cameras import add_capture_cameras


class MainController:
    """
    This class is used to run the program as a main script.
    """

    def __init__(self, recording_path: str, blend_file_path: str, config: Config):
        self.rig = None
        self.empties = None
        self._data_parent_empty = None
        self._empty_parent_object = None
        self._rigid_body_meshes_parent_object = None
        self._video_parent_object = None
        try:
            import bpy
            self._blender_version = bpy.app.version
        except ImportError:
            self._blender_version = None

        self.config = config

        self.recording_path = recording_path
        self.blend_file_path = blend_file_path
        self.recording_name = Path(self.recording_path).stem
        self._output_video_path = str(Path(self.blend_file_path).parent / f"{self.recording_name}_video_output.mp4")
        self.origin_name = f"{self.recording_name}_origin"
        self.rig_name = f"{self.recording_name}_rig"
        self.bone_constraint_definitions = get_bone_constraint_definitions()
        self._create_parent_empties()
        self.freemocap_data_handler = get_or_create_freemocap_data_handler(
            recording_path=self.recording_path
        )
        self.empties = None

    @property
    def data_parent_empty(self):
        return self._data_parent_empty

    @property
    def empty_names(self) -> List[str]:
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        empty_names = []

        def get_empty_names_from_dict(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    get_empty_names_from_dict(value) #recursion, baby!
                else:
                    empty_names.append(key)

        get_empty_names_from_dict(self.empties)

        return empty_names
    
    @property
    def center_of_mass_empty(self):
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        return list(self.empties["other"]["center_of_mass"].values())[0]

    def _create_parent_empties(self):
        self._data_parent_empty = create_parent_empty(name=self.origin_name,
                                                       display_scale=1.0,
                                                       type="ARROWS")
        self._empty_parent_object = create_parent_empty(
            name="empties_parent",
            parent_object=self._data_parent_empty,
            type="PLAIN_AXES",
            display_scale=0.3,
        )
        self._rigid_body_meshes_parent_object = create_parent_empty(
            name="rigid_body_meshes_parent",
            parent_object=self._data_parent_empty,
            type="CUBE",
            display_scale=0.2,
        )
        self._video_parent_object = create_parent_empty(
            name="videos_parent",
            parent_object=self._data_parent_empty,
            type="IMAGE",
            display_scale=0.1,
        )
        # self._data_parent_empty = create_parent_empty(
        #     name="center_of_mass_data_parent",
        #     parent_object=self._data_parent_empty,
        #     type="SPHERE",
        #     display_scale=0.1,
        # )


    def load_freemocap_data(self):
        try:
            print("Loading freemocap data....")
            self.freemocap_data_handler = load_freemocap_data(
                recording_path=self.recording_path
            )
            self.freemocap_data_handler.mark_processing_stage("original_from_file")
            set_start_end_frame(
                number_of_frames=self.freemocap_data_handler.number_of_frames
            )
        except Exception as e:
            print(f"Failed to load freemocap data: {e}")
            raise e

    def calculate_virtual_trajectories(self):
        try:
            print("Calculating virtual trajectories....")
            self.freemocap_data_handler.calculate_virtual_trajectories()
            self.freemocap_data_handler.mark_processing_stage(
                "add_virtual_trajectories"
            )
        except Exception as e:
            print(f"Failed to calculate virtual trajectories: {e}")
            print(e)
            raise e

    def put_data_in_inertial_reference_frame(self):
        try:
            print("Putting freemocap data in inertial reference frame....")
            put_skeleton_on_ground(handler=self.freemocap_data_handler)
        except Exception as e:
            print(
                f"Failed when trying to put freemocap data in inertial reference frame: {e}"
            )
            print(traceback.format_exc())
            raise e

    def enforce_rigid_bones(self):
        print("Enforcing rigid bones...")
        try:
            self.freemocap_data_handler = enforce_rigid_bodies(
                handler=self.freemocap_data_handler
            )

        except Exception as e:
            print(f"Failed during `enforce rigid bones`, error: `{e}`")
            print(e)
            raise e

    def fix_hand_data(self):
        try:
            # print("Fixing hand data...")
            self.freemocap_data_handler = fix_hand_data(
                handler=self.freemocap_data_handler
            )
        except Exception as e:
            print(f"Failed during `fix hand data`, error: `{e}`")
            print(e)
            raise e

    def calculate_joint_angles(self):
        try:
            print("Calculating joint angles...")
            # Get the combined marker names
            marker_names = (
                list(self.freemocap_data_handler.body_names) +
                list(self.freemocap_data_handler.right_hand_names) +
                list(self.freemocap_data_handler.left_hand_names)
            )
            marker_frame_xyz = np.concatenate(
                [
                    self.freemocap_data_handler.body_frame_name_xyz,
                    self.freemocap_data_handler.right_hand_frame_name_xyz,
                    self.freemocap_data_handler.left_hand_frame_name_xyz,
                ],
                axis=1,
            )
            calculate_joint_angles(
                output_path=str(Path(self.recording_path) / "output_data" / "joint_angles.csv"),
                marker_names=marker_names,
                marker_frame_xyz=marker_frame_xyz,
                joint_angles_definitions=joint_angles_definitions,
            )
            self.freemocap_data_handler.mark_processing_stage("calculate_joint_angles")
        except Exception as e:
            print(f"Failed to calculate joint angles: {e}")
            print(e)
            raise e

    def save_data_to_disk(self):
        try:
            print("Saving data to disk...")
            FreemocapDataSaver(handler=self.freemocap_data_handler).save(
                recording_path=self.recording_path
            )
        except Exception as e:
            print(f"Failed to save data to disk: {e}")
            print(e)
            raise e

    def create_empties(self):
        try:
            print("Creating keyframed empties....")

            self.empties = create_freemocap_empties(
                handler=self.freemocap_data_handler,
                parent_object=self._empty_parent_object,
                center_of_mass_data_parent=self._data_parent_empty,
            )
            print(f"Finished creating keyframed empties: {self.empties.keys()}")
        except Exception as e:
            print(f"Failed to create keyframed empties: {e}")

    def add_rig(self):
        try:
            print("Adding rig...")
            self.rig = create_rig(
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig_name=self.rig_name,
                parent_object=self._data_parent_empty,
                add_rig_method=AddRigMethods.BY_BONE,
                keep_symmetry=self.config.add_rig.keep_symmetry,
                add_fingers_constraints=self.config.add_rig.add_fingers_constraints,
                bone_constraint_definitions=self.bone_constraint_definitions,
                use_limit_rotation=self.config.add_rig.use_limit_rotation,
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
                Path(self.blend_file_path).parent / "saved_data" / f"{self.recording_name}_bone_and_joint_data.csv")
            save_bone_and_joint_angles_from_rig(
                rig=self.rig,
                bone_names=self.freemocap_data_handler.metadata["bone_data"].keys(),
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
            create_rigid_body_meshes(
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig=self.rig,
                empties=self.empties,
                parent_object=self._rigid_body_meshes_parent_object,
            )
        except Exception as e:
            print(f"Failed to attach rigid bone meshes to rig: {e}")
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
            print(f"Failed to attach skelly mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_mesh(self):

        try:
            print("Adding Center of Mass Mesh")
            create_center_of_mass_mesh(
                parent_object=self._data_parent_empty,
                center_of_mass_empty=self.center_of_mass_empty,
            )
        except Exception as e:
            print(f"Failed to attach center of mass mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_trails(self):
        try:
            print("Adding Center of Mass trail meshes")

            create_center_of_mass_trails(
                center_of_mass_trajectory=np.squeeze(self.freemocap_data_handler.center_of_mass_trajectory),
                parent_empty=self._data_parent_empty,
                tail_past_frames=30,
                trail_future_frames=30   ,
                trail_starting_width=0.045,
                trail_minimum_width=0.01,
                trail_size_decay_rate=0.8,
                trail_color=(1.0, 0.0, 1.0, 1.0),
            )

        except Exception as e:
            print(f"Failed to attach Center of Mass trail meshes to rig: {e}")
            print(e)
            raise e

    def add_videos(self):
        try:
            print("Loading videos as planes...")
            load_videos_as_planes(
                recording_path=self.recording_path,
                parent_object=self._video_parent_object,
            )
        except Exception as e:
            print(e)
            print(e)
            raise e

    def setup_scene(self):
        import bpy

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:  # iterate through areas in current screen
                if area.type == "VIEW_3D":
                    for (
                            space
                    ) in area.spaces:  # iterate through spaces in current VIEW_3D area
                        if space.type == "VIEW_3D":  # check if space is a 3D view
                            space.shading.type = "MATERIAL"

        self._empty_parent_object.hide_set(True)
        self._rigid_body_meshes_parent_object.hide_set(True)
        self.center_of_mass_empty.hide_set(True)
        self._video_parent_object.hide_set(True)
        self._data_parent_empty.hide_set(True)

        # remove default cube
        cube_name = bpy.app.translations.pgettext_data("Cube")
        if cube_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[cube_name])

        # create_scene_objects(scene=bpy.context.scene)


    def save_blender_file(self):
        print("Saving blender file...")
        import bpy

        bpy.ops.wm.save_as_mainfile(filepath=str(self.blend_file_path))
        print(f"Saved .blend file to: {self.blend_file_path}")


    def export_3d_model(self):
        print("Exporting 3D model...")
        try:
            export_3d_model(
                data_parent_empty=self.data_parent_empty,
                armature = self.rig,
                destination_folder=self.recording_path,
                add_subfolder=True,
                rename_root_bone=False,
            )
        except Exception as e:
            print(f"Failed to export 3D model: {e}")
            raise e

    def add_capture_cameras(self):
        print("Adding capture cameras...")
        try:
            add_capture_cameras(
                recording_folder=self.recording_path
            )
        except Exception as e:
            print(f"Failed to add capture cameras: {e}")
            raise e

    def load_data(self):
        import time
        print("Running all stages...")
        stage_times = {}

        # Pure python stuff
        # TODO - move the non-blender stuff to a another module (prob `skellyforge`)
        start_time = time.perf_counter_ns()
        self.load_freemocap_data()
        end_time = time.perf_counter_ns()
        stage_times['load_freemocap_data'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.calculate_virtual_trajectories()
        end_time = time.perf_counter_ns()
        stage_times['calculate_virtual_trajectories'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        if not self.freemocap_data_handler.freemocap_data.groundplane_calibration:
            self.put_data_in_inertial_reference_frame()
        end_time = time.perf_counter_ns()
        stage_times['put_data_in_inertial_reference_frame'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.enforce_rigid_bones()
        end_time = time.perf_counter_ns()
        stage_times['enforce_rigid_bones'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.fix_hand_data()
        end_time = time.perf_counter_ns()
        stage_times['fix_hand_data'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.calculate_joint_angles()
        end_time = time.perf_counter_ns()
        stage_times['calculate_joint_angles'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.save_data_to_disk()
        end_time = time.perf_counter_ns()
        stage_times['save_data_to_disk'] = (end_time - start_time)/1e9

        # Blender stuff
        import bpy
        start_time = time.perf_counter_ns()
        self.create_empties()
        end_time = time.perf_counter_ns()
        stage_times['create_empties'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.add_rig()
        end_time = time.perf_counter_ns()
        stage_times['add_rig'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.save_bone_and_joint_data_from_rig()
        end_time = time.perf_counter_ns()
        stage_times['save_bone_and_joint_data_from_rig'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.attach_rigid_body_mesh_to_rig()
        end_time = time.perf_counter_ns()
        stage_times['attach_rigid_body_mesh_to_rig'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.attach_skelly_mesh_to_rig()
        end_time = time.perf_counter_ns()
        stage_times['attach_skelly_mesh_to_rig'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.create_center_of_mass_mesh()
        end_time = time.perf_counter_ns()
        stage_times['create_center_of_mass_mesh'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.add_videos()
        end_time = time.perf_counter_ns()
        stage_times['add_videos'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.add_capture_cameras()
        end_time = time.perf_counter_ns()
        stage_times['add_capture_cameras'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.setup_scene()
        end_time = time.perf_counter_ns()
        stage_times['setup_scene'] = (end_time - start_time)/1e9

        start_time = time.perf_counter_ns()
        self.export_3d_model()
        end_time = time.perf_counter_ns()
        stage_times['export_3d_model'] = (end_time - start_time)/1e9

        try:
            # Add the data parent empty to the collection of data parents
            new_data_parent = bpy.context.scene.freemocap_properties.data_parent_collection.add()
            new_data_parent.name = self.data_parent_empty.name
            # Set the new data parent as the scope data parent in the addon ui
            bpy.context.scene.freemocap_properties.scope_data_parent = self.data_parent_empty.name
        except Exception as e:
            # Addon ui not loaded
            print(e)

        self.save_blender_file()

        # Print summary
        print("\nSummary of stage times:")
        for stage, time in stage_times.items():
            print(f"{stage}: {time:.3f} seconds")
        print(f"Total time: {sum(stage_times.values()):.3f} seconds")
