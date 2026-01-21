from pathlib import Path
from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH

EXPORT_PROFILES = {
    'debug': {
        'output_name_sufix': '_debug',
        'resolution_x': 1920,
        'resolution_y': 1080,
        'prerender_cameras': True,
        'render_cameras': {
            'Front': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_x': 0.0, # value between -0.5 and 0.5
                'translate_y': 0.0, # value between -0.5 and 0.5
                'view_margin': 0.1, # margin between camera view and markers view area
            },
        },
        'overlays': {
            "logo": {
                'type': 'image',
                'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                'scale_space': 'RELATIVE',
                'scale_x': 0.2,
                'scale_y': 0.2,
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass",
            "rigid_body_meshes",
            "videos",
            "skelly_mesh",            
        ],
    },
    'showcase': {
        'output_name_sufix': '_showcase',
        'resolution_x': 540,
        'resolution_y': 960,
        'prerender_cameras': True,
        'render_cameras': {
            'Front': {
                'resolution_x': 540,
                'resolution_y': 960,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
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
                'scale_x': 0.1,
                'scale_y': 0.1,
                'translate_x': 0.42,
                'translate_y': 0.42,
            },
        },
        'render_elements': [
            "videos",
            "skelly_mesh",            
        ],
    },
    'scientific': {
        'output_name_sufix': '_scientific',
        'resolution_x': 1920,
        'resolution_y': 1080,
        'prerender_cameras': True,
        'render_cameras': {
            'Front': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
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
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass",
            "rigid_body_meshes",
            "videos",
        ],
    },
    'multiview': {
        'output_name_sufix': '_multiview',
        'resolution_x': 1920,
        'resolution_y': 1080,
        'prerender_cameras': True,
        'render_cameras': {
            'Front': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_x': -0.25,
                'translate_y': 0.25,
                'view_margin': 0.1,
            },
            'Right': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_x': 0.25,
                'translate_y': 0.25,
                'view_margin': 0.1,
            },
            'Top': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_x': -0.25,
                'translate_y': -0.25,
                'view_margin': 0.1,
            },
            'Left': {
                'resolution_x': 960,
                'resolution_y': 540,
                'scale_space': 'RELATIVE',
                'scale_x': 1.0,
                'scale_y': 1.0,
                'translate_x': 0.25,
                'translate_y': -0.25,
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
                'translate_x': 0.45,
                'translate_y': 0.4,
            },
        },
        'render_elements': [
            "center_of_mass",
            "rigid_body_meshes",
        ],
    },
    # Custom profile that is modified before rendering with the UI options
    'custom': {
        'output_name_sufix': '',
        'resolution_x': 1920,
        'resolution_y': 1080,
        'prerender_cameras': True,
        'render_cameras': {},
        'overlays': {},
        'render_elements': [],
    },
}


RENDER_PARAMETERS = {
    'scene.render.engine': 'BLENDER_EEVEE_NEXT',
    'scene.eevee.taa_render_samples': 1,
    'scene.eevee.taa_samples': 1,
    'scene.render.image_settings.file_format': 'FFMPEG',
    'scene.render.ffmpeg.format': 'MPEG4',
    'scene.render.ffmpeg.codec': 'H264',
    'scene.render.ffmpeg.constant_rate_factor': 'LOWEST',
    'scene.render.ffmpeg.ffmpeg_preset': 'REALTIME',
    'scene.render.fps': 30,
    'scene.render.resolution_percentage': 100,
    'scene.eevee.use_gtao': False,
    'scene.render.use_motion_blur': False,
    'scene.eevee.volumetric_samples': 1,
    'scene.eevee.use_volumetric_shadows': False,
    'scene.eevee.use_shadows': False,
    'scene.render.image_settings.color_depth': '8',
    'scene.render.image_settings.color_mode': 'RGB',
    'scene.eevee.use_overscan': False,
    'scene.render.simplify_subdivision': 0,
    'scene.render.simplify_subdivision_render': 0,
    'scene.render.use_simplify': True,
    'scene.render.film_transparent': True,
    'scene.render.compositor_device': 'CPU',
    'scene.render.compositor_precision': 'FULL'

}

RENDER_BACKGROUND = {
    'base_image_path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "video_composite_background.png"),
    'color_modifier': (0.05, 0.05, 0.05, 1.0),
}

LENS_FOVS = {
    '50mm': {
        'horizontal_fov': 39.6,
        'vertical_fov': 22.8965642148994,
    }
}
