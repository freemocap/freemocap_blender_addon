import bpy

# Set the scene to use the Video Sequence Editor
bpy.context.scene.sequence_editor_create()

# Load your video
video_path = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_test_data\freemocap_test_data.mp4"
video_strip = bpy.context.scene.sequence_editor.sequences.new_movie(
    name="Video",
    filepath=video_path,
    channel=1,
    frame_start=1
)
print(f"Loaded video from {video_path} with duration {video_strip.frame_final_duration}")

# Add a text strip
text_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
    name="Text",
    type='TEXT',
    channel=2,
    frame_start=1,
    frame_end=video_strip.frame_final_duration
)
text_strip.text = "Your Text Here"
text_strip.font_size = 50
text_strip.location = (0.5, 0.5)  # Normalized screen coordinates

# Set render settings
bpy.context.scene.render.filepath = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_test_data\freemocap_test_data_overlay.mp4"
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
print(f"Rendering to {bpy.context.scene.render.filepath}")
# Render the video
bpy.ops.render.render(animation=True)

print("Done!")