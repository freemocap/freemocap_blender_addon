"""Public entry point for an explicitly installed add-on or Extension."""
from pathlib import Path
from .export_options import CAPABILITIES, parquet_options


def export_recording(*, recording_path, blend_file_path, config=None, route='legacy_npy',
                     trajectory_channel='LANDMARKS_3D', run_id=None, sensor_group=None):
    recording = Path(recording_path).expanduser().resolve()
    output = Path(blend_file_path).expanduser().resolve()
    if not recording.is_dir() and not (recording.is_file() and recording.suffix.lower() == '.parquet'):
        raise ValueError("Recording directory does not exist: {}".format(recording))
    if output.suffix.lower() != ".blend":
        raise ValueError("Output must be a .blend file")
    if not output.parent.is_dir():
        raise ValueError("Output directory does not exist: {}".format(output.parent))
    if route == 'legacy_npy':
        if not recording.is_dir():
            raise ValueError('Legacy NPY loading requires a recording folder')
        from .main import ajc27_run_as_main_function
        from .data_models.parameter_models.load_parameters_config import load_default_parameters_config
        if isinstance(config, dict):
            from .data_models.parameter_models.load_parameters_config import load_parameters_config_from_dict
            config = load_parameters_config_from_dict(config)
        ajc27_run_as_main_function(str(recording), str(output),
                                  config if config is not None else load_default_parameters_config())
    elif route in ('parquet_segments', 'parquet_constraints'):
        options = parquet_options(route, {} if config is None else config)
        import bpy
        from .core_functions.parquet_import import load_parquet
        result = load_parquet(recording, route=route, rest_pose=options["rest_pose"], trajectory_channel=trajectory_channel,
                     run_id=run_id, sensor_group=sensor_group)
        from .core_functions.animation_cleanup import apply_cleanup
        apply_cleanup(result['root'], foot_locking=options['foot_locking'], hand_limits=options['hand_limits'])
        if options['formats']:
            from .core_functions.export_3d_model.export_3d_model import export_3d_model
            export_3d_model(result['root'], result['rig'], formats=options['formats'],
                            destination_folder=str(output.parent), add_subfolder=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output))
    else:
        raise ValueError('Unknown import route: ' + route)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("Blender export did not produce a nonempty output: {}".format(output))
    return str(output)
