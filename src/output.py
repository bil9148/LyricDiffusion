import logging
import os
import db

class OutputPath:
    @staticmethod
    def getOutputPath():
        output_Path = db.DATABASE.fetch_one("SELECT value FROM settings where name = 'output_path';")

        if output_Path is None:
            print("Output path not found in database. Using default output path.")
            return OutputPath.getDefaultOutputPath()

        print("Output path found in database.")

        return output_Path[0]

    @staticmethod
    def getDefaultOutputPath():
        # Constant output path
        script_directory = os.path.dirname(os.path.realpath(__file__))
        # Remove '/src/' from the path
        output_path = script_directory.replace("src", "")
        return output_path
    
    @staticmethod
    def setOutputPath(output_Path):
        # First delete the old output path
        db.DATABASE.execute("DELETE FROM settings WHERE name = 'output_path';")
        # Then insert the new output path
        db.DATABASE.execute("INSERT INTO settings (name, value) VALUES ('output_path', %s);", (output_Path,))
        print(f"Output path updated to {output_Path} in database.")


def configure_logging():

    logFilePath = os.path.join(OutputPath.getOutputPath(), "log.txt")

    print("Log file path:", logFilePath)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logFilePath)
        ]
    )
