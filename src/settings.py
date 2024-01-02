import logging
import os
import db
import gui

class OutputPath:
    @staticmethod
    def getOutputPath():
        output_Path = db.DATABASE.fetch_one("SELECT value FROM settings where name = 'output_path';")

        if output_Path is None:
            return OutputPath.getDefaultOutputPath()

        return output_Path[0]

    @staticmethod
    def getDefaultOutputPath():
        # Default output path is the parent directory of the script directory
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
        logging.info(f"Output path updated to {output_Path} in database.")

class SkipEmptyVerses:
    def setSkipEmptyVerses(skipEmptyVerses):
        # First delete the old output path
        db.DATABASE.execute("DELETE FROM settings WHERE name = 'skip_empty_verses';")
        # Then insert the new output path
        db.DATABASE.execute("INSERT INTO settings (name, value) VALUES ('skip_empty_verses', %s);", (skipEmptyVerses,))
        logging.info(f"Skip empty verses updated to {skipEmptyVerses} in database.")

    def getSkipEmptyVerses():
        try:
            skipEmptyVerses = db.DATABASE.fetch_one("SELECT value FROM settings where name = 'skip_empty_verses';")

            if skipEmptyVerses is None:
                return True

            # Parse the result
            skipEmptyVerses = skipEmptyVerses[0]

            skipEmptyVerses = skipEmptyVerses.capitalize()

            if skipEmptyVerses == "True":
                return True
            elif skipEmptyVerses == "False":
                return False
            else:
                raise Exception(f"Invalid value for skip_empty_verses: {skipEmptyVerses}")    
        except Exception as e:
            gui.BasicUI.HandleError(e)    

        return True

def configure_logging():

    logFilePath = os.path.join(OutputPath.getOutputPath(), "log.txt")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logFilePath)
        ]
    )
