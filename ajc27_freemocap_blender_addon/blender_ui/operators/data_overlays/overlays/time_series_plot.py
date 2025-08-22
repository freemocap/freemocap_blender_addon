import numpy as np
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_component import OverlayComponent

class TimeSeriesOverlay(OverlayComponent):
    def __init__(self, name, data_path, column_index, window_size=100, pos=(10, 10), size=(200, 150)):
        super().__init__(name, pos, size)
        # Load angle data from numpy file
        self.angle_data = np.load(data_path)[:, column_index]
        # Print max and min values for debugging
        print(f"Max angle: {np.max(self.angle_data)}, Min angle: {np.min(self.angle_data)}")
        print(f"Data length: {len(self.angle_data)}")
        self.window_size = window_size
        self.current_frame = bpy.context.scene.frame_current
        
        # Set y-axis limits based on data range with 10% padding
        self.y_min = np.min(self.angle_data) * 0.9
        self.y_max = np.max(self.angle_data) * 1.1
        
        # Create shader for line drawing
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')

    def get_window_data(self):
        """Get data points for the current frame window"""
        current_frame = bpy.context.scene.frame_current
        half_window = self.window_size // 2
        
        # Calculate window bounds
        start = max(0, current_frame - half_window)
        end = min(len(self.angle_data), current_frame + half_window)
        
        # Get x coordinates (frame numbers)
        x_frames = np.arange(start, end)
        
        # Get corresponding angle values
        y_values = self.angle_data[start:end]
        
        print(f"Current frame: {current_frame}, Window: {start}-{end}, Data points: {len(y_values)}")
        
        return x_frames, y_values

    def draw(self):
        if not self.visible:
            return

        # Get current window data
        x_frames, y_values = self.get_window_data()
        if len(x_frames) < 2:
            print("Not enough data points to draw")
            return

        # Normalize coordinates to overlay area
        x_coords = np.interp(x_frames, 
                            [x_frames[0], x_frames[-1]],
                            [self.pos[0], self.pos[0] + self.size[0]])
        
        y_coords = np.interp(y_values,
                            [self.y_min, self.y_max],
                            [self.pos[1], self.pos[1] + self.size[1]])

        print(f"X coords range: {x_coords[0]:.2f} to {x_coords[-1]:.2f}")
        print(f"Y coords range: {y_coords[0]:.2f} to {y_coords[-1]:.2f}")

        # Create line vertices
        vertices = np.column_stack((x_coords, y_coords)).tolist()
        
        # Draw line
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": vertices})
        self.shader.bind()
        self.shader.uniform_float("color", (1, 1, 1, 1))
        batch.draw(self.shader)

        # Draw frame marker (vertical line at current frame)
        # Ensure current frame is within our window
        if x_frames[0] <= bpy.context.scene.frame_current <= x_frames[-1]:
            current_x = np.interp(bpy.context.scene.frame_current,
                                 [x_frames[0], x_frames[-1]],
                                 [self.pos[0], self.pos[0] + self.size[0]])
            
            marker_vertices = [
                (current_x, self.pos[1]),
                (current_x, self.pos[1] + self.size[1])
            ]
            
            batch = batch_for_shader(self.shader, 'LINES', {"pos": marker_vertices})
            self.shader.uniform_float("color", (1, 0, 0, 1))
            batch.draw(self.shader)
        
        # Draw border around the plot area for reference
        border_vertices = [
            (self.pos[0], self.pos[1]),
            (self.pos[0] + self.size[0], self.pos[1]),
            (self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
            (self.pos[0], self.pos[1] + self.size[1]),
            (self.pos[0], self.pos[1])
        ]
        
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": border_vertices})
        self.shader.uniform_float("color", (0.5, 0.5, 0.5, 1))
        batch.draw(self.shader)
