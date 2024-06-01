from pathlib import Path


def get_path_to_test_data() -> str:
    test_data_path = Path().home() / "freemocap_data" / "recording_sessions" / "freemocap_test_data"
    test_data_path = test_data_path.resolve()
    if not test_data_path.exists():
        print(
            "Sample data not found. To download sample data, in the main FreeMoCap Gui:"
            " `File Menu`>>'Download Sample Data',"
            " then press the `Process Recording Folder` button in the `Process Data` tab")
        raise Exception(f"Could not find sample data at {test_data_path}")

    output_data_path = test_data_path / "output_data"
    if not output_data_path.exists():
        print(
            f"Sample data found at `{test_data_path}, but has not been processed yet. "
            f"To process sample data, go to the main FreeMoCap Gui, "
            f"select the sample data folder and click the 'Process Videos' button or whatever its called lol")
        raise Exception(f"Could not find processed sample data at {output_data_path}")

    return str(test_data_path)


if __name__ == "__main__":
    test_data_path = get_path_to_test_data()
    print(f"Sample data downloaded found at: {str(test_data_path)}")
