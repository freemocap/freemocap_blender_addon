import bpy

def animate_skelly_blendshapes(data_parent_name: str):
    if data_parent_name not in bpy.data.objects:
        print(f"Warning: data_parent '{data_parent_name}' not found!")
        return

    data_parent = bpy.data.objects[data_parent_name]

    arkit_blendshapes = None
    skelly_mesh = None

    for child in data_parent.children_recursive:
        if "arkit_face_blendshapes" in child.name:
            arkit_blendshapes = child
        elif "skelly_mesh" in child.name:
            skelly_mesh = child

    if not arkit_blendshapes or not skelly_mesh:
        print("Warning: Missing required objects ('arkit_face_blendshapes' or 'skelly_mesh').")
        return

    if not skelly_mesh.data.shape_keys:
        print(f"Warning: '{skelly_mesh.name}' has no shape keys.")
        return

    shape_keys = skelly_mesh.data.shape_keys.key_blocks

    # Disable the Eyes_Mask (Mask modifier) in the skelly mesh
    for modifier in skelly_mesh.modifiers:
        if modifier.name == 'Eyes_Mask':
            modifier.show_viewport = False
            modifier.show_render = False
            break

    for prop_name in arkit_blendshapes.keys():
        # Avoid linking Blender's internal properties like _RNA_UI
        if prop_name.startswith("_"):
            continue
            
        if prop_name in shape_keys:
            shape_key = shape_keys[prop_name]
            
            # Create a driver for the shape key's value
            driver_fcurve = shape_key.driver_add("value")
            
            var = driver_fcurve.driver.variables.new()
            var.name = "blendshape_val"
            var.type = 'SINGLE_PROP'
            var.targets[0].id = arkit_blendshapes
            var.targets[0].data_path = f'["{prop_name}"]'
            
            driver_fcurve.driver.expression = var.name
