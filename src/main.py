import output
import gui
import db

def run():
    db.database.setupAppDatabase()
    output.configure_logging()
    gui.showGUI()

if __name__ == "__main__":
    run()