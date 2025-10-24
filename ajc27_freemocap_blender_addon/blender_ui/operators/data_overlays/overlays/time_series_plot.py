import numpy as np
import bpy
import gpu
import blf
from gpu_extras.batch import batch_for_shader

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_component import OverlayComponent

# TODO: Move the shared methods to a utility module

class TimeSeriesPlot(OverlayComponent):
    def __init__(
        self,
        name,
        data_path,
        column_index,
        window_size=100,
        position=(10, 10),
        size=(200, 150),
        plot_title="",
        line_color=(0.371235,0.672444,0.693872,1.0),
        current_frame_line_color=(0.693868,0.082283,0.095308,1.0),
        background_color=(0.0185,0.056129,0.05448,0.2),
        line_width=1.0,
        current_frame_line_width=1.5,
        border_line_width=1.0,
        value_unit="°",
        title_height_percentage=0.15,
        min_font_size=8,
        max_font_size=44,
    ):
        super().__init__(name, position, size)
        # Load time series data from numpy file
        self.time_series_data = np.load(data_path)[:, column_index]
        self.window_size = window_size
        self.current_frame = bpy.context.scene.frame_current
        
        # Set y-axis limits based on data range with 10% padding
        self.y_min = np.min(self.time_series_data) * 0.9
        self.y_max = np.max(self.time_series_data) * 1.1
        
        # Create shader for line drawing
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        # Create shader for background (supports transparency)
        self.background_shader = gpu.shader.from_builtin('UNIFORM_COLOR')

        self.plot_title = plot_title
        self.line_color = line_color
        self.current_frame_line_color = current_frame_line_color
        self.background_color = background_color
        self.line_width = line_width
        self.current_frame_line_width = current_frame_line_width
        self.border_line_width = border_line_width
        self.value_unit = value_unit
        self.title_height_percentage = title_height_percentage
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size

        # Calculate title area and plot area
        self.title_area_height = int(self.size[1] * self.title_height_percentage)
        self.plot_area_height = self.size[1] - self.title_area_height

        # Set up font for text rendering
        self.font_id = 0  # Default font
        self.font_size = self.calculate_optimal_font_size()

    def calculate_optimal_font_size(self):
        """Calculate the optimal font size based on title area dimensions and title text"""
        if not self.plot_title:
            return self.min_font_size
        
        # Start with the maximum font size
        test_font_size = self.max_font_size
        
        # Calculate available width and height in title area
        available_width = self.size[0] * 0.9
        available_height = self.title_area_height * 0.6
        
        # Test different font sizes to find the best fit
        while test_font_size >= self.min_font_size:
            blf.size(self.font_id, test_font_size)
            text_width, text_height = blf.dimensions(self.font_id, self.plot_title)
            
            # Check if text fits within available space
            if text_width <= available_width and text_height <= available_height:
                return test_font_size
            
            # Reduce font size and try again
            test_font_size -= 1
        
        # If no suitable size found, return minimum
        return self.min_font_size

    def get_text_width(self, text):
        """Calculate the actual width of text in pixels"""
        blf.size(self.font_id, self.font_size)
        width, height = blf.dimensions(self.font_id, text)
        return width

    def get_text_height(self, text, font_size=None):
        """Calculate the actual height of text in pixels"""
        if font_size is None:
            font_size = self.font_size
        blf.size(self.font_id, font_size)
        width, height = blf.dimensions(self.font_id, text)
        return height

    def get_window_data(self):
        """Get data points for the current frame window"""
        current_frame = bpy.context.scene.frame_current
        half_window = self.window_size // 2
        
        # Calculate window bounds
        start = max(0, current_frame - half_window)
        end = min(len(self.time_series_data), current_frame + half_window)
        
        # Get x coordinates (frame numbers)
        x_frames = np.arange(start, end)
        
        # Get corresponding time series values
        y_values = self.time_series_data[start:end]
        
        return x_frames, y_values
    
    def draw_text(self, text, position, color=(1, 1, 1, 1), font_size=None):
        """Helper function to draw text using blf"""
        if font_size is None:
            font_size = self.font_size
        blf.position(self.font_id, position[0], position[1], 0)
        blf.size(self.font_id, font_size)
        blf.color(self.font_id, color[0], color[1], color[2], color[3])
        blf.draw(self.font_id, text)

    def draw_background(self):
        """Draw a semi-transparent background rectangle"""
        # Enable blending for transparency
        gpu.state.blend_set('ALPHA')

        # Define the four corners of the background rectangle
        vertices = [
            (self.position[0], self.position[1]),  # Bottom-left
            (self.position[0] + self.size[0], self.position[1]),  # Bottom-right
            (self.position[0] + self.size[0], self.position[1] + self.size[1]),  # Top-right
            (self.position[0], self.position[1] + self.size[1]),  # Top-left
        ]
        
        # Define the two triangles that make up the rectangle
        indices = [(0, 1, 2), (0, 2, 3)]
        
        # Create and draw the batch
        batch = batch_for_shader(self.background_shader, 'TRIS', {"pos": vertices}, indices=indices)
        self.background_shader.bind()
        self.background_shader.uniform_float("color", self.background_color)
        batch.draw(self.background_shader)
    
    def draw(self):
        if not self.visible:
            return
        
        # Draw background first (so other elements appear on top)
        self.draw_background()

        # Get current window data
        x_frames, y_values = self.get_window_data()
        if len(x_frames) < 2:
            print("Not enough data points to draw")
            return
        
        # Calculate plot area position (below title area)
        plot_area_y = self.position[1]  # Plot area starts at bottom
        plot_area_height = self.plot_area_height

        # Normalize coordinates to plot area (excluding title area)
        x_coords = np.interp(x_frames, 
                            [x_frames[0], x_frames[-1]],
                            [self.position[0], self.position[0] + self.size[0]])
        
        y_coords = np.interp(y_values,
                            [self.y_min, self.y_max],
                            [plot_area_y, plot_area_y + plot_area_height])

        # Create line vertices
        vertices = np.column_stack((x_coords, y_coords)).tolist()
        
        # Draw line
        gpu.state.line_width_set(self.line_width)
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": vertices})
        self.shader.bind()
        self.shader.uniform_float("color", self.line_color)
        batch.draw(self.shader)
        gpu.state.line_width_set(1.0)  # Reset to default

        # Draw frame marker (vertical line at current frame)
        # Ensure current frame is within our window
        if x_frames[0] <= bpy.context.scene.frame_current <= x_frames[-1]:
            current_x = np.interp(bpy.context.scene.frame_current,
                                 [x_frames[0], x_frames[-1]],
                                 [self.position[0], self.position[0] + self.size[0]])
            
            marker_vertices = [
                (current_x, plot_area_y),  # Start at bottom of plot area
                (current_x, plot_area_y + plot_area_height)  # End at top of plot area
            ]
            
            gpu.state.line_width_set(self.current_frame_line_width)
            batch = batch_for_shader(self.shader, 'LINES', {"pos": marker_vertices})
            self.shader.uniform_float("color", self.current_frame_line_color)
            batch.draw(self.shader)
            gpu.state.line_width_set(1.0)  # Reset to default
        
        # Draw border around the plot area for reference
        border_vertices = [
            (self.position[0], self.position[1]),
            (self.position[0] + self.size[0], self.position[1]),
            (self.position[0] + self.size[0], self.position[1] + self.size[1]),
            (self.position[0], self.position[1] + self.size[1]),
            (self.position[0], self.position[1])
        ]
        
        gpu.state.line_width_set(self.border_line_width)
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": border_vertices})
        self.shader.uniform_float("color", (0.5, 0.5, 0.5, 1))
        batch.draw(self.shader)
        gpu.state.line_width_set(1.0)

        # Draw title in the title area (top portion)
        if self.plot_title:  # Only draw if title is not empty
            title_area_top = self.position[1] + self.size[1]  # Top of entire component
            title_area_bottom = title_area_top - self.title_area_height  # Bottom of title area
            
            # Calculate text dimensions for proper centering
            text_width = self.get_text_width(self.plot_title)
            text_height = self.get_text_height(self.plot_title)
            
            # Center title horizontally and vertically in title area
            title_x = self.position[0] + (self.size[0] - text_width) / 2
            title_y = title_area_bottom + (self.title_area_height - text_height) / 2
            
            self.draw_text(self.plot_title, (title_x, title_y))
        
        # Draw current value at the bottom of the plot area
        if x_frames[0] <= bpy.context.scene.frame_current <= x_frames[-1]:
            current_value = self.time_series_data[bpy.context.scene.frame_current]
            value_text = f"{current_value:.2f}{self.value_unit}"
            
            # Calculate value font size based on plot area height
            # Use a percentage of the plot area height for the value text
            value_font_size = max(self.min_font_size, min(self.max_font_size, int(self.plot_area_height * 0.15)))
            
            value_position = (
                self.position[0] + 5,
                plot_area_y + 15  # Bottom of plot area + small margin
            )
            self.draw_text(value_text, value_position, (1, 1, 0, 1), value_font_size)
