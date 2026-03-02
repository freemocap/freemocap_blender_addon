import bpy
from mathutils import Matrix
import math

def add_gaze_vectors(data_parent_name: str):
    """
    Creates left and right gaze vectors (cylinders) that originate from 
    the right_eye and left_eye empties and point in the direction of the actor's face.
    Their local rotations are driven by ARKit face blendshapes.
    """
    if data_parent_name not in bpy.data.objects:
        print(f"Warning: data_parent '{data_parent_name}' not found!")
        return

    data_parent = bpy.data.objects[data_parent_name]
    
    # 1. Find necessary objects
    right_eye_empty = None
    left_eye_empty = None
    armature = None
    arkit_blendshapes = None

    # Search recursively through all children of data_parent
    for child in data_parent.children_recursive:
        if "right_eye" in child.name:
            right_eye_empty = child
        elif "left_eye" in child.name:
            left_eye_empty = child
        elif "arkit_face_blendshapes" in child.name:
            arkit_blendshapes = child
        elif child.type == 'ARMATURE':
            armature = child
    if not right_eye_empty or not left_eye_empty or not armature:
        print("Warning: Missing required objects (right_eye, left_eye, or armature).")
        return
        
    cylinder_radius = 0.005
    cylinder_depth = 1.0

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    eyes_info = [
        {"name": "right_gaze_vector", "target": right_eye_empty, "side": "Right"},
        {"name": "left_gaze_vector", "target": left_eye_empty, "side": "Left"}
    ]

    for info in eyes_info:
        # Create cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius, depth=cylinder_depth, location=(0, 0, 0))
        cyl = bpy.context.active_object
        cyl.name = info["name"]
        
        # Add Material
        mat_name = "Gaze_Red" if info["side"] == "Right" else "Gaze_Blue"
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                if info["side"] == "Right":
                    bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0) # Red
                else:
                    bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 1.0, 1.0) # Blue
        
        if cyl.data.materials:
            cyl.data.materials[0] = mat
        else:
            cyl.data.materials.append(mat)
        
        # Orient the cylinder so it points along Y axis (face bone forward) 
        # and has its origin at the bottom (so it comes out of the eye)
        cyl_mesh = cyl.data
        for v in cyl_mesh.vertices:
            # First, rotate 90 degrees around X so the length goes along Y axis
            y = v.co.y
            z = v.co.z
            v.co.y = -z
            v.co.z = y
            # Then shift it forward by half depth so its origin is at the bottom
            v.co.y += cylinder_depth / 2.0

        cyl.parent = data_parent

        # Setup constraints
        # 1. Copy Location to eye empty
        loc_constraint = cyl.constraints.new(type='COPY_LOCATION')
        loc_constraint.target = info["target"]

        # 2. Copy Rotation from face bone
        rot_constraint = cyl.constraints.new(type='COPY_ROTATION')
        rot_constraint.target = armature
        rot_constraint.subtarget = "face" # Assumes there is a 'face' bone
        rot_constraint.mix_mode = 'ADD'
        rot_constraint.target_space = 'WORLD'
        rot_constraint.owner_space = 'WORLD'

        cyl.rotation_mode = 'XYZ'
        
        # Add Drivers for gaze direction (if arkit_blendshapes exists)
        if arkit_blendshapes:
            side = info["side"]
            
            # Eye Pitch (X rotation)
            # eyeLookUp drives positive/negative X? Depends on axes, let's say Up is -X and Down is +X
            driver_x = cyl.driver_add("rotation_euler", 0)
            
            var_up = driver_x.driver.variables.new()
            var_up.name = "look_up"
            var_up.type = 'SINGLE_PROP'
            var_up.targets[0].id = arkit_blendshapes
            var_up.targets[0].data_path = f'["eyeLookUp{side}"]'
            
            var_down = driver_x.driver.variables.new()
            var_down.name = "look_down"
            var_down.type = 'SINGLE_PROP'
            var_down.targets[0].id = arkit_blendshapes
            var_down.targets[0].data_path = f'["eyeLookDown{side}"]'
            
            # 30 degrees max rotation mapping (approx 0.5 radians)
            driver_x.driver.expression = "(look_down - look_up) * 0.5"

            # Eye Yaw (Z rotation)
            # eyeLookIn / eyeLookOut
            driver_z = cyl.driver_add("rotation_euler", 2)
            
            var_in = driver_z.driver.variables.new()
            var_in.name = "look_in"
            var_in.type = 'SINGLE_PROP'
            var_in.targets[0].id = arkit_blendshapes
            var_in.targets[0].data_path = f'["eyeLookIn{side}"]'
            
            var_out = driver_z.driver.variables.new()
            var_out.name = "look_out"
            var_out.type = 'SINGLE_PROP'
            var_out.targets[0].id = arkit_blendshapes
            var_out.targets[0].data_path = f'["eyeLookOut{side}"]'
            
            if side == "Right":
                # For Right eye: Look in (Left) is +Z, Look out (Right) is -Z
                driver_z.driver.expression = "(look_in - look_out) * 0.5"
            else:
                # For Left eye: Look in (Right) is -Z, Look out (Left) is +Z
                driver_z.driver.expression = "(look_out - look_in) * 0.5"

