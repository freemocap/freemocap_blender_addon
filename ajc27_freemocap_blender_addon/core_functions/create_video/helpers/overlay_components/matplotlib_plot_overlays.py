import os
import bpy
import numpy as np

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.frame_information_dataclass import FrameInformation
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import VISUAL_COMPONENTS, COLOR_PALETTE


class OverlayPlotComBos:
    def __init__(self, frame_info: FrameInformation):
        self.scene = frame_info.scene

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        from matplotlib import pyplot as plt
        import cv2
        ### Data setup ###

        # Set the frame according to the frame number
        self.scene.frame_set(frame_info.frame_start + frame_info.frame_number)

        # Get the x, y coordinates of the COM
        com_x = bpy.data.objects['center_of_mass'].matrix_world.translation[0]
        com_y = bpy.data.objects['center_of_mass'].matrix_world.translation[1]

        # Get the coordinates of the base of support points
        base_of_support_points = {
            'x': [
                bpy.data.objects['left_heel'].matrix_world.translation[0] - com_x,
                bpy.data.objects['left_foot_index'].matrix_world.translation[0] - com_x,
                bpy.data.objects['right_foot_index'].matrix_world.translation[0] - com_x,
                bpy.data.objects['right_heel'].matrix_world.translation[0] - com_x,
            ],
            'y': [
                bpy.data.objects['left_heel'].matrix_world.translation[1] - com_y,
                bpy.data.objects['left_foot_index'].matrix_world.translation[1] - com_y,
                bpy.data.objects['right_foot_index'].matrix_world.translation[1] - com_y,
                bpy.data.objects['right_heel'].matrix_world.translation[1] - com_y,
            ],
            'z': [
                bpy.data.objects['left_heel'].matrix_world.translation[2],
                bpy.data.objects['left_foot_index'].matrix_world.translation[2],
                bpy.data.objects['right_foot_index'].matrix_world.translation[2],
                bpy.data.objects['right_heel'].matrix_world.translation[2],
            ],
        }

        # Scattter chart labels
        scatter_labels = [
            'left_heel',
            'left_foot_index',
            'right_foot_index',
            'right_heel',
        ]

        ### Plot setup ###
        # Create the plot with size according to the component size
        fig, ax = plt.subplots(figsize=(6.4,
                                        6.4 * frame_info.height * VISUAL_COMPONENTS['plot_com_bos']['height_pct'] / (
                                                frame_info.width * VISUAL_COMPONENTS['plot_com_bos']['width_pct'])))

        # Plot the COM
        ax.scatter(0, 0, marker='o', color=COLOR_PALETTE['dark_terra_cotta']['hex'], zorder=2)

        # Filter out points that are above the ground contact threshold
        filtered_base_of_support_points = {
            'x': [x for x, z in zip(base_of_support_points['x'], base_of_support_points['z']) if
                  z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
            'y': [y for y, z in zip(base_of_support_points['y'], base_of_support_points['z']) if
                  z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
            'z': [z for z in base_of_support_points['z'] if
                  z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']],
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
        filtered_scatter_labels = [label for label, z in zip(scatter_labels, base_of_support_points['z']) if
                                   z < VISUAL_COMPONENTS['plot_com_bos']['ground_contact_threshold']]

        for point in range(0, len(filtered_base_of_support_points['x'])):
            plt.text(filtered_base_of_support_points['x'][point],
                     filtered_base_of_support_points['y'][point],
                     filtered_scatter_labels[point],
                     color=COLOR_PALETTE['crystal']['hex'],
                     fontsize=12)

        # Connect the points to form a polygon if there are more than 1 point
        if len(filtered_base_of_support_points['x']) > 1:
            ax.plot(filtered_base_of_support_points['x'] + [filtered_base_of_support_points['x'][0]],
                    filtered_base_of_support_points['y'] + [filtered_base_of_support_points['y'][0]], color='red',
                    zorder=1)

        ### Plot format setup ###

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
        ax.set_title('COM v/s BOS', color=COLOR_PALETTE['crystal']['hex'], fontsize=30)
        ax.set_xlabel('X Position', color=COLOR_PALETTE['crystal']['hex'], fontsize=24)
        ax.set_ylabel('Y Position', color=COLOR_PALETTE['crystal']['hex'], fontsize=24)
        ax.tick_params(axis='both', which='both', labelsize=14, colors=COLOR_PALETTE['dark_terra_cotta']['hex'])

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

        ### Plot image export ###

        # Convert the Matplotlib plot to an OpenCV image.
        fig.canvas.draw()
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(str(frame_info.file_directory) + '/video/'), exist_ok=True)
        # Save the image
        fig.savefig(str(frame_info.file_directory) + '/video/' + 'plot_aux.png', transparent=False)

        # Close the figure
        plt.close(fig)

        ### Image appending ###
        # Read the image component
        img = cv2.imread(str(frame_info.file_directory) + '/video/' + 'plot_aux.png', cv2.IMREAD_UNCHANGED)

        # Resize the component
        component = VISUAL_COMPONENTS['plot_com_bos']
        img_resized = cv2.resize(img,
                                 (int(frame_info.width * component['width_pct']),
                                  int(frame_info.height * component['height_pct'])),
                                 )

        # Get the rgb channel and the alpha mask
        plot_img_resized_rgb = img_resized[:, :, :3]
        plot_img_resized_alpha_mask = (img_resized[:, :, 3] / 255)[:, :, np.newaxis]

        # Get the top left corner of the plot based on the frame dimensions
        plot_top_left_corner = (
            int(frame_info.width * component['topleft_x_pct']), int(frame_info.height * component['topleft_y_pct']))

        # Get the frame subsection
        frame_subsection = image[plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
                           plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]]

        # Create the composite using the alpha mask
        composite = frame_subsection * (
                1 - plot_img_resized_alpha_mask) + plot_img_resized_rgb * plot_img_resized_alpha_mask

        # Append the composite to the frame
        image[plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
        plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]] = composite

        return image


class OverlayPlotFootDeviation:
    def __init__(self, frame_info: FrameInformation):
        self.scene = frame_info.scene

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        ### Data setup ###
        from matplotlib import pyplot as plt
        import cv2
        # Set the frame according to the frame number
        self.scene.frame_set(frame_info.frame_start + frame_info.frame_number)

        # Get Hips and feet vectors
        right_hip_vector = bpy.data.objects['right_hip'].matrix_world.translation - bpy.data.objects[
            'hips_center'].matrix_world.translation
        right_foot_vector = bpy.data.objects['right_foot_index'].matrix_world.translation - bpy.data.objects[
            'right_heel'].matrix_world.translation
        left_hip_vector = bpy.data.objects['left_hip'].matrix_world.translation - bpy.data.objects[
            'hips_center'].matrix_world.translation
        left_foot_vector = bpy.data.objects['left_foot_index'].matrix_world.translation - bpy.data.objects[
            'left_heel'].matrix_world.translation

        # Calculate the angle between the vectors
        right_hip_foot_angle = np.pi / 2 - np.arccos(
            right_foot_vector.dot(right_hip_vector) / (right_hip_vector.magnitude * right_foot_vector.magnitude))
        left_hip_foot_angle = np.pi / 2 - np.arccos(
            left_foot_vector.dot(left_hip_vector) / (left_hip_vector.magnitude * left_foot_vector.magnitude))

        # Define a foot length in cm for demonstration purposes
        foot_length = 30

        # Internal x-axis margin
        x_axis_internal_margin = 7

        # External x-axis margin
        x_axis_external_margin = 10

        # Define the fixed points for the scatter plot representation
        fixed_points = {
            'right_foot_origin': (-(foot_length + x_axis_internal_margin), 0),
            'right_foot_90_degree': (-(foot_length * 2 + x_axis_internal_margin), 0),
            'right_foot_0_degree': (-(foot_length + x_axis_internal_margin), foot_length),
            'right_foot_-90_degree': (-(x_axis_internal_margin), 0),
            'left_foot_origin': (foot_length + x_axis_internal_margin, 0),
            'left_foot_90_degree': (foot_length * 2 + x_axis_internal_margin, 0),
            'left_foot_0_degree': (foot_length + x_axis_internal_margin, foot_length),
            'left_foot_-90_degree': (x_axis_internal_margin, 0),
        }

        # Calculate the foot index using the angles
        right_foot_index_x = -foot_length * np.sin(right_hip_foot_angle)
        right_foot_index_y = foot_length * np.cos(right_hip_foot_angle)
        left_foot_index_x = foot_length * np.sin(left_hip_foot_angle)
        left_foot_index_y = foot_length * np.cos(left_hip_foot_angle)

        ### Plot setup ###
        # Create the plot objects
        fig, ax = plt.subplots(figsize=(6.4, 6.4 * frame_info.height * VISUAL_COMPONENTS['plot_foot_deviation'][
            'height_pct'] / (frame_info.width * VISUAL_COMPONENTS['plot_foot_deviation']['width_pct'])))

        # Plot the fixed points
        for fixed_point in fixed_points:
            ax.scatter(fixed_points[fixed_point][0], fixed_points[fixed_point][1], marker='o',
                       color=COLOR_PALETTE['dark_terra_cotta']['hex'], zorder=2)

        # Add labels
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] - 12, 'RIGHT',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=23, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] - 12, 'LEFT',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=23, ha='center')
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] - 5,
                 str(np.around(np.degrees(right_hip_foot_angle), 1)) + '°', color=COLOR_PALETTE['crystal']['hex'],
                 fontsize=22, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] - 5,
                 str(np.around(np.degrees(left_hip_foot_angle), 1)) + '°', color=COLOR_PALETTE['crystal']['hex'],
                 fontsize=22, ha='center')
        plt.text(fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][1] + 35, '0',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center')
        plt.text(fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][1] + 35, '0',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center')
        plt.text(fixed_points['right_foot_origin'][0] - 35, fixed_points['right_foot_origin'][1], '90',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='right', va='center')
        plt.text(fixed_points['left_foot_origin'][0] + 35, fixed_points['left_foot_origin'][1], '90',
                 color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='left', va='center')
        plt.text(0, 0, '-90', color=COLOR_PALETTE['crystal']['hex'], fontsize=12, ha='center', va='center')

        # Plot the line from foot origin to the foot index
        plt.plot([fixed_points['right_foot_origin'][0], fixed_points['right_foot_origin'][0] + right_foot_index_x],
                 [fixed_points['right_foot_origin'][1], fixed_points['right_foot_origin'][1] + right_foot_index_y],
                 color=COLOR_PALETTE['dark_terra_cotta']['hex'],
                 linewidth=5,
                 zorder=1,
                 )
        plt.plot([fixed_points['left_foot_origin'][0], fixed_points['left_foot_origin'][0] + left_foot_index_x],
                 [fixed_points['left_foot_origin'][1], fixed_points['left_foot_origin'][1] + left_foot_index_y],
                 color=COLOR_PALETTE['dark_terra_cotta']['hex'],
                 linewidth=5,
                 zorder=1,
                 )

        # Plot the foot index
        ax.scatter(fixed_points['right_foot_origin'][0] + right_foot_index_x,
                   fixed_points['right_foot_origin'][1] + right_foot_index_y,
                   marker='o',
                   color=COLOR_PALETTE['crystal']['hex'],
                   zorder=3,
                   s=50,
                   )
        ax.scatter(fixed_points['left_foot_origin'][0] + left_foot_index_x,
                   fixed_points['left_foot_origin'][1] + left_foot_index_y,
                   marker='o',
                   color=COLOR_PALETTE['crystal']['hex'],
                   zorder=3,
                   s=50,
                   )

        ### Plot format setup ###
        # Set plot title
        ax.set_title('Foot Deviation', color=COLOR_PALETTE['crystal']['hex'], fontsize=30)

        # Set the axes limits
        ax.set_xlim(-(foot_length * 2 + x_axis_internal_margin + x_axis_external_margin),
                    foot_length * 2 + x_axis_internal_margin + x_axis_external_margin)
        ax.set_ylim(-20, foot_length + x_axis_internal_margin)

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

        ### Plot image export ###
        # Convert the Matplotlib plot to an OpenCV image.
        fig.canvas.draw()
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(str(frame_info.file_directory) + '/video/'), exist_ok=True)
        # Save the image
        fig.savefig(str(frame_info.file_directory) + '/video/' + 'plot_aux.png', transparent=False, bbox_inches='tight')

        # Close the figure
        plt.close(fig)

        ### Image appending ###
        # Read the image component
        img = cv2.imread(str(frame_info.file_directory) + '/video/' + 'plot_aux.png', cv2.IMREAD_UNCHANGED)

        # Resize the component
        component = VISUAL_COMPONENTS['plot_foot_deviation']
        img_resized = cv2.resize(img,
                                 (int(frame_info.width * component['width_pct']),
                                  int(frame_info.height * component['height_pct'])),
                                 )

        # Get the rgb channel and the alpha mask
        plot_img_resized_rgb = img_resized[:, :, :3]
        plot_img_resized_alpha_mask = (img_resized[:, :, 3] / 255)[:, :, np.newaxis]

        # Get the top left corner of the plot based on the frame dimensions
        plot_top_left_corner = (
            int(frame_info.width * component['topleft_x_pct']), int(frame_info.height * component['topleft_y_pct']))

        # Get the frame subsection
        frame_subsection = image[plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
                           plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]]

        # Create the composite using the alpha mask
        composite = frame_subsection * (
                1 - plot_img_resized_alpha_mask) + plot_img_resized_rgb * plot_img_resized_alpha_mask

        # Append the composite to the frame
        image[plot_top_left_corner[1]:plot_top_left_corner[1] + img_resized.shape[0],
        plot_top_left_corner[0]:plot_top_left_corner[0] + img_resized.shape[1]] = composite

        return image
