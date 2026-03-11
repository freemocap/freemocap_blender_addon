import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH


def add_gaze_visuals(
    data_parent_name: str,
    driver_multiplier: float = 1.0,
    foveal_radius: float = 0.01, # In meters
    foveal_depth: float = 1.0, # In meters
    fov_depth: float = 1.0 # In meters
):
    """
    Appends pre-built gaze visual meshes from .blend files and applies the
    appropriate constraints and drivers to each one.

    For each eye it appends:
      - FOV_Limit_{side}:  copy location (eye empty) + copy rotation (face bone).
                           No drivers – represents the anatomical field-of-view limit.
      - FOV_Peripheral_{side}: copy location (eye empty) + copy rotation (face bone)
                           + eye-rotation drivers, representing the live gaze direction.

    Blend file paths (assets/gaze_visuals/):
      FOV_Peripheral_Left_HD.blend
      FOV_Peripheral_Right_HD.blend
      FOV_Limit_Left.blend
      FOV_Limit_Right.blend
    """
    if data_parent_name not in bpy.data.objects:
        print(f"Warning: data_parent '{data_parent_name}' not found!")
        return

    data_parent = bpy.data.objects[data_parent_name]

    # Find required scene objects
    right_eye_empty = None
    left_eye_empty = None
    armature = None
    arkit_blendshapes = None

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

    # Create gaze_visuals empty parent
    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    gaze_visuals_empty = bpy.context.active_object
    gaze_visuals_empty.name = "gaze_visuals"
    gaze_visuals_empty.parent = data_parent
    gaze_visuals_empty.hide_set(True)

    # Asset paths
    gaze_visuals_dir = Path(PACKAGE_ROOT_PATH) / "assets" / "gaze_visuals"

    asset_paths = {
        "FOV_Peripheral_Left":   str(gaze_visuals_dir / "FOV_Peripheral_Left_HD.blend"),
        "FOV_Peripheral_Right":  str(gaze_visuals_dir / "FOV_Peripheral_Right_HD.blend"),
        "FOV_Limit_Left":  str(gaze_visuals_dir / "FOV_Limit_Left.blend"),
        "FOV_Limit_Right": str(gaze_visuals_dir / "FOV_Limit_Right.blend"),
    }

    # Per-eye info
    eyes_info = [
        {
            "side": "Right",
            "target": right_eye_empty,
            "objects": [
                {"blend_key": "FOV_Limit_Right", "use_drivers": False, "type": "append"},
                {"blend_key": "FOV_Peripheral_Right", "use_drivers": True,  "type": "append"},
                {"blend_key": "FOV_Foveal_Right", "use_drivers": True,  "type": "cylinder"},
            ],
        },
        {
            "side": "Left",
            "target": left_eye_empty,
            "objects": [
                {"blend_key": "FOV_Limit_Left", "use_drivers": False, "type": "append"},
                {"blend_key": "FOV_Peripheral_Left", "use_drivers": True,  "type": "append"},
                {"blend_key": "FOV_Foveal_Left", "use_drivers": True,  "type": "cylinder"},
            ],
        },
    ]

    # Process each mesh
    # Keeps track of appended objects by blend_key so FOV_Peripheral can reference
    # the already-appended FOV_Limit object for the Geometry Nodes modifier.
    appended_objects: dict = {}
    for info in eyes_info:
        side   = info["side"]
        target = info["target"]

        for obj_info in info["objects"]:
            blend_key   = obj_info["blend_key"]
            use_drivers = obj_info["use_drivers"]
            obj_type    = obj_info["type"]

            appended_obj = None

            if obj_type == "append":
                blend_path = asset_paths[blend_key]
                # Append from .blend
                # Always append a fresh copy; Blender will auto-suffix the name
                # (e.g. FOV_Peripheral_Right.001) when multiple captures are loaded in the
                # same session.
                with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                    if blend_key in data_from.objects:
                        data_to.objects.append(blend_key)

                # Link the freshly appended object (parent is None = not yet in any scene)
                for obj in bpy.data.objects:
                    if blend_key in obj.name and obj.parent is None:
                        bpy.context.collection.objects.link(obj)
                        appended_obj = obj
                        break

                if appended_obj is None:
                    print(f"Warning: Could not append '{blend_key}' from {blend_path}")
                    continue
                    
                # Scale the appended mesh along all axes by the fov_depth parameter,
                # since the pre-built meshes are designed to be 1 meter in depth.
                appended_obj.scale = (fov_depth, fov_depth, fov_depth)

            elif obj_type == "cylinder":
                # Procedurally generate fovea cylinder
                bpy.ops.mesh.primitive_cylinder_add(radius=foveal_radius, depth=foveal_depth, location=(0, 0, 0))
                appended_obj = bpy.context.active_object
                appended_obj.name = blend_key
                
                mesh = appended_obj.data
                for vertex in mesh.vertices:
                    y = vertex.co.y
                    z = vertex.co.z
                    vertex.co.y = -z
                    vertex.co.z = y
                    vertex.co.y += foveal_depth / 2.0

                # Add Material
                material_name = "FOV_Foveal_Right" if info["side"] == "Right" else "FOV_Foveal_Left"
                material = bpy.data.materials.get(material_name)
                if material is None:
                    material = bpy.data.materials.new(name=material_name)
                    material.use_nodes = True
                    bsdf = material.node_tree.nodes.get("Principled BSDF")
                    if bsdf:
                        if info["side"] == "Right":
                            bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)
                        else:
                            bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 1.0, 1.0)
                
                if appended_obj.data.materials:
                    appended_obj.data.materials[0] = material
                else:
                    appended_obj.data.materials.append(material)

            # Parent to gaze_visuals empty
            appended_obj.parent = gaze_visuals_empty
            appended_obj.rotation_mode = 'XYZ'

            # Constraint 1: Copy Location → eye empty
            loc_con = appended_obj.constraints.new(type='COPY_LOCATION')
            loc_con.target = target

            # Constraint 2: Copy Rotation → face bone
            rot_con = appended_obj.constraints.new(type='COPY_ROTATION')
            rot_con.target      = armature
            rot_con.subtarget   = "face"
            rot_con.mix_mode    = 'ADD'
            rot_con.target_space = 'WORLD'
            rot_con.owner_space  = 'WORLD'

            # Drivers (FOV_Peripheral only)
            if use_drivers and arkit_blendshapes:

                # Driver X – Eye Pitch (look up / down)
                driver_x = appended_obj.driver_add("rotation_euler", 0)

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

                driver_x.driver.expression = (
                    f"(look_down - look_up) * {driver_multiplier}"
                )

                # Driver Z – Eye Yaw (look in / out)
                driver_z = appended_obj.driver_add("rotation_euler", 2)

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
                    driver_z.driver.expression = (
                        f"(look_in - look_out) * {driver_multiplier}"
                    )
                else:
                    driver_z.driver.expression = (
                        f"(look_out - look_in) * {driver_multiplier}"
                    )

            # Geometry Nodes modifier (FOV_Peripheral only)
            if use_drivers and "FOV_Peripheral" in blend_key:  # GN clipping is just for the Peripheral meshes, not Foveal
                limit_key = blend_key.replace("FOV_Peripheral", "FOV_Limit")  # e.g. "FOV_Limit_Right"
                limit_obj = appended_objects.get(limit_key)
                
                if limit_obj is not None:
                    # Geometry Nodes Clipping
                    gn_mod = appended_obj.modifiers.new(
                        name="GeoNodes_Clipping", type='NODES'
                    )
                    
                    # Create a new node group for this mesh
                    node_group = bpy.data.node_groups.new(
                        name=f"GN_Clipping_{blend_key}", type='GeometryNodeTree'
                    )
                    gn_mod.node_group = node_group
                    
                    # Create group input/output interfaces (Blender 4.0+ uses interface, older uses inputs/outputs)
                    if hasattr(node_group, "interface"):
                        node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
                        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
                    else:
                        node_group.inputs.new('NodeSocketGeometry', "Geometry")
                        node_group.outputs.new('NodeSocketGeometry', "Geometry")
                        
                    nodes = node_group.nodes
                    links = node_group.links
                    
                    input_node = nodes.new("NodeGroupInput")
                    input_node.location = (-400, 0)
                    
                    output_node = nodes.new("NodeGroupOutput")
                    output_node.location = (400, 0)
                    
                    # Object Info
                    obj_info = nodes.new("GeometryNodeObjectInfo")
                    obj_info.location = (-400, -200)
                    obj_info.transform_space = 'RELATIVE'
                    obj_info.inputs['Object'].default_value = limit_obj
                    
                    # Position
                    pos_node = nodes.new("GeometryNodeInputPosition")
                    pos_node.location = (-400, -400)
                    
                    # Normalize (Vector Math)
                    norm_node = nodes.new("ShaderNodeVectorMath")
                    norm_node.location = (-200, -400)
                    norm_node.operation = 'NORMALIZE'
                    
                    # Raycast
                    raycast = nodes.new("GeometryNodeRaycast")
                    raycast.location = (0, -200)
                    raycast.mapping = 'INTERPOLATED'
                    
                    # Not (Boolean Math)
                    bool_not = nodes.new("FunctionNodeBooleanMath")
                    bool_not.location = (200, -100)
                    bool_not.operation = 'NOT'
                    
                    # Delete Geometry
                    del_geom = nodes.new("GeometryNodeDeleteGeometry")
                    del_geom.location = (200, 0)
                    
                    # Link them up
                    links.new(input_node.outputs['Geometry'], del_geom.inputs['Geometry'])
                    links.new(obj_info.outputs['Geometry'], raycast.inputs['Target Geometry'])
                    links.new(pos_node.outputs['Position'], norm_node.inputs[0])
                    links.new(norm_node.outputs['Vector'], raycast.inputs['Ray Direction'])
                    
                    links.new(raycast.outputs['Is Hit'], bool_not.inputs[0])
                    links.new(bool_not.outputs['Boolean'], del_geom.inputs['Selection'])
                    
                    links.new(del_geom.outputs['Geometry'], output_node.inputs['Geometry'])

                else:
                    print(
                        f"Warning: Could not find '{limit_key}' to use as "
                        f"Geometry Nodes target for '{blend_key}'."
                    )

            # Store reference for later use (e.g. Geometry Nodes target)
            appended_objects[blend_key] = appended_obj

    # Hide FOV_Limit meshes
    for key, obj in appended_objects.items():
        if key.startswith("FOV_Limit"):
            obj.hide_set(True)
