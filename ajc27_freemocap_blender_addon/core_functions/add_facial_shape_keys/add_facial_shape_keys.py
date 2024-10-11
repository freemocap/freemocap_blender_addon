import csv
from pathlib import Path
import bpy

shape_keys_map = {
    'arkit' : {
        'browInnerUp': 'browInnerUp',
        'browDownLeft': 'browDownLeft',
        'browDownRight': 'browDownRight',
        'browOuterUpLeft': 'browOuterUpLeft',
        'browOuterUpRight': 'browOuterUpRight',
        'eyeLookUpLeft': 'eyeLookUpLeft',
        'eyeLookUpRight': 'eyeLookUpRight',
        'eyeLookDownLeft': 'eyeLookDownLeft',
        'eyeLookDownRight': 'eyeLookDownRight',
        'eyeLookInLeft': 'eyeLookInLeft',
        'eyeLookInRight': 'eyeLookInRight',
        'eyeLookOutLeft': 'eyeLookOutLeft',
        'eyeLookOutRight': 'eyeLookOutRight',
        'eyeBlinkLeft': 'eyeBlinkLeft',
        'eyeBlinkRight': 'eyeBlinkRight',
        'eyeSquintLeft': 'eyeSquintLeft',
        'eyeSquintRight': 'eyeSquintRight',
        'eyeWideLeft': 'eyeWideLeft',
        'eyeWideRight': 'eyeWideRight',
        'cheekPuff': 'cheekPuff',
        'cheekSquintLeft': 'cheekSquintLeft',
        'cheekSquintRight': 'cheekSquintRight',
        'noseSneerLeft': 'noseSneerLeft',
        'noseSneerRight': 'noseSneerRight',
        'jawOpen': 'jawOpen',
        'jawForward': 'jawForward',
        'jawLeft': 'jawLeft',
        'jawRight': 'jawRight',
        'mouthFunnel': 'mouthFunnel',
        'mouthPucker': 'mouthPucker',
        'mouthLeft': 'mouthLeft',
        'mouthRight': 'mouthRight',
        'mouthRollUpper': 'mouthRollUpper',
        'mouthRollLower': 'mouthRollLower',
        'mouthShrugUpper': 'mouthShrugUpper',
        'mouthShrugLower': 'mouthShrugLower',
        'mouthClose': 'mouthClose',
        'mouthSmileLeft': 'mouthSmileLeft',
        'mouthSmileRight': 'mouthSmileRight',
        'mouthFrownLeft': 'mouthFrownLeft',
        'mouthFrownRight': 'mouthFrownRight',
        'mouthDimpleLeft': 'mouthDimpleLeft',
        'mouthDimpleRight': 'mouthDimpleRight',
        'mouthUpperUpLeft': 'mouthUpperUpLeft',
        'mouthUpperUpRight': 'mouthUpperUpRight',
        'mouthLowerDownLeft': 'mouthLowerDownLeft',
        'mouthLowerDownRight': 'mouthLowerDownRight',
        'mouthPressLeft': 'mouthPressLeft',
        'mouthPressRight': 'mouthPressRight',
        'mouthStretchLeft': 'mouthStretchLeft',
        'mouthStretchRight': 'mouthStretchRight',
        'tongueOut': 'tongueOut',
    },
    'metahuman': {
        'CTRL_expressions_browRaiseInL': 'browInnerUp',
        'CTRL_expressions_browRaiseInR': 'browInnerUp',
        'CTRL_expressions_browDownL': 'browDownLeft',
        'CTRL_expressions_browDownR': 'browDownRight',
        'CTRL_expressions_browRaiseOuterL': 'browOuterUpLeft',
        'CTRL_expressions_browRaiseOuterR': 'browOuterUpRight',
        'CTRL_expressions_eyeBlinkL': 'eyeBlinkLeft',
        'CTRL_expressions_eyeBlinkR': 'eyeBlinkRight',
        'CTRL_expressions_eyeLookUpL': 'eyeLookUpLeft',
        'CTRL_expressions_eyeLookUpR': 'eyeLookUpRight',
        'CTRL_expressions_eyeLookDownL': 'eyeLookDownLeft',
        'CTRL_expressions_eyeLookDownR': 'eyeLookDownRight',
        'CTRL_expressions_eyeLookLeftL': 'eyeLookOutLeft',
        'CTRL_expressions_eyeLookLeftR': 'eyeLookInRight',
        'CTRL_expressions_eyeLookRightL': 'eyeLookInLeft',
        'CTRL_expressions_eyeLookRightR': 'eyeLookOutRight',
        'CTRL_expressions_eyeSquintInnerL': 'eyeSquintLeft',
        'CTRL_expressions_eyeSquintInnerR': 'eyeSquintRight',
        'CTRL_expressions_eyeWidenL': 'eyeWideLeft',
        'CTRL_expressions_eyeWidenR': 'eyeWideRight',
        'CTRL_expressions_eyeCheekRaiseL': 'cheekSquintLeft',
        'CTRL_expressions_eyeCheekRaiseR': 'cheekSquintRight',
        'CTRL_expressions_mouthCheekBlowL': 'cheekPuff',
        'CTRL_expressions_mouthCheekBlowR': 'cheekPuff',
        'CTRL_expressions_noseWrinkleL': 'noseSneerLeft',
        'CTRL_expressions_noseWrinkleR': 'noseSneerRight',
        'CTRL_expressions_jawOpen': 'jawOpen',
        'CTRL_expressions_jawFwd': 'jawForward',
        'CTRL_expressions_jawLeft': 'jawLeft',
        'CTRL_expressions_jawRight': 'jawRight',
        'CTRL_expressions_mouthFunnelDL': 'mouthFunnel',
        'CTRL_expressions_mouthFunnelDR': 'mouthFunnel',
        'CTRL_expressions_mouthFunnelUL': 'mouthFunnel',
        'CTRL_expressions_mouthFunnelUR': 'mouthFunnel',
        'CTRL_expressions_mouthLipsPurseDL': 'mouthPucker',
        'CTRL_expressions_mouthLipsPurseDR': 'mouthPucker',
        'CTRL_expressions_mouthLipsPurseUL': 'mouthPucker',
        'CTRL_expressions_mouthLipsPurseUR': 'mouthPucker',
        'CTRL_expressions_mouthLipsTowardsDL': 'mouthPucker',
        'CTRL_expressions_mouthLipsTowardsDR': 'mouthPucker',
        'CTRL_expressions_mouthLipsTowardsUL': 'mouthPucker',
        'CTRL_expressions_mouthLipsTowardsUR': 'mouthPucker',
        'CTRL_expressions_mouthLeft': 'mouthLeft',
        'CTRL_expressions_mouthRight': 'mouthRight',
        'CTRL_expressions_mouthUpperLipRollInL': 'mouthRollUpper',
        'CTRL_expressions_mouthUpperLipRollInR': 'mouthRollUpper',
        'CTRL_expressions_mouthLowerLipRollInL': 'mouthRollLower',
        'CTRL_expressions_mouthLowerLipRollInR': 'mouthRollLower',
        'CTRL_expressions_mouthUpperLipRollOutL': 'mouthShrugUpper',
        'CTRL_expressions_mouthUpperLipRollOutR': 'mouthShrugUpper',
        'CTRL_expressions_mouthLowerLipRollOutL': 'mouthShrugLower',
        'CTRL_expressions_mouthLowerLipRollOutR': 'mouthShrugLower',
        'CTRL_expressions_mouthLipsTogetherDL': 'mouthClose',
        'CTRL_expressions_mouthLipsTogetherDR': 'mouthClose',
        'CTRL_expressions_mouthLipsTogetherUL': 'mouthClose',
        'CTRL_expressions_mouthLipsTogetherUR': 'mouthClose',
        'CTRL_expressions_mouthDimpleL': 'mouthDimpleLeft',
        'CTRL_expressions_mouthDimpleR': 'mouthDimpleRight',
        'CTRL_expressions_mouthCornerPullL': 'mouthSmileLeft',
        'CTRL_expressions_mouthCornerPullR': 'mouthSmileRight',
        'CTRL_expressions_mouthCornerDepressL': 'mouthFrownLeft',
        'CTRL_expressions_mouthCornerDepressR': 'mouthFrownRight',
        'CTRL_expressions_mouthUpperLipRaiseL': 'mouthUpperUpLeft',
        'CTRL_expressions_mouthUpperLipRaiseR': 'mouthUpperUpRight',
        'CTRL_expressions_mouthLowerLipDepressL': 'mouthLowerDownLeft',
        'CTRL_expressions_mouthLowerLipDepressR': 'mouthLowerDownRight',
        'CTRL_expressions_mouthSharpCornerPullL': 'mouthPressLeft',
        'CTRL_expressions_mouthSharpCornerPullR': 'mouthPressRight',
        'CTRL_expressions_mouthStretchL': 'mouthStretchLeft',
        'CTRL_expressions_mouthStretchR': 'mouthStretchRight',
        'CTRL_expressions_tongueOut': 'tongueOut'
    }
}

def add_facial_shape_keys(
    recording_path: str,
    data_parent_object: bpy.types.Object,
) -> None:

    facial_shape_keys_parent = add_facial_shape_keys_parent(
        recording_path=recording_path,
        data_parent_object=data_parent_object,
    )
    # butterworth_filter_facial_shape_keys(
    #     facial_shape_keys_parent = facial_shape_keys_parent
    # )
    add_facial_shape_keys_to_mesh(
        mesh_name = 'skelly_mesh',
        shape_key_type = 'metahuman'
    )

    return

def add_facial_shape_keys_parent(
    recording_path: str,
    data_parent_object: bpy.types.Object,
) -> bpy.types.Object:
    
    # Define the path to the facecam folder
    facecam_folder = Path(recording_path) / "facecam"

    # Search if there is a file with .csv extension
    csv_files = list(facecam_folder.glob("*.csv"))

    if not csv_files:
        print("No CSV file found in the facecam folder.")
        return None
    else:
        csv_file = csv_files[0]

        # Open the CSV file
        with open(csv_file, 'r') as csvfile:

            reader = csv.reader(csvfile)
            
            # Get the header row
            header_row = next(reader)
            
            # Read the entire CSV file into a list of rows
            rows = list(reader)
            
            # Create a single empty object if it doesn't exist
            shapekeys_parent_name = "facial_shapekeys"
            if shapekeys_parent_name not in bpy.data.objects:
                bpy.ops.object.empty_add(location=(0, 0, 0))
                empty = bpy.context.active_object
                empty.name = shapekeys_parent_name
                
            # Get the empty object
            shapekeys_parent = bpy.data.objects[shapekeys_parent_name]

            # Parent the empty object to the data_parent_object
            shapekeys_parent.parent = data_parent_object

            # Hide the empty object
            shapekeys_parent.hide_set(True)
            
            # Create custom properties and animate them
            for i, shapekey_name in enumerate(header_row[2:]):
                
                # Create a custom property if it doesn't exist
                if shapekey_name not in shapekeys_parent.keys():
                    shapekeys_parent[shapekey_name] = 0.0
                
                # Read the shapekey_values for this column
                shapekey_values = [row[i+2] for row in rows]
                
                # Animate the custom property
                for j, shapekey_value in enumerate(shapekey_values):
                    shapekeys_parent[shapekey_name] = float(shapekey_value)
                    shapekeys_parent.keyframe_insert(data_path=f'["{shapekey_name}"]', frame=j)

    return shapekeys_parent

def butterworth_filter_facial_shape_keys(
    facial_shape_keys_parent: bpy.types.Object
) -> None:

    # If the facial_shape_keys_parent object doesn't exist, return
    if facial_shape_keys_parent is None:
        return

    # Deselect all objects
    for data_object in bpy.data.objects:
        data_object.select_set(False)

    # Save the current area
    current_area = bpy.context.area.type

    # Change the current area to the graph editor
    bpy.context.area.type = "GRAPH_EDITOR"

    # Apply the butterworth filter
    bpy.ops.graph.butterworth_smooth(
        cutoff_frequency=5,
        filter_order=4,
        samples_per_frame=1,
        blend=1.0,
        blend_in_out=1
    )
    
    # Restore the area
    bpy.context.area.type = current_area

    # Deselect all objects
    for data_object in bpy.data.objects:
        data_object.select_set(False)

    return
    
def add_facial_shape_keys_to_mesh(
    mesh_name: str = 'skelly_mesh',
    shape_key_type: str = 'metahuman'
) -> None:

    # Get a reference to the mesh object. If doesn't exist return
    if mesh_name not in bpy.data.objects:
        print(f"Could not find mesh object with name {mesh_name}.")
        return
    else:
        mesh = bpy.data.objects[mesh_name]

    # Get a reference to the shapekeys object. If doesn't exist return
    if 'facial_shapekeys' not in bpy.data.objects:
        print(f"Could not find shapekeys object with name 'facial_shapekeys'.")
        return
    else:
        mesh = bpy.data.objects['skelly_mesh']

    # Get a list of the custom properties of the object with the name 'facial_shapekeys'
    shapekeys = bpy.data.objects['facial_shapekeys'].keys()

    # Add the basis shapekey
    mesh.shape_key_add(from_mix=False)
    bpy.data.shape_keys["Key"].key_blocks["Key"].name = 'Basis'

    # Add the custom properties to the mesh, use an index for the shapekeys
    for i, shape_key in enumerate(shape_keys_map[shape_key_type]):
        mesh.shape_key_add(from_mix=False)
        bpy.context.object.active_shape_key_index = (i + 1)
        bpy.data.shape_keys["Key"].key_blocks["Key"].name = shape_key
        driver = bpy.data.shape_keys["Key"].key_blocks[shape_key].driver_add('value').driver
        driver.type = 'SCRIPTED'
        driver.expression = '0.0 + var'
        var = driver.variables.new()
        var.name = 'var'
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id = bpy.data.objects['facial_shapekeys']
        target.data_path = '["' + shape_keys_map[shape_key_type][shape_key] + '"]'



