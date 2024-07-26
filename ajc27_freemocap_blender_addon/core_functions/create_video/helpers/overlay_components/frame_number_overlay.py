import numpy as np
from freemocap_video_export.create_video.visual_overlays.frame_information_dataclass import FrameInformation
from freemocap_video_export.video_config import visual_components


class VisualComponentFrameNumber:
    def __init__(self, **kwargs):
        self.position_x_pct = visual_components['frame_number']['position_x_pct']
        self.position_y_pct = visual_components['frame_number']['position_y_pct']

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        import cv2
        # Add frame number / total frame to the frame
        annotated_image = cv2.putText(
            image,
            str(frame_info.frame_number).zfill(frame_info.total_frames_digits) + '/' + str(frame_info.total_frames),
            (int(self.position_x_pct * frame_info.width), int(self.position_y_pct * frame_info.height)),
            visual_components['frame_number']['font'],
            visual_components['frame_number']['fontScale'],
            visual_components['frame_number']['color'],
            visual_components['frame_number']['thickness'],
            visual_components['frame_number']['lineType'],
            )

        return annotated_image
