import bpy
import math as m

def add_angle_meshes(
    joint_angle_list: list,
    points: list,
    mesh_type: str
) -> dict:

    angle_meshes = {}

    # for point in points:
    for i, joint_angle in enumerate(joint_angle_list):

        if mesh_type == 'angle':
            # Add a circle mesh to the scene
            bpy.ops.mesh.primitive_circle_add(
                enter_editmode=False,
                align='WORLD',
                location=(0, 0, 0),
                radius=0.05,
                fill_type='NGON'
            )
        elif mesh_type == 'angletext':
            # Add a text mesh to the scene
            bpy.ops.object.text_add(
                enter_editmode=False,
                align='WORLD',
                location=(0, 0, 0),
                rotation=(m.radians(90), 0, 0),
                scale=(1, 1, 1)
            )
    
        # Change the name of the circle mesh. Used "#" as the joint angle name
        # has a "_" separator
        bpy.context.active_object.name = mesh_type + "#" + joint_angle

        # Add a copy location constraint to the angle mesh
        bpy.ops.object.constraint_add(type='COPY_LOCATION')

        # Set the copy location target as the joint object
        bpy.context.object.constraints["Copy Location"].target = bpy.data.objects[points[i]]

        # Append the angle mesh to the angle meshes dictionary
        angle_meshes[joint_angle] = bpy.data.objects[mesh_type + "#" + joint_angle]

    return angle_meshes
