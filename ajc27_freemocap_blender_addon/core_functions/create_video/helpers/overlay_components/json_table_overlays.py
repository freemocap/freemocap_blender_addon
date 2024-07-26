import json
from typing import Optional, Dict, Any

import cv2
import numpy as np
from freemocap_video_export.create_video.visual_overlays.frame_information_dataclass import FrameInformation
from freemocap_video_export.video_config import visual_components


class VisualComponentStaticJSONTable:
    def __init__(self,
                 frame_info: FrameInformation,
                 data_type: str):
        self.data_type = data_type
        self.position_x_pct = visual_components[self.data_type]['position_x_pct']
        self.position_y_pct = visual_components[self.data_type]['position_y_pct']
        self.frame_info = frame_info
        self.table_lines = []
        self.table_pointer = 0

        self.data: Optional[dict] = None
        self.image: Optional[np.ndarray] = None

        with open(str(frame_info.file_directory) + visual_components[self.data_type]['relative_path']) as json_file:
            self.data = json.load(json_file)

        self.create_table_lines(1, self.data)

    def add_component(self,
                      image: np.ndarray,
                      frame_info: FrameInformation):
        self.image = image
        self.frame_info = frame_info
        self.table_pointer = 0

        for line in self.table_lines:
            self.image = self.put_text(line[0], line[1])

        return self.image

    def create_table_lines(self,
                           json_level: int,
                           data: Dict[str, Any]):

        for key, value in data.items():
            if isinstance(value, dict):
                self.table_lines.append((json_level, ' ' * (json_level - 1) + str(key).replace('_', ' ')))
                self.create_table_lines(json_level + 1, value)
            else:
                # If the value is a float, round it
                if type(value) == float:
                    value = round(value, visual_components['static_json_table']['float_decimal_digits'])

                self.table_lines.append(
                    (json_level, ' ' * (json_level - 1) + str(key).replace('_', ' ') + ' : ' + str(value)))

    def put_text(self,
                 json_level: int,
                 text: str):

        self.table_pointer = self.table_pointer + (
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['fontScale']) * 35

        annotated_image = cv2.putText(
            self.image,
            text,
            (int(self.position_x_pct * self.frame_info.width),
             int(self.position_y_pct * self.frame_info.height + self.table_pointer)),
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['font'],
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['fontScale'],
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['color'],
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['thickness'],
            visual_components[self.data_type]['text_parameters']['level_' + str(json_level)]['lineType'],
        )

        return annotated_image


class VisualComponentRecordingParameters(VisualComponentStaticJSONTable):
    def __init__(self, frame_info: FrameInformation):
        super().__init__(frame_info, 'recording_parameters')


class VisualComponentMediapipeSkeletonSegmentLengths(VisualComponentStaticJSONTable):
    def __init__(self, frame_info: FrameInformation):
        super().__init__(frame_info, 'mediapipe_skeleton_segment_lengths')
