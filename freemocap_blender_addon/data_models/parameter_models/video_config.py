try:
    import cv2
except Exception as e:
    pass
export_profiles = {
    'debug': {
        'resolution_x': 1920,
        'resolution_y': 1080,
        'bitrate': 2000000,
        'visual_components': [
            "frame_number",
            "logo",
            "recording_parameters",
            "mediapipe_skeleton_segment_lengths",
        ],
    },
    'showcase': {
        'resolution_x': 1080,
        'resolution_y': 1920,
        'bitrate': 5000000,
        'visual_components': [
            "logo",
        ],
        'background_path': '/assets/charuco_board.png',
    },
    'scientific': {
        'resolution_x': 1920,
        'resolution_y': 1080,
        'bitrate': 3000000,
        'visual_components': [
            "frame_number",
            "logo",
            "recording_parameters",
            "mediapipe_skeleton_segment_lengths",
            "plot_com_bos",
        ],
    },
}

render_parameters = {
    'scene.render.engine': 'BLENDER_EEVEE',
    'scene.eevee.taa_render_samples': 1,
    'scene.render.image_settings.file_format': 'FFMPEG',
    'scene.render.ffmpeg.format': 'MPEG4',
    'scene.render.ffmpeg.codec': 'H264',
    'scene.render.ffmpeg.constant_rate_factor': 'LOWEST',
    'scene.render.ffmpeg.ffmpeg_preset': 'REALTIME',
    'scene.render.fps': 30,
    'scene.render.resolution_percentage': 100,
    'scene.eevee.use_gtao': False,
    'scene.eevee.use_bloom': False,
    'scene.eevee.use_ssr': False,
    'scene.eevee.use_motion_blur': False,
    'scene.eevee.volumetric_samples': 4,
    'scene.eevee.use_volumetric_lights': False,
    'scene.eevee.use_soft_shadows': True,
}

render_background = {
    'height': 10,
    'y_axis_offset': 0.1,
}

lens_FOVs = {
    '50mm': {
        'horizontal_fov': 39.6,
        'vertical_fov': 22.8965642148994,
    }
}

color_palette = {
    'crystal': {
        'rgb': (164, 214, 217),
        'bgr': (217, 214, 164),
        'hex': '#A4D6D9',
    },
    'dark_terra_cotta': {
        'rgb': (217, 81, 87),
        'bgr': (87, 81, 217),
        'hex': '#D95157',
    },
    'police_blue': {
        'rgb': (54, 93, 95),
        'bgr': (95, 93, 54),
        'hex': '#365D5F',
    },
    'japanese_indigo': {
        'rgb': (37, 67, 66),
        'bgr': (66, 67, 37),
        'hex': '#254342',
    },
    'glossy_gold': {
        'rgb': (250, 228, 129),
        'bgr': (129, 228, 250),
        'hex': '#FAE481',
    },

}

visual_components = {
    'frame_number': {
        'position_x_pct': 0.02,
        'position_y_pct': 0.05,
        'font': cv2.FONT_HERSHEY_SIMPLEX,
        'fontScale': 1,
        'color': color_palette['crystal']['bgr'],
        'thickness': 2,
        'lineType': cv2.LINE_AA,
    },
    'logo': {
        'relative_path': '/assets/freemocap_logo.png',
        'resize_largest_side_pct': 0.1,
        'position_x_pct': 0.9,
        'position_y_pct': 0.02,
    },
    'static_json_table': {
        'float_decimal_digits': 2,
    },
    'recording_parameters': {
        'relative_path': '/output_data/recording_parameters.json',
        'position_x_pct': 0.79,
        'position_y_pct': 0.6,
        'text_parameters': {
            'level_1': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.6,
                'color': color_palette['dark_terra_cotta']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
            'level_2': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.55,
                'color': color_palette['crystal']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
            'level_3': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.5,
                'color': color_palette['glossy_gold']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
        },
    },
    'mediapipe_skeleton_segment_lengths': {
        'relative_path': '/output_data/mediapipe_skeleton_segment_lengths.json',
        'position_x_pct': 0.02,
        'position_y_pct': 0.07,
        'text_parameters': {
            'level_1': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.4,
                'color': color_palette['dark_terra_cotta']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
            'level_2': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.35,
                'color': color_palette['crystal']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
            'level_3': {
                'font': cv2.FONT_HERSHEY_SIMPLEX,
                'fontScale': 0.3,
                'color': color_palette['glossy_gold']['bgr'],
                'thickness': 1,
                'lineType': cv2.LINE_AA,
            },
        },
    },
    'plot_com_bos': {
        'topleft_x_pct': 0.75,
        'topleft_y_pct': 0.7,
        'width_pct': 0.23,
        'height_pct': 0.25,
        'ground_contact_threshold': 0.05,
    },
    'plot_foot_deviation': {
        'topleft_x_pct': 0.75,
        'topleft_y_pct': 0.4,
        'width_pct': 0.23,
        'height_pct': 0.25,
    }
}
