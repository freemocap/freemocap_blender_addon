from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.skelly_mesh_paths import SKELLY_BONES_PATH
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import ArmatureBoneInfo
from ajc27_freemocap_blender_addon.data_models.armatures.bone_name_map import bone_name_map
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType
from ajc27_freemocap_blender_addon.data_models.meshes.skelly_bones import get_skelly_bones
from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement
from ajc27_freemocap_blender_addon.system.constants import UE_METAHUMAN_SIMPLE_ARMATURE, FREEMOCAP_ARMATURE

import bpy 

def attach_skelly_by_bone_mesh(
    rig: bpy.types.Object,
    armature: dict[str, ArmatureBoneInfo] = ArmatureType.FREEMOCAP,
    pose: dict[str, PoseElement] = PoseType.FREEMOCAP_TPOSE,
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
