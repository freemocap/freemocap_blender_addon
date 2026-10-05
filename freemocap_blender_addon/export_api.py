"""Public entry point for an explicitly installed add-on or Extension."""
from pathlib import Path


def export_recording(*, recording_path, blend_file_path, config=None):
    recording = Path(recording_path).expanduser().resolve()
    output = Path(blend_file_path).expanduser().resolve()
    if not recording.is_dir():
        raise ValueError("Recording directory does not exist: {}".format(recording))
    if output.suffix.lower() != ".blend":
        raise ValueError("Output must be a .blend file")
    if not output.parent.is_dir():
        raise ValueError("Output directory does not exist: {}".format(output.parent))
    from .main import ajc27_run_as_main_function
    from .data_models.parameter_models.load_parameters_config import load_default_parameters_config
    ajc27_run_as_main_function(str(recording), str(output),
                              config if config is not None else load_default_parameters_config())
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("Blender export did not produce a nonempty output: {}".format(output))
    return str(output)
