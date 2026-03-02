import csv
import bpy
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
            
        # Get the empty object
        empty = bpy.data.objects[empty_name]
        
        # Parent the empty object to the origin empty
        if data_parent_name in bpy.data.objects:
            empty.parent = bpy.data.objects[data_parent_name]
        else:
            print(f"Warning: Parent object '{data_parent_name}' not found!")
        
        # Create custom properties and animate them
        for i, column_name in enumerate(header_row[1:]):
            
            # Create a custom property if it doesn't exist
            if column_name not in empty.keys():
                empty[column_name] = 0.0
            
            # Read the values for this column
            values = [row[i+1] for row in rows]
            
            # Animate the custom property
            for j, value in enumerate(values):
                empty[column_name] = float(value)
                empty.keyframe_insert(data_path=f'["{column_name}"]', frame=j)
