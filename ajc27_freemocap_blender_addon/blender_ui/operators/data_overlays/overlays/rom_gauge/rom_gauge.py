import numpy as np
import bpy
import gpu
import blf
import math
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_component import OverlayComponent
from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlays.rom_gauge.rom_gauge_angle_definitions import rom_gauge_angle_definitions

# TODO: Move the shared methods to a utility module

class ROMGauge(OverlayComponent):
    def __init__(
        self,
        name,
        data_path,
        column_index,
        position=(10, 10),
        size=(200, 200),  # Square gauge by default
        plot_title="ROM Gauge",
        background_color=(0.1, 0.1, 0.1, 0.2),
        reference_vector_color=(0.0, 1.0, 0.0, 1.0),  # Green reference
        rotation_vector_color=(1.0, 0.0, 0.0, 1.0),  # Red rotation
        line_width=2.0,
        border_line_width=1.0,
        title_height_percentage=0.15,
        min_font_size=8,
        max_font_size=44,
    ):
        super().__init__(name, position, size)
        
        # Load angle data from numpy file
        self.angle_data = np.load(data_path)[:, column_index]
        self.current_frame = bpy.context.scene.frame_current
        
        # Create shader for line drawing
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        # Create shader for background (supports transparency)
        self.background_shader = gpu.shader.from_builtin('UNIFORM_COLOR')

        self.plot_title = plot_title
        self.reference_vector = Vector(rom_gauge_angle_definitions.get(name, {}).get('reference_vector', (1, 0))).normalized()
        proximal_segment_vector = rom_gauge_angle_definitions.get(name, {}).get('proximal_segment_vector', None)
        if proximal_segment_vector is not None:
            self.proximal_segment_vector = Vector(proximal_segment_vector).normalized()
        else:
            self.proximal_segment_vector = None
        # self.proximal_segment_vector = Vector(rom_gauge_angle_definitions.get(name, {}).get('proximal_segment_vector', (0, -1))).normalized()
        self.rotation_plane_name = rom_gauge_angle_definitions.get(name, {}).get('rotation_plane_name', 'Unknown Plane')
        self.rotation_direction = rom_gauge_angle_definitions.get(name, {}).get('rotation_direction', 1)
        self.background_color = background_color
        self.reference_vector_color = reference_vector_color
        self.rotation_vector_color = rotation_vector_color
        self.line_width = line_width
        self.border_line_width = border_line_width
        self.title_height_percentage = title_height_percentage
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size

        # Calculate title area and gauge area
        self.title_area_height = int(self.size[1] * self.title_height_percentage)
        self.gauge_area_height = self.size[1] - self.title_area_height
        
        # Calculate gauge center and radius
        self.gauge_center_x = self.position[0] + self.size[0] / 2
        self.gauge_center_y = self.position[1] + self.gauge_area_height / 2
        self.gauge_radius = min(self.size[0], self.gauge_area_height) * 0.4  # 40% of min dimension

        # Set up font for text rendering
        self.font_id = 0  # Default font
        self.font_size = self.calculate_optimal_font_size()

    def get_current_angle(self):
        """Get the current angle based on the current frame"""
        current_frame = bpy.context.scene.frame_current
        if 0 <= current_frame < len(self.angle_data):
            return math.radians(self.angle_data[current_frame])
        return 0.0

    def rotate_vector_2d(self, vector, angle):
        """Rotate a 2D vector by a given angle (in radians)"""
        effective_angle = angle * self.rotation_direction
        cos_angle = math.cos(effective_angle)
        sin_angle = math.sin(effective_angle)
        x = vector.x * cos_angle - vector.y * sin_angle
        y = vector.x * sin_angle + vector.y * cos_angle
        return Vector((x, y))

    def calculate_optimal_font_size(self):
        """Calculate the optimal font size based on title area dimensions and title text"""
        if not self.plot_title:
            return self.min_font_size
        
        # Start with the maximum font size
        test_font_size = self.max_font_size
        
        # Calculate available width and height in title area
        available_width = self.size[0] * 0.9
        available_height = self.title_area_height * 0.8
        
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

    def get_text_width(self, text, font_size=None):
        """Calculate the actual width of text in pixels"""
        if font_size is None:
            font_size = self.font_size
        blf.size(self.font_id, font_size)
        width, height = blf.dimensions(self.font_id, text)
        return width

    def get_text_height(self, text, font_size=None):
        """Calculate the actual height of text in pixels"""
        if font_size is None:
            font_size = self.font_size
        blf.size(self.font_id, font_size)
        width, height = blf.dimensions(self.font_id, text)
        return height

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

    def draw_gauge_circle(self):
        """Draw the circular gauge background"""
        # Draw a simple circle outline
        circle_vertices = []
        num_segments = 32
        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = self.gauge_center_x + self.gauge_radius * math.cos(angle)
            y = self.gauge_center_y + self.gauge_radius * math.sin(angle)
            circle_vertices.append((x, y))
        
        gpu.state.line_width_set(1.0)
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": circle_vertices})
        self.shader.uniform_float("color", (0.7, 0.7, 0.7, 1.0))
        batch.draw(self.shader)

    def draw_vector(self, center_x, center_y, vector, length, color, draw_arrow=True):
        """Draw a vector from the center point with optional arrowhead"""
        # Calculate end point
        end_x = center_x + vector.x * length
        end_y = center_y + vector.y * length
        
        # Draw the vector line
        vertices = [
            (center_x, center_y),
            (end_x, end_y)
        ]
        
        gpu.state.line_width_set(self.line_width)
        batch = batch_for_shader(self.shader, 'LINES', {"pos": vertices})
        self.shader.uniform_float("color", color)
        batch.draw(self.shader)
        
        # Draw arrowhead if requested
        if draw_arrow:
            arrow_length = length * 0.2
            arrow_angle = math.atan2(vector.y, vector.x)
            
            # Arrowhead points
            arrow1_angle = arrow_angle + math.radians(135)
            arrow2_angle = arrow_angle - math.radians(135)
            
            arrow1_x = end_x + arrow_length * math.cos(arrow1_angle)
            arrow1_y = end_y + arrow_length * math.sin(arrow1_angle)
            arrow2_x = end_x + arrow_length * math.cos(arrow2_angle)
            arrow2_y = end_y + arrow_length * math.sin(arrow2_angle)
            
            arrow_vertices = [
                (end_x, end_y),
                (arrow1_x, arrow1_y),
                (end_x, end_y),
                (arrow2_x, arrow2_y)
            ]
            
            batch = batch_for_shader(self.shader, 'LINES', {"pos": arrow_vertices})
            batch.draw(self.shader)
        
        gpu.state.line_width_set(1.0)

    def draw(self):
        if not self.visible:
            return
        
        # Draw background first
        self.draw_background()

        # Draw gauge circle
        self.draw_gauge_circle()

        # Get current rotation angle from data
        current_angle = self.get_current_angle()

        # Calculate rotation vector by rotating reference vector using our 2D rotation function
        rotation_vector = self.rotate_vector_2d(self.reference_vector, current_angle)

        # Draw proximal segment vector (no arrow)
        if self.proximal_segment_vector:
            self.draw_vector(
                self.gauge_center_x, 
                self.gauge_center_y, 
                self.proximal_segment_vector, 
                self.gauge_radius, 
                (0.5, 0.5, 0.8, 1.0),  # Blue-ish color
                draw_arrow=False  # No arrow for proximal segment
            )

        # Draw reference vector
        self.draw_vector(
            self.gauge_center_x, 
            self.gauge_center_y, 
            self.reference_vector, 
            self.gauge_radius, 
            self.reference_vector_color
        )

        # Draw rotation vector
        self.draw_vector(
            self.gauge_center_x, 
            self.gauge_center_y, 
            rotation_vector, 
            self.gauge_radius, 
            self.rotation_vector_color
        )

        # Draw title in the title area
        if self.plot_title:
            title_area_top = self.position[1] + self.size[1]
            title_area_bottom = title_area_top - self.title_area_height
            
            text_width = self.get_text_width(self.plot_title)
            text_height = self.get_text_height(self.plot_title)
            
            title_x = self.position[0] + (self.size[0] - text_width) / 2
            title_y = title_area_bottom + (self.title_area_height - text_height) / 2
            
            self.draw_text(self.plot_title, (title_x, title_y))

        # Draw current angle value
        current_angle_degrees = math.degrees(current_angle)
        angle_text = f"{current_angle_degrees:.1f}°"
        
        # Calculate value font size based on gauge area
        value_font_size = max(self.min_font_size, min(self.max_font_size, int(self.gauge_area_height * 0.1)))
        text_width = self.get_text_width(angle_text, value_font_size)
        text_height = self.get_text_height(angle_text, value_font_size)
        
        # value_x = self.gauge_center_x - text_width / 2
        # value_y = self.gauge_center_y - text_height / 2

        value_x = self.position[0] + 5
        value_y = self.position[1] + 15
        
        self.draw_text(angle_text, (value_x, value_y), (1, 1, 0, 1), value_font_size)

        # Draw rotation plane name in lower right corner
        plane_font_size = max(self.min_font_size, min(self.max_font_size, int(self.gauge_area_height * 0.08)))
        plane_text_width = self.get_text_width(self.rotation_plane_name, plane_font_size)

        # Position in lower right corner with some margin
        plane_x = self.position[0] + self.size[0] - plane_text_width - 5
        plane_y = self.position[1] + 15

        self.draw_text(self.rotation_plane_name, (plane_x, plane_y), (0.8, 0.8, 0.8, 1.0), plane_font_size)

        # Draw border around the component
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
