from enum import Enum
import traceback
from pathlib import Path
from typing import Dict
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import ArmatureBoneInfo
from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement
import bpy
from mathutils import Vector, Matrix, Euler


from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH
from ajc27_freemocap_blender_addon.system.constants import (
    FREEMOCAP_ARMATURE,
    UE_METAHUMAN_SIMPLE_ARMATURE,
)
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType
from ajc27_freemocap_blender_addon.data_models.armatures.bone_name_map import (
    bone_name_map,
)
from ajc27_freemocap_blender_addon.data_models.meshes.skelly_bones import (
    get_skelly_bones,
)

SKELLY_MESH_PATH = str(Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_lowpoly_mesh.fbx")
SKELLY_BONES_PATH = str(Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones")

class AddSkellyMeshMethods(Enum):
    BY_BONE_MESH = "by_bone_mesh"
    COMPLETE_MESH = "complete_mesh"

def attach_skelly_mesh_to_rig(
    rig: bpy.types.Object,
    body_dimensions: Dict[str, float],
    add_mesh_method: AddSkellyMeshMethods = AddSkellyMeshMethods.BY_BONE_MESH,
) -> None:
    # Change to object mode
    if bpy.context.selected_objects != []:
        bpy.ops.object.mode_set(mode='OBJECT')

    if add_mesh_method == AddSkellyMeshMethods.BY_BONE_MESH:
        attach_skelly_by_bone_mesh(
            rig=rig,
        )
    elif add_mesh_method == AddSkellyMeshMethods.COMPLETE_MESH:
        attach_skelly_complete_mesh(
            rig=rig,
            body_dimensions=body_dimensions,
        )
    else:
        raise ValueError("Invalid add_mesh_method")    

def attach_skelly_by_bone_mesh(
    rig: bpy.types.Object,
    armature: Dict[str, ArmatureBoneInfo] = ArmatureType.FREEMOCAP,
    pose: Dict[str, PoseElement] = PoseType.FREEMOCAP_TPOSE,
) -> None:
    
    if armature == ArmatureType.UE_METAHUMAN_SIMPLE:
        armature_name = UE_METAHUMAN_SIMPLE_ARMATURE
    elif armature == ArmatureType.FREEMOCAP:
        armature_name = FREEMOCAP_ARMATURE
    else:
        raise ValueError("Invalid armature name")

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    #  Set the rig as active object
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig

    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the skelly bones dictionary
    skelly_bones = get_skelly_bones()

    #  Iterate through the skelly bones dictionary and update the
    #  default origin, length and normalized direction
    missing_meshes = []
    for mesh in skelly_bones:
        try:
            skelly_bones[mesh].bones_origin = Vector(rig.data.edit_bones[bone_name_map[armature_name][skelly_bones[mesh].bones[0]]].head)
            skelly_bones[mesh].bones_end = Vector(rig.data.edit_bones[bone_name_map[armature_name][skelly_bones[mesh].bones[-1]]].tail)
            skelly_bones[mesh].bones_length = (skelly_bones[mesh].bones_end - skelly_bones[mesh].bones_origin).length
        except KeyError as e:
            print(f"missing data for mesh: {mesh}, excluding it from final mesh")
            missing_meshes.append(mesh)
            continue
        except Exception as e:
            print(f"Error while updating skelly bones: {e}")
            print(traceback.format_exc())

    for mesh in missing_meshes:
        skelly_bones.pop(mesh)

    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Define the list that will contain the different Skelly meshes
    skelly_meshes = []

    # Iterate through the skelly bones dictionary and add the corresponding skelly mesh
    for mesh in skelly_bones:
        # print("Adding Skelly_" + mesh + " mesh...")
        try:
            # Import the skelly mesh
            mesh_path = SKELLY_BONES_PATH + '/Skelly_' + mesh + '.fbx'
            if not Path(mesh_path).is_file():
                raise FileNotFoundError(f"Could not find skelly mesh at {mesh_path}")
            bpy.ops.import_scene.fbx(filepath=str(mesh_path))

        except Exception as e:
            print(f"Error while importing skelly mesh: {e}")
            print(traceback.format_exc())
            continue

        skelly_meshes.append(bpy.data.objects['Skelly_' + mesh])

        # Get reference to the imported mesh
        skelly_mesh = bpy.data.objects['Skelly_' + mesh]

        # Get the rotation matrix
        if mesh == 'head':
            rotation_matrix = Matrix.Identity(4)
        else:
            rotation_matrix = Euler(
                Vector(pose[bone_name_map[armature_name][mesh]].rotation),
                'XYZ',
            ).to_matrix()

        # Move the Skelly part to the equivalent bone's head location
        skelly_mesh.location = (skelly_bones[mesh].bones_origin
            + rotation_matrix @ Vector(skelly_bones[mesh].position_offset)
        )

        # Rotate the part mesh with the rotation matrix
        skelly_mesh.rotation_euler = rotation_matrix.to_euler('XYZ')

        # Get the bone length
        if skelly_bones[mesh].adjust_rotation:
            bone_length = (skelly_bones[mesh].bones_end - (skelly_bones[mesh].bones_origin + (rotation_matrix @ Vector(skelly_bones[mesh].position_offset)))).length
        elif mesh == 'head':
            # bone_length = rig.data.edit_bones[bone_name_map[armature_name][skelly_bones[mesh]['bones'][0]]].length
            bone_length = skelly_bones['spine'].bones_length / 3.123 # Head length to spine length ratio
        else:
            bone_length = skelly_bones[mesh].bones_length

        # Get the mesh length
        mesh_length = skelly_bones[mesh].mesh_length

        # Resize the Skelly part to match the bone length
        skelly_mesh.scale = (bone_length / mesh_length, bone_length / mesh_length, bone_length / mesh_length)

        # Adjust rotation if necessary
        if skelly_bones[mesh].adjust_rotation:
            # Save the Skelly part's original location
            part_location = Vector(skelly_mesh.location)

            # Get the direction vector
            bone_vector = skelly_bones[mesh].bones_end - skelly_bones[mesh].bones_origin
            # Get new bone vector after applying the position offset
            new_bone_vector = skelly_bones[mesh].bones_end - part_location
            
            # Apply the rotations to the Skelly part
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

            # Get the angle between the two vectors
            rotation_quaternion = bone_vector.rotation_difference(new_bone_vector)
            # Change the rotation mode
            skelly_mesh.rotation_mode = 'QUATERNION'
            # Rotate the Skelly part
            skelly_mesh.rotation_quaternion = rotation_quaternion

        # Apply the transformations to the Skelly part
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
 
    # Set material 'Base' as material 0 for all skelly bone meshes
    for skelly_mesh in skelly_meshes:
        skelly_mesh.data.materials[0] = bpy.data.materials['Bone']

    # Rename the first mesh to skelly_mesh
    skelly_meshes[0].name = "skelly_mesh"

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select all body meshes
    for skelly_mesh in skelly_meshes:
        skelly_mesh.select_set(True)

    # Set skelly_mesh as active
    bpy.context.view_layer.objects.active = skelly_meshes[0]
    
    # Join the body meshes
    bpy.ops.object.join()

    # Select the rig
    rig.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = rig
    # Parent the mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

def attach_skelly_complete_mesh(
    rig: bpy.types.Object,
    body_dimensions: Dict[str, float],
    skelly_mesh_path: str = SKELLY_MESH_PATH
) -> None:
    
    try:
        # Get the script filepath
        # Import the skelly mesh

        # skelly_mesh_path = file_path.parent.parent.parent /"assets"/"skelly_lowpoly_mesh.fbx"
        if not Path(skelly_mesh_path).is_file():
            raise FileNotFoundError(f"Could not find skelly mesh at {skelly_mesh_path}")
        bpy.ops.import_scene.fbx(filepath=str(skelly_mesh_path))

    except Exception as e:
        print(f"Error while importing skelly mesh: {e}")
        print(traceback.format_exc())
        
    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    # Select the rig
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig

    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get reference to the neck bone
    neck = rig.data.edit_bones['neck']

    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get the skelly mesh
    skelly_mesh = bpy.data.objects['Skelly_LowPoly_Mesh']

    # Get the neck bone tail position and save it as the head position
    head_location = (neck.tail[0], neck.tail[1], neck.tail[2])
    # Set the location of the skelly mesh
    skelly_mesh.location = head_location

    # Get the body mesh z dimension
    raw_body_mesh_wingspan_width = skelly_mesh.dimensions.x
    raw_body_mesh_toe_to_heel_depth = skelly_mesh.dimensions.y
    raw_body_mesh_height = skelly_mesh.dimensions.z

    # Calculate the proportion between the rig and the mesh
    rig_to_body_mesh_height_ratio =  body_dimensions['total_height'] / raw_body_mesh_height 
    rig_to_body_mesh_wingspan_ratio =   body_dimensions['total_wingspan'] /raw_body_mesh_wingspan_width 
    rig_to_body_mesh_toe_to_toe_ratio = body_dimensions['mean_foot_length'] /  raw_body_mesh_toe_to_heel_depth 

    # Scale the mesh by the rig and body_mesh proportions multiplied by a scale factor
    skelly_mesh.scale = (rig_to_body_mesh_wingspan_ratio,
                            rig_to_body_mesh_toe_to_toe_ratio,
                            rig_to_body_mesh_height_ratio)


    # Set rig as active
    bpy.context.view_layer.objects.active = skelly_mesh

    # Select the skelly_mesh
    skelly_mesh.select_set(True)

    # Apply transformations to the mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Change skelly mesh origin to (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    ### Parent the skelly_mesh with the rig
    # Select the rig
    rig.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = rig
    # Parent the body_mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # Rename the skelly mesh to fmc_mesh
    skelly_mesh.name = 'skelly_mesh'



