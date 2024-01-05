import settings as settings
import gui
# import db


def run():
    # db.DATABASE.setupAppDatabase()
    settings.Logger.configure_logging()
    gui.showGUI()


if __name__ == "__main__":
    run()
