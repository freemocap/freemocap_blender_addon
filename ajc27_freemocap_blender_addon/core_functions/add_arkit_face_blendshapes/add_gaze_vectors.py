import bpy
from mathutils import Matrix
import math

def add_gaze_vectors(
    data_parent_name: str,
    cylinder_radius: float = 0.005,
    view_depth: float = 1.0,
    focus_aperture_degrees: float = 2.0,
    peripheral_horizontal_degrees: float = 120.0,
    peripheral_vertical_degrees: float = 120.0,
    transparency: float = 0.5,
    driver_multiplier: float = 0.5
):
    """
    Creates left and right gaze vectors that originate from the right_eye and left_eye empties.
    For each eye, it creates:
      - central_side_vector: cylinder reference for head direction (no drivers)
      - focus_view: cone representing foveal vision (2 deg) (with drivers)
      - peripheral_view: oval cone representing peripheral vision (100x130 deg) (with drivers)
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

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Create the gaze_vectors empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    gaze_vectors_empty = bpy.context.active_object
    gaze_vectors_empty.name = "gaze_vectors"
    gaze_vectors_empty.parent = data_parent
    gaze_vectors_empty.hide_set(True)

    eyes_info = [
        {"side": "Right", "target": right_eye_empty, "color": (1.0, 0.0, 0.0, 1.0)},
        {"side": "Left", "target": left_eye_empty, "color": (0.0, 0.0, 1.0, 1.0)}
    ]

    for info in eyes_info:
        side = info["side"]
        side_lower = side.lower()
        target = info["target"]
        
        # Create Material
        mat_name = f"Gaze_{side}"
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            
        # Enable Alpha Blending for Transparency
        mat.blend_method = 'BLEND'
        
        # Set Viewport Color (so it's visible in solid mode)
        mat.diffuse_color = (info["color"][0], info["color"][1], info["color"][2], transparency)

        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (info["color"][0], info["color"][1], info["color"][2], transparency)
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = transparency

        objects_to_create = [
            {
                "name": f"central_sight_vector_{side_lower}",
                "type": "cylinder",
                "use_drivers": False
            },
            {
                "name": f"focus_view_{side_lower}",
                "type": "cone",
                "horizontal_aperture": focus_aperture_degrees,
                "vertical_aperture": focus_aperture_degrees,
                "use_drivers": True
            },
            {
                "name": f"peripheral_view_{side_lower}",
                "type": "cone",
                "horizontal_aperture": peripheral_horizontal_degrees,
                "vertical_aperture": peripheral_vertical_degrees,
                "use_drivers": True
            }
        ]

        for obj_data in objects_to_create:
            if obj_data["type"] == "cylinder":
                bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius, depth=view_depth, location=(0, 0, 0))
                obj = bpy.context.active_object
                obj.name = obj_data["name"]
                
                mesh = obj.data
                for v in mesh.vertices:
                    y = v.co.y
                    z = v.co.z
                    v.co.y = -z
                    v.co.z = y
                    v.co.y += view_depth / 2.0
                    
            elif obj_data["type"] == "cone":
                bpy.ops.mesh.primitive_cone_add(radius1=1.0, radius2=0, depth=view_depth, location=(0, 0, 0))
                obj = bpy.context.active_object
                obj.name = obj_data["name"]
                
                # Calculate radii based on specified apertures
                radius_x = view_depth * math.tan(math.radians(obj_data["horizontal_aperture"] / 2.0))
                radius_z = view_depth * math.tan(math.radians(obj_data["vertical_aperture"] / 2.0))
                
                mesh = obj.data
                for v in mesh.vertices:
                    y = v.co.y
                    z = v.co.z
                    
                    # Rotate 90 degrees around X
                    v.co.y = -z
                    v.co.z = y
                    
                    # Shift forward by half depth so origin/tip is at bottom
                    v.co.y += view_depth / 2.0
                    
                    # Scale X and Z to get the desired base aperture
                    v.co.x *= radius_x
                    v.co.z *= radius_z
            
            # Common setup
            obj.parent = gaze_vectors_empty
            
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
                
            obj.rotation_mode = 'XYZ'
            
            # Add constraints
            # 1. Copy Location
            loc_constraint = obj.constraints.new(type='COPY_LOCATION')
            loc_constraint.target = target

            # 2. Copy Rotation
            rot_constraint = obj.constraints.new(type='COPY_ROTATION')
            rot_constraint.target = armature
            rot_constraint.subtarget = "face" # Assumes there is a 'face' bone
            rot_constraint.mix_mode = 'ADD'
            rot_constraint.target_space = 'WORLD'
            rot_constraint.owner_space = 'WORLD'
            
            # Add Drivers
            if obj_data["use_drivers"] and arkit_blendshapes:
                # Driver X (Eye Pitch)
                driver_x = obj.driver_add("rotation_euler", 0)
                
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
                
                driver_x.driver.expression = f"(look_down - look_up) * {driver_multiplier}"

                # Driver Z (Eye Yaw)
                driver_z = obj.driver_add("rotation_euler", 2)
                
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
                    driver_z.driver.expression = f"(look_in - look_out) * {driver_multiplier}"
                else:
                    driver_z.driver.expression = f"(look_out - look_in) * {driver_multiplier}"

