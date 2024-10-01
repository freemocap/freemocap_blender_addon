import os

import cv2
import numpy as np
from freemocap_video_export.create_video.visual_overlays.frame_information_dataclass import FrameInformation
from freemocap_video_export.video_config import visual_components


class VisualComponentImage:
    def __init__(self,
                 frame_info: FrameInformation,
                 image_type: str):
        # Get the raw image
        try:
            self.image_raw = cv2.imread(
                os.path.dirname(os.path.realpath(__file__)) + visual_components[image_type]['relative_path'],
                cv2.IMREAD_UNCHANGED)
        except:
            print('Image not found: ' + os.path.dirname(os.path.realpath(__file__)) + visual_components[image_type][
                'relative_path'])

        # Get the larger side of the image to use it as reference
        larger_side = frame_info.width if frame_info.width > frame_info.height else frame_info.height

        # Set the image properties
        self.image_width = int(larger_side * visual_components[image_type]['resize_largest_side_pct'])
        self.image_height = int(self.image_raw.shape[0] * self.image_width / self.image_raw.shape[1])
        # Resize the image
        self.image = cv2.resize(self.image_raw, (int(self.image_width), int(self.image_height)))

        # Get the rgb image and alpha mask
        self.image_rgb = self.image[:, :, :3]
        self.image_alpha_mask = (self.image[:, :, 3] / 255)[:, :, np.newaxis]

        # Get the x and y positions of the image
        image_position_x = int(frame_info.width * visual_components[image_type]['position_x_pct'])
        image_position_y = int(frame_info.height * visual_components[image_type]['position_y_pct'])

        # Adjust the position in case they get out of frame
        if image_position_x + self.image_width > frame_info.width:
            image_position_x = frame_info.width - self.image_width
        if image_position_y + self.image_height > frame_info.height:
            image_position_y = frame_info.height - self.image_height

        # Set the image position
        self.image_position = (image_position_x, image_position_y)

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        # Get the frame subsection
        frame_subsection = image[self.image_position[1]:self.image_position[1] + self.image_height,
                           self.image_position[0]:self.image_position[0] + self.image_width]

        # Create the composite using the alpha mask
        composite = frame_subsection * (1 - self.image_alpha_mask) + self.image_rgb * self.image_alpha_mask

        # Append the composite to the frame
        image[self.image_position[1]:self.image_position[1] + self.image_height,
        self.image_position[0]:self.image_position[0] + self.image_width] = composite

        return image


class VisualComponentLogo(VisualComponentImage):
    def __init__(self, frame_info: FrameInformation):
        super().__init__(frame_info, 'logo')
