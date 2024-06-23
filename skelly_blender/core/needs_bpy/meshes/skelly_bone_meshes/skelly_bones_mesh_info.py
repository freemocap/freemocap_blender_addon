from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import bpy

from skelly_blender import PACKAGE_ROOT_PATH
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_segments import BodySegments

SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones"


@dataclass
class SkellyBoneMeshInfo:
    mesh_path: str  # Path to the mesh
    host_bones: List[str]  # Bones of the mesh
    scale_reference_keypoint: BodyKeypoints

    # bones_origin: Union[Tuple[float, float, float], Vector]  # Origin of the bones
    # bones_end: Union[Tuple[float, float, float], Vector]  # End of the bones
    # bones_length: float  # Total length of the bones
    # mesh_length: float  # Length of the mesh
    # position_offset: Tuple[float, float, float]  # Position offset of the mesh
    # adjust_rotation: bool  # Adjust rotation of mesh after offset

    def __post_init__(self):
        self.mesh_path = str(Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path)

    @property
    def mesh_name(self) -> str:
        return (Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path).stem


@dataclass
class SkellyBoneMesh:
    name: str
    mesh: bpy.types.Object
    mesh_length: float


def load_skelly_fbx_meshes() -> Dict[str, bpy.types.Object]:
    meshes = {}
    for bone_mesh_segment_host, bone_mesh_info in SKELLY_BONE_MESHES.items():
        if not bone_mesh_info:
            continue

        bpy.ops.import_scene.fbx(filepath=str(bone_mesh_info.mesh_path))
        mesh = bpy.data.objects[bone_mesh_info.mesh_name]
        mesh_scale_reference = bpy.data.objects[bone_mesh_info.scale_reference_keypoint.blenderize().upper()]
        mesh_scale = mesh_scale_reference.location.length

        # # Make sure the object is selected and active
        # bpy.context.view_layer.objects.active = mesh
        # mesh.select_set(True)
        #
        # # Apply the scale transformation
        # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        #
        # # Deselect the object
        # mesh.select_set(False)

        # Store the mesh in the dictionary
        meshes[bone_mesh_segment_host] = SkellyBoneMesh(name=bone_mesh_info.mesh_name,
                                                        mesh=mesh,
                                                        mesh_length=mesh_scale)

        print(
            f"Loaded Mesh: '{bone_mesh_info.mesh_name}'\n"
            f"  Bone: '{bone_mesh_segment_host}'\n"
            f"  Path: '{bone_mesh_info.mesh_path}'\n"
            f"  Scale: {mesh_scale:.3f}"
        )

    return meshes


SKELLY_BONE_MESHES = {
    # BodySegments.SPINE_SACRUM_LUMBAR.blenderize(): "body/axial/skelly_pelvis.fbx",
    # BodySegments.SPINE_THORACIC.blenderize(): "body/axial/skelly_thoracic_spine.fbx",
    # BodySegments.SPINE_CERVICAL.blenderize(): "body/axial/skelly_cervical_spine.fbx",
    BodySegments.SKULL_NOSE.blenderize(): SkellyBoneMeshInfo(mesh_path="body/axial/skelly_skull.fbx",
                                                             host_bones=[BodySegments.SKULL_NOSE.blenderize()],
                                                             scale_reference_keypoint=BodyKeypoints.NOSE_TIP),
    BodySegments.SKULL_RIGHT_EYE_INNER.blenderize(): "",
    BodySegments.SKULL_RIGHT_EYE_CENTER.blenderize(): "",
    BodySegments.SKULL_RIGHT_EYE_OUTER.blenderize(): "",
    BodySegments.SKULL_RIGHT_EAR.blenderize(): "",
    BodySegments.SKULL_RIGHT_MOUTH.blenderize(): "",
    BodySegments.SKULL_LEFT_EYE_INNER.blenderize(): "",
    BodySegments.SKULL_LEFT_EYE_CENTER.blenderize(): "",
    BodySegments.SKULL_LEFT_EYE_OUTER.blenderize(): "",
    BodySegments.SKULL_LEFT_EAR.blenderize(): "",
    BodySegments.SKULL_LEFT_MOUTH.blenderize(): "",
    BodySegments.RIGHT_CLAVICLE.blenderize(): "",
    BodySegments.RIGHT_ARM_PROXIMAL.blenderize(): "",
    BodySegments.RIGHT_ARM_DISTAL.blenderize(): "",
    BodySegments.RIGHT_PALM_INDEX.blenderize(): "",
    BodySegments.RIGHT_PALM_PINKY.blenderize(): "",
    BodySegments.RIGHT_PALM_THUMB.blenderize(): "",
    BodySegments.PELVIS_RIGHT.blenderize(): "",
    BodySegments.RIGHT_LEG_THIGH.blenderize(): "",
    BodySegments.RIGHT_LEG_CALF.blenderize(): "",
    BodySegments.RIGHT_FOOT_FRONT.blenderize(): "",
    BodySegments.RIGHT_FOOT_HEEL.blenderize(): "",
    BodySegments.LEFT_CLAVICLE.blenderize(): "",
    BodySegments.LEFT_ARM_PROXIMAL.blenderize(): "",
    BodySegments.LEFT_ARM_DISTAL.blenderize(): "",
    BodySegments.LEFT_PALM_INDEX.blenderize(): "",
    BodySegments.LEFT_PALM_PINKY.blenderize(): "",
    BodySegments.LEFT_PALM_THUMB.blenderize(): "",
    BodySegments.PELVIS_LEFT.blenderize(): "",
    BodySegments.LEFT_LEG_THIGH.blenderize(): "",
    BodySegments.LEFT_LEG_CALF.blenderize(): "",
    BodySegments.LEFT_FOOT_FRONT.blenderize(): "",
    BodySegments.LEFT_FOOT_HEEL.blenderize(): "",
}

#
#
#
#
#
#
#
#
#
#
#     "body/axial/skelly_cervical_spine.fbx": SkellyBoneMeshInfo(
#         bones=[DefaultBoneConstraints.],
#         position_offset=(0, 0, 0.03),
#         adjust_rotation=False,
#     ),
#     BlenderizedAxialSegments.SPINE_CERVICAL.value: SkellyBoneMeshInfo(
#         bones=["spine", "spine.001", "neck"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.70856,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "upper_arm.R": SkellyBoneMeshInfo(
#         bones=["upper_arm.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.325418,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "upper_arm.L": SkellyBoneMeshInfo(
#         bones=["upper_arm.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.325418,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "forearm.R": SkellyBoneMeshInfo(
#         bones=["forearm.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.255504,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "forearm.L": SkellyBoneMeshInfo(
#         bones=["forearm.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.255504,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "hand.R": SkellyBoneMeshInfo(
#         bones=["hand.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.0845,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "hand.L": SkellyBoneMeshInfo(
#         bones=["hand.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.0845,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.01.R": SkellyBoneMeshInfo(
#         bones=["thumb.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.03675,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.01.L": SkellyBoneMeshInfo(
#         bones=["thumb.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.03675,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.02.R": SkellyBoneMeshInfo(
#         bones=["thumb.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.032224,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.02.L": SkellyBoneMeshInfo(
#         bones=["thumb.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.032224,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.03.R": SkellyBoneMeshInfo(
#         bones=["thumb.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.023374,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thumb.03.L": SkellyBoneMeshInfo(
#         bones=["thumb.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.023374,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "palm.01.R": SkellyBoneMeshInfo(
#         bones=["palm.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.085891,
#         position_offset=(0, -0.025, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.01.L": SkellyBoneMeshInfo(
#         bones=["palm.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.085891,
#         position_offset=(0, -0.025, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.02.R": SkellyBoneMeshInfo(
#         bones=["palm.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.085828,
#         position_offset=(0, -0.005, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.02.L": SkellyBoneMeshInfo(
#         bones=["palm.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.085828,
#         position_offset=(0, -0.005, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.03.R": SkellyBoneMeshInfo(
#         bones=["palm.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.082869,
#         position_offset=(0, 0.01, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.03.L": SkellyBoneMeshInfo(
#         bones=["palm.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.082869,
#         position_offset=(0, 0.01, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.04.R": SkellyBoneMeshInfo(
#         bones=["palm.04.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.070385,
#         position_offset=(0, 0.025, 0.02),
#         adjust_rotation=True,
#     ),
#     "palm.04.L": SkellyBoneMeshInfo(
#         bones=["palm.04.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.070385,
#         position_offset=(0, 0.025, 0.02),
#         adjust_rotation=True,
#     ),
#     "f_index.01.R": SkellyBoneMeshInfo(
#         bones=["f_index.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.053961,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_index.01.L": SkellyBoneMeshInfo(
#         bones=["f_index.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.053961,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_index.02.R": SkellyBoneMeshInfo(
#         bones=["f_index.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.033378,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_index.02.L": SkellyBoneMeshInfo(
#         bones=["f_index.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.033378,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_index.03.R": SkellyBoneMeshInfo(
#         bones=["f_index.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.024385,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_index.03.L": SkellyBoneMeshInfo(
#         bones=["f_index.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.024385,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.01.R": SkellyBoneMeshInfo(
#         bones=["f_middle.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.053792,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.01.L": SkellyBoneMeshInfo(
#         bones=["f_middle.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.053792,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.02.R": SkellyBoneMeshInfo(
#         bones=["f_middle.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.03347,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.02.L": SkellyBoneMeshInfo(
#         bones=["f_middle.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.03347,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.03.R": SkellyBoneMeshInfo(
#         bones=["f_middle.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.028028,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_middle.03.L": SkellyBoneMeshInfo(
#         bones=["f_middle.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.028028,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.01.R": SkellyBoneMeshInfo(
#         bones=["f_ring.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.046598,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.01.L": SkellyBoneMeshInfo(
#         bones=["f_ring.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.046598,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.02.R": SkellyBoneMeshInfo(
#         bones=["f_ring.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.036003,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.02.L": SkellyBoneMeshInfo(
#         bones=["f_ring.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.036003,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.03.R": SkellyBoneMeshInfo(
#         bones=["f_ring.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.024413,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_ring.03.L": SkellyBoneMeshInfo(
#         bones=["f_ring.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.024413,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.01.R": SkellyBoneMeshInfo(
#         bones=["f_pinky.01.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.039485,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.01.L": SkellyBoneMeshInfo(
#         bones=["f_pinky.01.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.039485,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.02.R": SkellyBoneMeshInfo(
#         bones=["f_pinky.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.027034,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.02.L": SkellyBoneMeshInfo(
#         bones=["f_pinky.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.027034,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.03.R": SkellyBoneMeshInfo(
#         bones=["f_pinky.03.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.020288,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "f_pinky.03.L": SkellyBoneMeshInfo(
#         bones=["f_pinky.03.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.020288,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thigh.R": SkellyBoneMeshInfo(
#         bones=["thigh.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.42875,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "thigh.L": SkellyBoneMeshInfo(
#         bones=["thigh.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.42875,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "shin.R": SkellyBoneMeshInfo(
#         bones=["shin.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.412281,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "shin.L": SkellyBoneMeshInfo(
#         bones=["shin.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.412281,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "foot.R": SkellyBoneMeshInfo(
#         bones=["foot.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.226,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "foot.L": SkellyBoneMeshInfo(
#         bones=["foot.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.226,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "heel.02.R": SkellyBoneMeshInfo(
#         bones=["heel.02.R"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.150255,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
#     "heel.02.L": SkellyBoneMeshInfo(
#         bones=["heel.02.L"],
#         bones_origin=(0, 0, 0),
#         bones_end=(0, 0, 0),
#         bones_length=0,
#         mesh_length=0.150255,
#         position_offset=(0, 0, 0),
#         adjust_rotation=False,
#     ),
# }
