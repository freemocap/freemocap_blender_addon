import csv
import bpy
import numpy as np
from pathlib import Path

def add_arkit_face_blendshapes(recording_folder: str, data_parent_name: str):
    recording_folder_path = Path(recording_folder)
    blendshapes_folder = recording_folder_path / "output_data" / "face_blendshapes"
    
    if not blendshapes_folder.exists():
        print(f"Face blendshapes folder not found at {blendshapes_folder}")
        return
        
    csv_files = list(blendshapes_folder.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {blendshapes_folder}")
        return
        
    csv_file_path = csv_files[0]
    
    # Open the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Get the header row
        header_row = next(reader)
        
        # Read the entire CSV file into a list of rows
        rows = list(reader)
        
        # Create a single empty object if it doesn't exist
        empty_name = "arkit_face_blendshapes"
        if empty_name not in bpy.data.objects:
            bpy.ops.object.empty_add(location=(0, 0, 0))
            empty = bpy.context.active_object
            empty.name = empty_name
            
        # Get the empty object and hide it in the viewport by default
        empty = bpy.data.objects[empty_name]
        empty.hide_set(True)
        
        # Parent the empty object to the origin empty
        if data_parent_name in bpy.data.objects:
            empty.parent = bpy.data.objects[data_parent_name]
        else:
            print(f"Warning: Parent object '{data_parent_name}' not found!")
        
        # ── Bulk-keyframe all blendshape custom properties ────────────────────
        num_frames = len(rows)
        start_frame = bpy.context.scene.frame_start
        frames = np.arange(start_frame, start_frame + num_frames, dtype=np.float32)

        # Build the action (and channelbag for Blender ≥ 4.4)
        action = bpy.data.actions.new(name=f"{empty_name}_Action")
        empty.animation_data_create()
        empty.animation_data.action = action

        if bpy.app.version >= (4, 4):
            slot       = action.slots.new(id_type='OBJECT', name=empty_name)
            layer      = action.layers.new("Layer")
            strip      = layer.strips.new(type='KEYFRAME')
            channelbag = strip.channelbag(slot, ensure=True)
            empty.animation_data.action_slot = action.slots[0]

        # Skip the first column (frame index / timestamp) and the constant
        # "BlendShapeCount" column (always 52, not useful as a custom property).
        blendshape_columns = [c for c in header_row[1:] if c != "BlendShapeCount"]

        for i, column_name in enumerate(blendshape_columns):

            # Ensure the custom property exists
            if column_name not in empty.keys():
                empty[column_name] = 0.0

            # Collect values for this column as a float32 array
            values = np.array([float(row[i + 1]) for row in rows], dtype=np.float32)

            # Build the data path Blender uses for custom-property fcurves
            data_path = f'["{column_name}"]'

            # Create the fcurve on the correct container
            if bpy.app.version >= (4, 4):
                fcurve = channelbag.fcurves.new(data_path=data_path, index=0)
            else:
                fcurve = action.fcurves.new(data_path=data_path, index=0)

            fcurve.keyframe_points.add(count=num_frames)

            # Interleave frames and values into a flat [f0, v0, f1, v1, …] array
            co = np.empty(2 * num_frames, dtype=np.float32)
            co[0::2] = frames   # frame numbers
            co[1::2] = values   # blendshape values

            fcurve.keyframe_points.foreach_set("co", co)
            fcurve.update()
