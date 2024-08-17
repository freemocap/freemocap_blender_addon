import os
import io
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
from mathutils import Vector
import bpy

from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    VISUAL_COMPONENTS,
    COLOR_PALETTE,
)

from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler

class frame_number:
    def __init__(self, frame_info=None):
        self.position_x_pct = VISUAL_COMPONENTS['frame_number']['position_x_pct']
        self.position_y_pct = VISUAL_COMPONENTS['frame_number']['position_y_pct']

    def add_component(self,
                      frame=None,
                      frame_info=None):

        # Add "frame number / total frame count" to the frame
        frame = cv2.putText(
            frame, 
            (str(frame_info.frame_number).zfill(len(str(frame_info.total_frames)))
             + '/'
             + str(frame_info.total_frames)),
            (int(self.position_x_pct * frame_info.width),
             int(self.position_y_pct * frame_info.height)), 
            VISUAL_COMPONENTS['frame_number']['font'],
            VISUAL_COMPONENTS['frame_number']['fontScale'], 
            VISUAL_COMPONENTS['frame_number']['color'], 
            VISUAL_COMPONENTS['frame_number']['thickness'],
            VISUAL_COMPONENTS['frame_number']['lineType'],
        )
        
        return frame

class image:
    def __init__(self, frame_info=None, image_type=None):
        # Get the raw image
        try:
            self.image_raw = cv2.imread(VISUAL_COMPONENTS[image_type]['path'],
                                        cv2.IMREAD_UNCHANGED)
        except:
            print('Image not found: ' + VISUAL_COMPONENTS[image_type]['path'])
            self.image_raw = None
            return

        # Get the larger side of the image to use it as reference
        larger_side = max(frame_info.width, frame_info.height)

        # Set the image properties
        self.image_width = int(
            larger_side
            * VISUAL_COMPONENTS[image_type]['resize_largest_side_pct']
        )
        self.image_height = int(
            self.image_raw.shape[0]
            * self.image_width / self.image_raw.shape[1]
        )
        # Resize the image
        self.image = cv2.resize(self.image_raw,
                                (int(self.image_width),
                                 int(self.image_height))
        )
        
        # Get the rgb image and alpha mask
        self.image_rgb = self.image[:, :, :3]
        self.image_alpha_mask = (self.image[:, :, 3] / 255)[:,:,np.newaxis]

        # Get the x and y positions of the image
        image_position_x = int(
            frame_info.width
            * VISUAL_COMPONENTS[image_type]['position_x_pct']
        )
        image_position_y = int(
            frame_info.height
            * VISUAL_COMPONENTS[image_type]['position_y_pct']
        )

        # Adjust the position in case they get out of frame
        if image_position_x + self.image_width > frame_info.width:
            image_position_x = frame_info.width - self.image_width
        if image_position_y + self.image_height > frame_info.height:
            image_position_y = frame_info.height - self.image_height

        # Set the image position
        self.image_position     = (image_position_x, image_position_y)

    def add_component(self,
                      frame=None,
                      frame_info=None):
        
        # If the image is not found, return the same frame
        if self.image_raw is None:
            return frame

        # Get the frame subsection
        frame_subsection = frame[
            self.image_position[1]:self.image_position[1]+self.image_height,
            self.image_position[0]:self.image_position[0]+self.image_width
        ]
        
        # Create the composite using the alpha mask
        composite = (frame_subsection * (1 - self.image_alpha_mask)
                     + self.image_rgb * self.image_alpha_mask)
        
        # Append the composite to the frame
        frame[
            self.image_position[1]:self.image_position[1]+self.image_height,
            self.image_position[0]:self.image_position[0]+self.image_width
        ] = composite
        
        return frame
    
class logo(image):
    def __init__(self, frame_info):
        super().__init__(frame_info, 'logo')
        
class static_json_table():
    def __init__(self, frame_info, data_type):
        self.data_type = data_type
        self.position_x_pct = VISUAL_COMPONENTS[self.data_type]['position_x_pct']
        self.position_y_pct = VISUAL_COMPONENTS[self.data_type]['position_y_pct']
        self.data = None
        self.frame = None
        self.frame_info = frame_info
        self.table_lines = []
        self.table_pointer = 0

        with open(str(frame_info.file_directory)
                  + VISUAL_COMPONENTS[self.data_type]['relative_path']) as json_file:
            self.data = json.load(json_file)

        self.create_table_lines(1, self.data)

    def add_component(self,
                      frame=None,
                      frame_info=None):
        self.frame = frame
        self.frame_info = frame_info
        self.table_pointer = 0

        for line in self.table_lines:
            self.frame = self.put_text(line[0], line[1])

        return self.frame

    def create_table_lines(self, json_level, data):

        for key, value in data.items():
            if isinstance(value, dict):
                self.table_lines.append(
                    (json_level,
                     ' '*(json_level-1) + str(key).replace('_', ' '))
                )
                self.create_table_lines(json_level + 1, value)
            else:
                # If the value is a float, round it
                if type(value) == float:
                    value = round(
                        value,
                        VISUAL_COMPONENTS['static_json_table']['float_decimal_digits']
                    )

                self.table_lines.append(
                    (json_level,
                     ' '*(json_level-1) + str(key).replace('_', ' ') + ' : ' + str(value))
                )
    
    def put_text(self, json_level, text):

        self.table_pointer = (
            self.table_pointer
            + (VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['fontScale'])
            * 35
        )

        frame = cv2.putText(
            self.frame,
            text,
            (int(self.position_x_pct * self.frame_info.width),
             int(self.position_y_pct * self.frame_info.height + self.table_pointer)), 
            VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['font'],
            VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['fontScale'], 
            VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['color'], 
            VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['thickness'],
            VISUAL_COMPONENTS[self.data_type]['text_parameters']['level_' + str(json_level)]['lineType'],
        )

        return frame

class recording_parameters(static_json_table):
    def __init__(self, frame_info):
        super().__init__(frame_info, 'recording_parameters')

class mediapipe_skeleton_segment_lengths(static_json_table):
    def __init__(self, frame_info):
        super().__init__(frame_info, 'mediapipe_skeleton_segment_lengths')

class plot_com_bos():
    def __init__(self, frame_info):
        self.marker_index = { # Order is important to generate the convex BOS polygon
            'left_heel': frame_info.handler.body_names.index('left_heel'),
            'left_foot_index': frame_info.handler.body_names.index('left_foot_index'),
            'right_foot_index': frame_info.handler.body_names.index('right_foot_index'),
            'right_heel': frame_info.handler.body_names.index('right_heel'),
        }

    def add_component(self,
                      frame=None,
                      frame_info=None):
        
        frame_index = frame_info.frame_start + frame_info.frame_number

        # Get the x, y coordinates of the COM
        com_x = frame_info.handler.center_of_mass_trajectory[frame_index, 0][0]
        com_y = frame_info.handler.center_of_mass_trajectory[frame_index, 0][1]

        trajectory_frame_marker_xyz = frame_info.handler.body_frame_name_xyz

        base_of_support_points = {
            'x': [],
            'y': [],
            'z': [],
        }

        for marker_name, marker_index in self.marker_index.items():
            base_of_support_points['x'].append(trajectory_frame_marker_xyz[frame_index, marker_index][0] - com_x)
            base_of_support_points['y'].append(trajectory_frame_marker_xyz[frame_index, marker_index][1] - com_y)
            base_of_support_points['z'].append(trajectory_frame_marker_xyz[frame_index, marker_index][2])

        # Scattter chart labels
        scatter_labels = list(self.marker_index.keys())

        # Create the plot with size according to the component size
        fig, ax = plt.subplots(figsize=(
            6.4,
            6.4 * frame_info.height * VISUAL_COMPONENTS['plot_com_bos']['height_pct']
            / (frame_info.width * VISUAL_COMPONENTS['plot_com_bos']['width_pct']))
        )

        # Plot the COM
        ax.scatter(0,
                   0,
                   marker='o',
                   color=COLOR_PALETTE['dark_terra_cotta']['hex'], zorder=2
        )

        # Filter out points that are above the ground contact threshold
        filtered_base_of_support_points = {
            'x': [x for x, z in zip(base_of_support_points['x'], base_of_support_points['z'])
                  if z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
            'y': [y for y, z in zip(base_of_support_points['y'], base_of_support_points['z'])
                  if z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
            'z': [z for z in base_of_support_points['z']
                  if z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
        }

        # Plot the base of support
        ax.scatter(filtered_base_of_support_points['x'],
                   filtered_base_of_support_points['y'],
                   marker='o',
                   color=COLOR_PALETTE['crystal']['hex'],
                   zorder=2,
        )

        # Add labels
        plt.text(0, 0, 'COM', color=COLOR_PALETTE['crystal']['hex'], fontsize=12)

        # Filter the labels based on the filtered base of support points
        filtered_scatter_labels = [
            label for label, z in zip(scatter_labels, base_of_support_points['z'])
            if z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']
        ]

        for point in range(0, len(filtered_base_of_support_points['x'])):
            plt.text(filtered_base_of_support_points['x'][point],
                    filtered_base_of_support_points['y'][point],
                    filtered_scatter_labels[point],
                    color=COLOR_PALETTE['crystal']['hex'],
                    fontsize=12)

        # Connect the points to form a polygon if there are more than 1 point
        if len(filtered_base_of_support_points['x']) > 1:
            ax.plot(
                filtered_base_of_support_points['x'] + [filtered_base_of_support_points['x'][0]],
                filtered_base_of_support_points['y'] + [filtered_base_of_support_points['y'][0]],
                color='red',
                zorder=1
            )

        # Get the maximum value to set the axes limits if there are at least 1 point
        if len(filtered_base_of_support_points['x']) > 0:
            max_x_value = max(abs(x) for x in filtered_base_of_support_points['x'])
            max_y_value = max(abs(y) for y in filtered_base_of_support_points['y'])
            max_value = max(max_x_value, max_y_value)
        else:
            max_value = 10

        # Set the axes limits
        ax.set_xlim(-max_value * 1.1, max_value * 1.1)
        ax.set_ylim(-max_value * 1.1, max_value * 1.1)

        # Set the title and axes labels
        ax.set_title(
            'COM v/s BOS',
            color=COLOR_PALETTE['crystal']['hex'],
            fontsize=30
        )
        ax.set_xlabel(
            'X Position',
            color=COLOR_PALETTE['crystal']['hex'],
            fontsize=24
        )
        ax.set_ylabel(
            'Y Position',
            color=COLOR_PALETTE['crystal']['hex'],
            fontsize=24
        )
        ax.tick_params(
            axis='both',
            which='both',
            labelsize=14,
            colors=COLOR_PALETTE['dark_terra_cotta']['hex']
        )

        # Enable grid lines
        plt.grid(True)

        # Set the color of the gridlines
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        # Set the axes colors
        ax.spines['bottom'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['top'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['left'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['right'].set_color(COLOR_PALETTE['crystal']['hex'])

        # Adjust the padding around the plot area
        plt.subplots_adjust(left=0.18, right=0.95, bottom=0.2, top=0.85)

        # Set the background color and transparency
        ax.set_facecolor(COLOR_PALETTE['japanese_indigo']['hex'])
        ax.patch.set_alpha(0.7)
        fig.set_facecolor(COLOR_PALETTE['japanese_indigo']['hex'])
        fig.patch.set_alpha(0.7)

        # Convert the Matplotlib plot to an OpenCV image.
        fig.canvas.draw()

        # Convert the Matplotlib plot to a byte stream in memory.
        with io.BytesIO() as buffer:
            fig.savefig(buffer, format='png', transparent=False)
            buffer.seek(0)
            img_bytes = buffer.read()

        # Close the figure
        plt.close(fig)

        # Convert the byte stream to a numpy array.
        img_arr = np.frombuffer(img_bytes, dtype=np.uint8)

        # Decode the numpy array into an image.
        img = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)

        # Resize the component
        component = VISUAL_COMPONENTS['plot_com_bos']
        img_resized = cv2.resize(
            img,
            (
                int(frame_info.width * component['width_pct']),
                int(frame_info.height * component['height_pct'])
            ),
        )

        # Get the rgb channel and the alpha mask
        plot_img_resized_rgb = img_resized[:, :, :3]
        plot_img_resized_alpha_mask = (img_resized[:, :, 3] / 255)[:,:,np.newaxis]

        # Get the top left corner of the plot based on the frame dimensions
        plot_top_left_corner = (
            int(frame_info.width * component['topleft_x_pct']),
            int(frame_info.height * component['topleft_y_pct'])
        )

        # Get the frame subsection
        frame_subsection = frame[
            plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
            plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]
        ]
        
        # Create the composite using the alpha mask
        composite = (
            frame_subsection * (1 - plot_img_resized_alpha_mask)
            + plot_img_resized_rgb * plot_img_resized_alpha_mask
        )

        # Append the composite to the frame
        frame[
            plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
            plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]
        ] = composite

        return frame

class plot_foot_deviation():
    def __init__(self, frame_info):
        self.marker_index = {
            'hips_center': frame_info.handler.body_names.index('hips_center'),
            'left_hip': frame_info.handler.body_names.index('left_hip'),
            'right_hip': frame_info.handler.body_names.index('right_hip'),
            'left_heel': frame_info.handler.body_names.index('left_heel'),
            'left_foot_index': frame_info.handler.body_names.index('left_foot_index'),
            'right_heel': frame_info.handler.body_names.index('right_heel'),
            'right_foot_index': frame_info.handler.body_names.index('right_foot_index'),
        }

    def add_component(self,
                frame=None,
                frame_info=None):
        
        frame_index = frame_info.frame_start + frame_info.frame_number

        trajectory_frame_marker_xyz = frame_info.handler.body_frame_name_xyz

        # Get Hips and feet vectors
        right_hip_vector = (
            Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['right_hip']])
            - Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['hips_center']])
        )
        right_foot_vector = (
            Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['right_foot_index']])
            - Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['right_heel']])
        )
        left_hip_vector = (
            Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['left_hip']])
            - Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['hips_center']])
        )
        left_foot_vector = (
            Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['left_foot_index']])
            - Vector(trajectory_frame_marker_xyz[frame_index, self.marker_index['left_heel']])
        )

        # Calculate the angle between the vectors
        right_hip_foot_angle = (
            np.pi / 2
            - np.arccos(
                right_foot_vector.dot(right_hip_vector)
                / (right_hip_vector.magnitude * right_foot_vector.magnitude)
            )
        )
        left_hip_foot_angle = (
            np.pi / 2
            - np.arccos(
                left_foot_vector.dot(left_hip_vector)
                / (left_hip_vector.magnitude * left_foot_vector.magnitude)
            )
        )        
        # Define a foot length in cm for demonstration purposes
        foot_length = 30

        # Internal x-axis margin
        x_axis_internal_margin = 7

        # External x-axis margin
        x_axis_external_margin = 10

        # Define the fixed points for the scatter plot representation
        fixed_points = {
            'right_foot_origin' : (-(foot_length + x_axis_internal_margin), 0),
            'right_foot_90_degree' : (-(foot_length * 2 + x_axis_internal_margin), 0),
            'right_foot_0_degree' : (-(foot_length + x_axis_internal_margin), foot_length),
            'right_foot_-90_degree' : (-(x_axis_internal_margin), 0),
            'left_foot_origin' : (foot_length + x_axis_internal_margin, 0),
            'left_foot_90_degree' : (foot_length * 2 + x_axis_internal_margin, 0),
            'left_foot_0_degree' : (foot_length + x_axis_internal_margin, foot_length),
            'left_foot_-90_degree' : (x_axis_internal_margin, 0),
        }

        # Calculate the foot index using the angles
        right_foot_index_x  = -foot_length * np.sin(right_hip_foot_angle)
        right_foot_index_y  = foot_length * np.cos(right_hip_foot_angle)
        left_foot_index_x   = foot_length * np.sin(left_hip_foot_angle)
        left_foot_index_y   = foot_length * np.cos(left_hip_foot_angle)

        ### Plot setup ###

        # Create the plot objects
        fig, ax = plt.subplots(
            figsize=(
                6.4,
                6.4 * frame_info.height * VISUAL_COMPONENTS['plot_foot_deviation']['height_pct']
                / (frame_info.width * VISUAL_COMPONENTS['plot_foot_deviation']['width_pct'])
            )
        )

        # Plot the fixed points
        for fixed_point in fixed_points:
            ax.scatter(
                fixed_points[fixed_point][0],
                fixed_points[fixed_point][1],
                marker='o',
                color=COLOR_PALETTE['dark_terra_cotta']['hex'],
                zorder=2
            )

        # Add labels
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] - 12, 'RIGHT', color=COLOR_PALETTE['crystal']['hex'], fontsize=23, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] - 12, 'LEFT', color=COLOR_PALETTE['crystal']['hex'], fontsize=23, ha='center')
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] - 5, str(np.around(np.degrees(right_hip_foot_angle),1)) + '°', color=COLOR_PALETTE['crystal']['hex'], fontsize=22, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] - 5, str(np.around(np.degrees(left_hip_foot_angle),1)) + '°', color=COLOR_PALETTE['crystal']['hex'], fontsize=22, ha='center')
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] + 35, '0', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] + 35, '0', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center')
        plt.text(fixed_points['right_foot_origin'][0] - 35, fixed_points['right_foot_origin'][1], '90', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='right', va='center')
        plt.text(fixed_points['left_foot_origin'][0] + 35, fixed_points['left_foot_origin'][1], '90', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='left', va='center')
        plt.text(0, 0, '-90', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center', va='center')

        # Plot the line from foot origin to the foot index
        plt.plot(
            [fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][0] + right_foot_index_x],
            [fixed_points['right_foot_origin'][1], fixed_points['right_foot_origin'][1] + right_foot_index_y],
            color=COLOR_PALETTE['dark_terra_cotta']['hex'],
            linewidth=5,
            zorder = 1,
        )
        plt.plot(
            [fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][0] + left_foot_index_x],
            [fixed_points['left_foot_origin'][1], fixed_points['left_foot_origin'][1] + left_foot_index_y],
            color=COLOR_PALETTE['dark_terra_cotta']['hex'],
            linewidth=5,
            zorder = 1,
        )

        # Plot the foot index
        ax.scatter(
            fixed_points['right_foot_origin'][0] + right_foot_index_x,
            fixed_points['right_foot_origin'][1] + right_foot_index_y,
            marker='o',
            color=COLOR_PALETTE['crystal']['hex'],
            zorder=3,
            s=50,
        )
        ax.scatter(
            fixed_points['left_foot_origin'][0] + left_foot_index_x,
            fixed_points['left_foot_origin'][1] + left_foot_index_y,
            marker='o',
            color=COLOR_PALETTE['crystal']['hex'],
            zorder=3,
            s=50,
        )

        # Set plot title
        ax.set_title(
            'Foot Deviation',
            color=COLOR_PALETTE['crystal']['hex'],
            fontsize=30
        )

        # Set the axes limits
        ax.set_xlim(
            -(foot_length * 2 + x_axis_internal_margin + x_axis_external_margin),
            foot_length * 2 + x_axis_internal_margin + x_axis_external_margin
        )
        ax.set_ylim(
            -20,
            foot_length + x_axis_internal_margin
        )

        # Invert the y axis
        ax.invert_yaxis()

        # Adjust the padding around the plot area
        plt.subplots_adjust(left=0.1, right=0.9)

        # Hide the axes
        plt.axis('off')
        plt.gca().set_frame_on(False)

        # Set the axes colors
        ax.spines['bottom'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['top'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['left'].set_color(COLOR_PALETTE['crystal']['hex'])
        ax.spines['right'].set_color(COLOR_PALETTE['crystal']['hex'])

        # Set the background color and transparency
        fig.set_facecolor(COLOR_PALETTE['japanese_indigo']['hex'])
        fig.patch.set_alpha(0.7)

        # Convert the Matplotlib plot to an OpenCV image.
        fig.canvas.draw()

        # Convert the Matplotlib plot to a byte stream in memory.
        with io.BytesIO() as buffer:
            fig.savefig(buffer, format='png', transparent=False)
            buffer.seek(0)
            img_bytes = buffer.read()

        # Close the figure
        plt.close(fig)

        # Convert the byte stream to a numpy array.
        img_arr = np.frombuffer(img_bytes, dtype=np.uint8)

        # Decode the numpy array into an image.
        img = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)

        # Resize the component
        component = VISUAL_COMPONENTS['plot_foot_deviation']
        img_resized = cv2.resize(
            img,
            (int(frame_info.width * component['width_pct']),
            int(frame_info.height * component['height_pct'])),
        )

        # Get the rgb channel and the alpha mask
        plot_img_resized_rgb = img_resized[:, :, :3]
        plot_img_resized_alpha_mask = (img_resized[:, :, 3] / 255)[:,:,np.newaxis]

        # Get the top left corner of the plot based on the frame dimensions
        plot_top_left_corner = (
            int(frame_info.width * component['topleft_x_pct']),
            int(frame_info.height * component['topleft_y_pct'])
        )

        # Get the frame subsection
        frame_subsection = frame[
            plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
            plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]
        ]

        # Create the composite using the alpha mask
        composite = (
            frame_subsection * (1 - plot_img_resized_alpha_mask)
            + plot_img_resized_rgb * plot_img_resized_alpha_mask
        )

        # Append the composite to the frame
        frame[
            plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
            plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]
        ] = composite

        return frame
