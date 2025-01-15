import sys
from pathlib import Path

from ajc27_freemocap_blender_addon.core_functions.setup_scene.clear_scene import clear_scene
from ajc27_freemocap_blender_addon.data_models.parameter_models.load_parameters_config import \
    load_default_parameters_config
from ajc27_freemocap_blender_addon.data_models.parameter_models.parameter_models import Config


def ajc27_run_as_main_function(recording_path: str,
                               blend_file_path: str,
                               config: Config = load_default_parameters_config()):
    from ajc27_freemocap_blender_addon.core_functions.main_controller import MainController

    controller = MainController(recording_path=recording_path,
                                blend_file_path=blend_file_path,
                                config=config)

    clear_scene()

    controller.load_data()

    print("Done!!!")


if __name__ == "__main__" or __name__ == "<run_path>":
    print("LoadING FREEMOCAP BLENDER ADDON...")
    try:
        argv = sys.argv
        print(f"Received command line arguments: {argv}")
        argv = argv[argv.index("--") + 1:]
        recording_path_input = Path(argv[0])
        blender_file_save_path_input = Path(argv[1])


        if not recording_path_input:
            if __name__ == "<run_path>":
                print("No recording path specified!")
                raise ValueError("No recording path specified")
            elif (Path().home() / "freemocap_data/recording_sessions/freemocap_sample_data").exists():
                recording_path_input = Path().home() / "freemocap_data/recording_sessions/freemocap_sample_data"
            else:
                raise ValueError("No recording path specified")

        if not Path(recording_path_input).exists():
            print(f"Recording path {recording_path_input} does not exist!")
            raise ValueError(f"Recording path {recording_path_input} does not exist!")

        if not blender_file_save_path_input:
            blender_file_save_path_input = recording_path_input / (recording_path_input.stem + ".blend")

        print(f"Running {__file__} with recording_path={recording_path_input}")
        ajc27_run_as_main_function(recording_path=str(recording_path_input),
                                   blend_file_path=str(blender_file_save_path_input))
    except Exception as e:
        print(f"ERROR RUNNING {__file__}: \n\n GOT ERROR \n\n {str(e)}")

