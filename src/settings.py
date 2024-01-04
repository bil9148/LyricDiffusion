import logging
import os
# import db

Output_Path = None


class OutputPath:
    @staticmethod
    def getOutputPath():
        global Output_Path
        if Output_Path is None:
            Output_Path = OutputPath.getDefaultOutputPath()
        return Output_Path

    @staticmethod
    def getDefaultOutputPath():
        # Default output path is the parent directory of the script directory
        script_directory = os.path.dirname(os.path.realpath(__file__))
        # Remove '/src/' from the path
        output_path = script_directory.replace("src", "")
        return output_path

    @staticmethod
    def setOutputPath(output_Path):
        global Output_Path
        Output_Path = output_Path
        logging.info(f"Output path updated to {Output_Path}.")

    # @staticmethod
    # def getOutputPath():
    #     output_Path = db.DATABASE.fetch_one(
    #         "SELECT value FROM settings where name = 'output_path';")

    #     if output_Path is None:
    #         return OutputPath.getDefaultOutputPath()

    #     return output_Path[0]

    # @staticmethod
    # def setOutputPath(output_Path):
    #     # First delete the old output path
    #     db.DATABASE.execute("DELETE FROM settings WHERE name = 'output_path';")
    #     # Then insert the new output path
    #     db.DATABASE.execute(
    #         "INSERT INTO settings (name, value) VALUES ('output_path', %s);", (output_Path,))

    #     logging.info(f"Output path updated to {Output_Path} in database.")


SkipVerses = True


class SkipEmptyVerses:
    # @staticmethod
    # def setSkipEmptyVerses(skipEmptyVerses):
    #     # # First delete the old output path
    #     # db.DATABASE.execute(
    #     #     "DELETE FROM settings WHERE name = 'skip_empty_verses';")
    #     # # Then insert the new output path
    #     # db.DATABASE.execute(
    #     #     "INSERT INTO settings (name, value) VALUES ('skip_empty_verses', %s);", (skipEmptyVerses,))
    #     logging.info(
    #         f"Skip empty verses updated to {skipEmptyVerses} in database.")

    # @staticmethod
    # def getSkipEmptyVerses():
    # try:
    #     skipEmptyVerses = db.DATABASE.fetch_one(
    #         "SELECT value FROM settings where name = 'skip_empty_verses';")

    #     if skipEmptyVerses is None:
    #         return True

    #     # Parse the result
    #     skipEmptyVerses = skipEmptyVerses[0]

    #     skipEmptyVerses = skipEmptyVerses.capitalize()

    #     if skipEmptyVerses == "True":
    #         return True
    #     elif skipEmptyVerses == "False":
    #         return False
    #     else:
    #         raise Exception(
    #             f"Invalid value for skip_empty_verses: {skipEmptyVerses}")
    # except Exception as e:
    #     gui.BasicUI.HandleError(e)

    # return True

    @staticmethod
    def setSkipEmptyVerses(skipEmptyVerses):
        global SkipVerses
        SkipVerses = skipEmptyVerses
        logging.info(
            f"Skip empty verses updated to {skipEmptyVerses}.")

    @staticmethod
    def getSkipEmptyVerses():
        global SkipVerses
        return SkipVerses


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
