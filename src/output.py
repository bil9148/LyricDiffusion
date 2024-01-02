import logging
import os


def get_output_path():
    # Constant output path
    script_directory = os.path.dirname(os.path.realpath(__file__))
    # Remove '/src/' from the path
    output_path = script_directory.replace("src", "")
    return output_path


OUTPUT_PATH = get_output_path()

def configure_logging():

    logFilePath = os.path.join(OUTPUT_PATH, "log.txt")

    open(logFilePath, "w")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logFilePath)
        ]
    )
