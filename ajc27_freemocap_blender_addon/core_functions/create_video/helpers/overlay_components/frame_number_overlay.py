import numpy as np

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.frame_information_dataclass import FrameInformation
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import VISUAL_COMPONENTS


class OverlayFrameNumber:
    def __init__(self, frame_info=None):
        self.position_x_pct = VISUAL_COMPONENTS['frame_number']['position_x_pct']
        self.position_y_pct = VISUAL_COMPONENTS['frame_number']['position_y_pct']

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        import cv2
        # Add frame number / total frame to the frame
        annotated_image = cv2.putText(
            image,
            str(frame_info.frame_number).zfill(frame_info.total_frames_digits) + '/' + str(frame_info.total_frames),
            (int(self.position_x_pct * frame_info.width), int(self.position_y_pct * frame_info.height)),
            VISUAL_COMPONENTS['frame_number']['font'],
            VISUAL_COMPONENTS['frame_number']['fontScale'],
            VISUAL_COMPONENTS['frame_number']['color'],
            VISUAL_COMPONENTS['frame_number']['thickness'],
            VISUAL_COMPONENTS['frame_number']['lineType'],
            )

        return annotated_image
