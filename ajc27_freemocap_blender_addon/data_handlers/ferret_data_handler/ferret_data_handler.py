from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from .ferret_data.ferret_data_model import FerretData


@dataclass
class FerretDataHandler:
    ferret_data: FerretData

    @classmethod
    def from_recording_path(cls,
                            recording_path: str,
                            ) -> "FerretDataHandler":
        ferret_data = FerretData.from_recording_path(recording_path=recording_path)
        return cls(ferret_data=ferret_data)

    @property
    def metadata(self) -> dict[object, object]:
        return self.ferret_data.metadata

    @property
    def trajectories(self) -> dict[str, np.ndarray]:
        trajectories = {}
        trajectories.update(self.body_trajectories)
        trajectories.update(self.right_hand_trajectories)
        trajectories.update(self.left_hand_trajectories)
        trajectories.update(self.face_trajectories)
        trajectories.update(self.other_trajectories)
        return trajectories

    @property
    def center_of_mass_trajectory(self) -> np.ndarray:
        return self.ferret_data.other["center_of_mass"].data


    @property
    def body_trajectories(self) -> dict[str, np.ndarray]:
        return {trajectory_name: self.body_frame_name_xyz[:, trajectory_number]
                for trajectory_number, trajectory_name in enumerate(self.body_names)}

    @property
    def right_hand_trajectories(self) -> dict[str, np.ndarray]:
        return {trajectory_name: self.right_hand_frame_name_xyz[:, trajectory_number]
                for trajectory_number, trajectory_name in enumerate(self.right_hand_names)}

    @property
    def left_hand_trajectories(self) -> dict[str, np.ndarray]:
        return {trajectory_name: self.left_hand_frame_name_xyz[:, trajectory_number]
                for trajectory_number, trajectory_name in enumerate(self.left_hand_names)}

    @property
    def face_trajectories(self) -> dict[str, np.ndarray]:
        return {trajectory_name: self.face_frame_name_xyz[:, trajectory_number]
                for trajectory_number, trajectory_name in enumerate(self.face_names)}

    @property
    def other_trajectories(self) -> dict[str, np.ndarray]:
        trajectories = {}
        for name, component in self.ferret_data.other.items():
            trajectories.update({name: component.data})
        return trajectories

    @property
    def all_frame_name_xyz(self):
        all_data = np.concatenate([self.body_frame_name_xyz,
                                   self.right_hand_frame_name_xyz,
                                   self.left_hand_frame_name_xyz,
                                   self.face_frame_name_xyz], axis=1)

        for other_component in self.ferret_data.other.values():
            if len(other_component.data.shape) == 2:
                other_component.data = np.expand_dims(other_component.data, axis=1)
            all_data = np.concatenate([all_data, other_component.data], axis=1)

        if all_data.shape[0] != self.number_of_frames:
            raise ValueError(
                f"Number of frames ({self.number_of_frames}) does not match number of frames in all_frame_name_xyz ({all_data.shape[0]}).")
        if all_data.shape[1] != self.number_of_trajectories:
            raise ValueError(
                f"Number of trajectories ({self.number_of_trajectories}) does not match number of trajectories in all_frame_name_xyz ({all_data.shape[1]}).")
        if all_data.shape[2] != 3:
            raise ValueError(f"all_frame_name_xyz should have 3 dimensions. Got {all_data.shape[2]} instead.")

        return all_data

    @property
    def body_frame_name_xyz(self):
        return self.ferret_data.body.data

    @body_frame_name_xyz.setter
    def body_frame_name_xyz(self, value):
        if value.shape != self.body_frame_name_xyz.shape:
            raise ValueError(
                f"Shape of new body data ({value.shape}) does not match shape of old body data ({self.body_frame_name_xyz.shape}).")
        self.ferret_data.body.data = value

    @property
    def right_hand_frame_name_xyz(self):
        return self.ferret_data.hands["right"].data

    @right_hand_frame_name_xyz.setter
    def right_hand_frame_name_xyz(self, value):
        if value.shape != self.right_hand_frame_name_xyz.shape:
            raise ValueError(
                f"Shape of new right hand data ({value.shape}) does not match shape of old right hand data ({self.right_hand_frame_name_xyz.shape}).")
        self.ferret_data.hands["right"].data = value

    @property
    def left_hand_frame_name_xyz(self):
        return self.ferret_data.hands["left"].data

    @left_hand_frame_name_xyz.setter
    def left_hand_frame_name_xyz(self, value):
        if value.shape != self.left_hand_frame_name_xyz.shape:
            raise ValueError(
                f"Shape of new left hand data ({value.shape}) does not match shape of old left hand data ({self.left_hand_frame_name_xyz.shape}).")
        self.ferret_data.hands["left"].data = value

    @property
    def face_frame_name_xyz(self):
        return self.ferret_data.face.data

    @face_frame_name_xyz.setter
    def face_frame_name_xyz(self, value):
        if value.shape != self.face_frame_name_xyz.shape:
            raise ValueError(
                f"Shape of new face data ({value.shape}) does not match shape of old face data ({self.face_frame_name_xyz.shape}).")
        self.ferret_data.face.data = value

    @property
    def body_names(self):
        return self.ferret_data.body.trajectory_names

    @property
    def right_hand_names(self):
        return self.ferret_data.hands["right"].trajectory_names

    @property
    def left_hand_names(self):
        return self.ferret_data.hands["left"].trajectory_names

    @property
    def face_names(self):
        return self.ferret_data.face.trajectory_names

    @property
    def number_of_frames(self) -> int:
        frame_counts = self._collect_frame_counts()
        self._validate_frame_counts(frame_counts)
        return frame_counts['body']

    @property
    def number_of_body_trajectories(self):
        return self.body_frame_name_xyz.shape[1]

    @property
    def number_of_right_hand_trajectories(self):
        return self.right_hand_frame_name_xyz.shape[1]

    @property
    def number_of_left_hand_trajectories(self):
        return self.left_hand_frame_name_xyz.shape[1]

    @property
    def number_of_face_trajectories(self):
        return self.face_frame_name_xyz.shape[1]

    @property
    def number_of_hand_trajectories(self):
        if not self.number_of_right_hand_trajectories == self.number_of_left_hand_trajectories:
            print(f"Number of right hand trajectories ({self.number_of_right_hand_trajectories}) "
                  f"does not match number of left hand trajectories ({self.number_of_left_hand_trajectories}).")
        return self.number_of_right_hand_trajectories + self.number_of_left_hand_trajectories

    @property
    def number_of_other_trajectories(self):
        return sum([other_component.data.shape[1] for other_component in self.ferret_data.other.values()])

    @property
    def number_of_trajectories(self):
        return (self.number_of_body_trajectories +
                self.number_of_right_hand_trajectories +
                self.number_of_left_hand_trajectories +
                self.number_of_face_trajectories +
                self.number_of_other_trajectories)

    def get_body_dimensions(self):
        if self.metadata is None:
            self.ferret_data.metadata = {}
        if "body_dimensions" in self.metadata:
            return self.metadata["body_dimensions"]
        else:
            raise ValueError("Body dimensions not found in metadata - please run `enforce_rigid_bones()`/`estimate_body_dimensions()` first.")

    def estimate_good_clean_frame(self):
        return estimate_good_frame(trajectories_with_error=self.get_trajectories(with_error=True))


    def add_trajectory(self,
                       trajectory: np.ndarray,
                       trajectory_name: str,
                       component_type: FREEMOCAP_DATA_COMPONENT_TYPES,
                       source: str = None, # TODO: remove this from the chain if it isn't used anywhere
                       group_name: str = None):
        if trajectory.shape[0] != self.number_of_frames:
            raise ValueError(
                f"Number of frames ({trajectory.shape[0]}) does not match number of frames in existing data ({self.number_of_frames}).")

        if len(trajectory.shape) == 2:
            num_dimensions = trajectory.shape[1]
            trajectory = np.expand_dims(trajectory,
                                        axis=1)  # add a dummy "name" dimenstion to trajectory so it can be concatenated with other trajectories
        if len(trajectory.shape) == 3:
            num_dimensions = trajectory.shape[2]

            if num_dimensions != 3:
                raise ValueError(
                    f"Trajectory data should have 3 dimensions. Got {trajectory.shape[2]} instead.")

        if component_type == "body":
            self.ferret_data.body.data = np.concatenate([self.body_frame_name_xyz, trajectory], axis=1)
            self.ferret_data.body.trajectory_names.append(trajectory_name)
        elif component_type == "right_hand":
            self.ferret_data.hands["right"].data = np.concatenate([self.right_hand_frame_name_xyz, trajectory],
                                                                  axis=1)
            self.ferret_data.hands["right"].trajectory_names.append(trajectory_name)
        elif component_type == "left_hand":
            self.ferret_data.hands["left"].data = np.concatenate([self.left_hand_frame_name_xyz, trajectory], axis=1)
            self.ferret_data.hands["left"].trajectory_names.append(trajectory_name)
        elif component_type == "face":
            self.ferret_data.face.data = np.concatenate([self.face_frame_name_xyz, trajectory], axis=1)
            self.ferret_data.face.trajectory_names.append(trajectory_name)
        elif component_type == "other":
            for other_component in self.ferret_data.other.values():
                if other_component.name == group_name:
                    other_component.data = np.concatenate([other_component.data, trajectory], axis=1)
                    other_component.trajectory_names.append(trajectory_name)
        else:
            raise ValueError(
                f"Component type {component_type} not recognized.")

    def add_trajectories(self,
                         trajectories: dict[str, np.ndarray],
                         component_type: Union[str, List[str]],
                         source: str = None,
                         group_name: str = None):

        if not isinstance(component_type, list):
            component_types = [component_type] * len(trajectories)
        else:
            component_types = [component_type]

        for trajectory_number, trajectory_dict in enumerate(trajectories.items()):
            trajectory_name, trajectory = trajectory_dict

            self.add_trajectory(trajectory=trajectory,
                                trajectory_name=trajectory_name,
                                component_type=component_types[trajectory_number],
                                source=source,
                                group_name=group_name)

    def get_trajectories(self,
                         trajectory_names: List[str] = None,
                         components=None,
                         with_error: bool = False) -> Union[
        dict[str, np.ndarray], dict[str, dict[str, np.ndarray]]]:

        if trajectory_names is None:
            trajectory_names = [self.body_names, self.right_hand_names, self.left_hand_names]
        if not isinstance(trajectory_names, list):
            trajectory_names = [trajectory_names]

        if components is None:
            components = [None] * len(trajectory_names)
        elif not isinstance(components, list):
            components = [components] * len(trajectory_names)

        return {name: self.get_trajectory(name=name,
                                          component_type=component,
                                          with_error=with_error) for
                name, component in zip(trajectory_names, components)}

    def get_trajectory(self,
                       name: str,
                       component_type: FREEMOCAP_DATA_COMPONENT_TYPES = None,
                       with_error: bool = False) -> Union[np.ndarray, dict[str, np.ndarray]]:

        trajectories = []
        errors = []
        if component_type is None:
            if name in self.body_names:
                trajectories.append(self.body_frame_name_xyz[:, self.body_names.index(name), :])
                if with_error:
                    errors.append(self.ferret_data.body.error[:, self.body_names.index(name)])

            if name in self.right_hand_names:
                trajectories.append(self.right_hand_frame_name_xyz[:, self.right_hand_names.index(name), :])
                if with_error:
                    errors.append(self.ferret_data.hands["right"].error[:, self.right_hand_names.index(name)])

            if name in self.left_hand_names:
                trajectories.append(self.left_hand_frame_name_xyz[:, self.left_hand_names.index(name), :])
                if with_error:
                    errors.append(self.ferret_data.hands["left"].error[:, self.left_hand_names.index(name)])

            if name in self.face_names:
                trajectories.append(self.face_frame_name_xyz[:, self.face_names.index(name), :])
                if with_error:
                    errors.append(self.ferret_data.face.error[:, self.face_names.index(name)])

            for other_component in self.ferret_data.other.values():
                if name in other_component.trajectory_names:
                    if len(other_component.data.shape) == 3:
                        trajectories.append(
                            other_component.data[:, other_component.trajectory_names.index(name), :])
                    elif len(other_component.data.shape) == 2:
                        trajectories.append(
                            other_component.data[:, other_component.trajectory_names.index(name)])
                    else:
                        raise ValueError(
                            f"Data shape {other_component.data.shape} is not supported. Should be 2 or 3 dimensional.")

                    if with_error and other_component.error is not None:
                        errors.append(
                            other_component.error[:, other_component.trajectory_names.index(name)])
                    else:
                        errors.append(None)
        if trajectories == []:
            raise ValueError(f"Trajectory {name} not found.")

        if len(trajectories) > 1:
            raise ValueError(
                f"Trajectory {name} found in multiple components. Specify component (body, right_hand, left_hand, face, other) to resolve ambiguity.")

        if not with_error:
            return trajectories[0]
        else:
            return {"trajectory": trajectories[0], "error": errors[0]}

    def set_trajectory(self,
                       name: str,
                       data: np.ndarray,
                       component_type: Optional[FREEMOCAP_DATA_COMPONENT_TYPES] = None):
        data = np.squeeze(
            data)  # get rid of any dimensions of size 1 (aka `singleton dimensions`, aka 'you called a square a flat cube')
        if not len(data.shape) == 2:
            raise ValueError(
                f"Data should have 2 dimensions. Got {data.shape} instead.")

        if data.shape[0] != self.number_of_frames:
            raise ValueError(
                f"Number of frames ({data.shape[0]}) does not match number of frames in existing data ({self.number_of_frames}).")
        if data.shape[1] != 3:
            raise ValueError(
                f"Trajectory data should have 3 dimensions. Got {data.shape[1]} instead.")

        try:
            if component_type is None:
                if name in self.body_names:
                    self.ferret_data.body.data[:, self.body_names.index(name), :] = data

                if name in self.right_hand_names:
                    self.ferret_data.hands["right"].data[:, self.right_hand_names.index(name), :] = data

                if name in self.left_hand_names:
                    self.ferret_data.hands["left"].data[:, self.left_hand_names.index(name), :] = data

                if name in self.face_names:
                    self.ferret_data.face.data[:, self.face_names.index(name), :] = data

                for other_component in self.ferret_data.other.values():
                    if name in other_component.trajectory_names:
                        if len(other_component.data.shape) == 3:
                            other_component.data[:, other_component.trajectory_names.index(name), :] = data
                        elif len(other_component.data.shape) == 2:
                            other_component.data = data
                        else:
                            raise ValueError(
                                f"Data shape {other_component.data.shape} is not supported. Should be 2 or 3 dimensional.")
        except Exception as e:
            print(f"Error while setting trajectory `{name}`:\n error:\n {e}")
            print(e)
            raise Exception(f"Error while setting trajectory: {e}")

    def _collect_frame_counts(self) -> dict:
        frame_counts = {
            'body': self.body_frame_name_xyz.shape[0],
            'right_hand': self.right_hand_frame_name_xyz.shape[0],
            'left_hand': self.left_hand_frame_name_xyz.shape[0],
            'face': self.face_frame_name_xyz.shape[0],
            'other': [other_component.data.shape[0] for other_component in self.ferret_data.other.values()],
        }
        return frame_counts

    def _validate_frame_counts(self, frame_counts: dict):
        body_frame_count = frame_counts['body']
        are_frame_counts_equal = all(
            body_frame_count == frame_count
            for frame_count in frame_counts.values()
            if isinstance(frame_count, int)
        )
        are_other_frame_counts_equal = all(
            body_frame_count == frame_count
            for frame_count in frame_counts['other']
        )
        if not (are_frame_counts_equal and are_other_frame_counts_equal):
            raise ValueError(f"Number of frames do not match: {frame_counts}")



    def extract_data_from_empties(self, empties: dict[str, Any]):

        try:
            import bpy
            print(f"Extracting data from empties {empties.keys()}")

            body_frames = []
            right_hand_frames = []
            left_hand_frames = []
            face_frames = []
            other_components_frames = {}

            for frame_number in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
                print(f"Extracting data from frame {frame_number}...")
                bpy.context.scene.frame_set(frame_number)

                if "body" in empties.keys():
                    body_frames.append(np.array(
                        [bpy.data.objects[empty_name].location for empty_name in empties["body"].keys()]))

                if "hands" in empties.keys():
                    right_hand_frames.append(np.array(
                        [bpy.data.objects[empty_name].location for empty_name in empties["hands"]["right"].keys()]))

                    left_hand_frames.append(np.array(
                        [bpy.data.objects[empty_name].location for empty_name in empties["hands"]["left"].keys()]))

                if "face" in empties.keys():
                    face_frames.append(np.array(
                        [bpy.data.objects[empty_name].location for empty_name in empties["face"].keys()]))

                if "other" in empties.keys():
                    for other_name, other_component in self.ferret_data.other.items():
                        if not other_name in other_components_frames.keys():
                            other_components_frames[other_name] = []
                        other_components_frames[other_name].append(np.ndarray(bpy.data.objects[other_name].location))

            if len(body_frames) > 0:
                self.body_frame_name_xyz = np.array(body_frames)
            if len(right_hand_frames) > 0:
                self.right_hand_frame_name_xyz = np.array(right_hand_frames)
            if len(left_hand_frames) > 0:
                self.left_hand_frame_name_xyz = np.array(left_hand_frames)
            if len(face_frames) > 0:
                self.face_frame_name_xyz = np.array(face_frames)
            if len(other_components_frames) > 0:
                for other_name, other_component_frames in other_components_frames.items():
                    self.ferret_data.other[other_name].data = np.array(other_component_frames)

        except Exception as e:
            print(f"Failed to extract data from empties {empties.keys()}")
            print(e)
            raise e


    def calculate_virtual_trajectories(self):
        print(f"Calculating virtual trajectories")
        try:
            virtual_trajectories = calculate_virtual_trajectories(body_frame_name_xyz=self.body_frame_name_xyz,
                                                                  body_names=self.body_names)
            self.add_trajectories(trajectories=virtual_trajectories,
                                  component_type="body",
                                  )

        except Exception as e:
            print(f"Failed to calculate virtual trajectories: {e}")
            print(e)
            raise e

    def get_trajectory_names(self, component_name: str) -> List[str]:
        if component_name == "body":
            return self.body_names
        elif component_name == "right_hand":
            return self.right_hand_names
        elif component_name == "left_hand":
            return self.left_hand_names
        elif component_name == "face":
            return self.face_names
        elif component_name == "other":
            other_names = []
            for other_component in self.ferret_data.other.values():
                other_names.extend(other_component.trajectory_names)
            return other_names
        else:
            if component_name in self.ferret_data.other.keys():
                return self.ferret_data.other[component_name].trajectory_names

        raise ValueError(f"Component {component_name} not found.")


    def __str__(self):
        return str(self.ferret_data)
