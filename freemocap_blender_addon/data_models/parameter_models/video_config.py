from pathlib import Path
from freemocap_blender_addon import PACKAGE_ROOT_PATH

EXPORT_PROFILES = {
    'default': {
        'resolution_x': 1920,
        'resolution_y': 1080,
        'render_cameras': {
            'Front': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': 0.0, # value between -1 and 1
                'translate_y': 0.0, # value between -1 and 1
                'view_margin': 0.1, # margin between camera view and markers view area
            },
            # 'Right': {
            #     'resolution_x': 720,
            #     'resolution_y': 1280,
            #     'scale_space': 'RELATIVE',
            #     'scale_x': 0.3,
            #     'scale_y': 0.3,
            #     'translate_relative': True,
            #     'translate_x': 0.4,
            #     'translate_y': -0.3,
            #     'view_margin': 0.0,
            # },
            # 'Left': {
            #     'resolution_x': 720,
            #     'resolution_y': 1280,
            #     'scale_space': 'RELATIVE',
            #     'scale_x': 0.3,
            #     'scale_y': 0.3,
            #     'translate_relative': True,
            #     'translate_x': -0.4,
            #     'translate_y': -0.3,
            #     'view_margin': 0.0,
            # },
            # 'Back': {
            #     'resolution_x': 720,
            #     'resolution_y': 1280,
            #     'scale_space': 'RELATIVE',
            #     'scale_x': 0.5,
            #     'scale_y': 0.5,
            #     'translate_relative': True,
            #     'translate_x': 0.0,
            #     'translate_y': -0.2,
            #     'view_margin': 0.0,
            # },
            # 'Top': {
            #     'resolution_x': 1920,
            #     'resolution_y': 1080,
            #     'scale_space': 'RELATIVE',
            #     'scale_x': 0.2,
            #     'scale_y': 0.2,
            #     'translate_relative': True,
            #     'translate_x': -0.35,
            #     'translate_y': 0.1,
            #     'view_margin': 0.0,
            # },
        },
        'overlays': {
            "logo": {
                'type': 'image',
                'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_relative': True,
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass_data",
            "rigid_body_meshes",
            "videos",
            "skelly_mesh",
            "ground_plane"
        ],
    },
    'showcase': {
        'resolution_x': 1080,
        'resolution_y': 1920,
        'render_cameras': {
            'Front': {
                'resolution_x': 1080,
                'resolution_y': 1920,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': 0.0,
                'translate_y': 0.0,
                'view_margin': 0.1,
            },
        },
        'overlays': {
            "logo": {
                'type': 'image',
                'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_relative': True,
                'translate_x': 0.4,
                'translate_y': 0.43,
            },
        },
        'render_elements': [
            "videos",
            "skelly_mesh",            
        ],
    },
    'scientific': {
        'resolution_x': 1920,
        'resolution_y': 1080,
        'render_cameras': {
            'Front': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': 0.0,
                'translate_y': 0.0,
                'view_margin': 0.1,
            },
            'Right': {
                'resolution_x': 720,
                'resolution_y': 1280,
                'scale_space': 'RELATIVE',
                'scale_x': 0.3,
                'scale_y': 0.3,
                'translate_relative': True,
                'translate_x': 0.4,
                'translate_y': -0.3,
                'view_margin': 0.0,
            },
            'Top': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_relative': True,
                'translate_x': -0.35,
                'translate_y': -0.3,
                'view_margin': 0.0,
            },
        },
        'overlays': {
            "logo": {
                'type': 'image',
                'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_relative': True,
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass_data",
            "rigid_body_meshes",
            "videos",
        ],
    },
    'multiview': {
        'resolution_x': 1920,
        'resolution_y': 1080,
        'render_cameras': {
            'Front': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': -0.25,
                'translate_y': 0.25,
                'view_margin': 0.05,
            },
            'Right': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': 0.25,
                'translate_y': 0.25,
                'view_margin': 0.05,
            },
            'Top': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': -0.25,
                'translate_y': -0.25,
                'view_margin': 0.05,
            },
            'Left': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_relative': True,
                'translate_x': 0.25,
                'translate_y': -0.25,
                'view_margin': 0.05,
            },
        },
        'overlays': {
            "logo": {
                'type': 'image',
                'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_relative': True,
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass_data",
            "rigid_body_meshes",
        ],
    },
}

RENDER_PARAMETERS = {
    'scene.render.engine': 'BLENDER_EEVEE',
    'scene.eevee.taa_render_samples': 1,
    'scene.render.image_settings.file_format': 'FFMPEG',
    'scene.render.ffmpeg.format': 'MPEG4',
    'scene.render.ffmpeg.codec': 'H264',
    'scene.render.ffmpeg.constant_rate_factor': 'VERYLOW',
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

RENDER_BACKGROUND = {
    'height': 10,
    'y_axis_offset': 0.1,
}

LENS_FOVS = {
    '50mm': {
        'horizontal_fov': 39.6,
        'vertical_fov': 22.8965642148994,
    }
}
