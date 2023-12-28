import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(r"C:\Users\andre\source\repos\AIG\l2i.log")
        ]
    )
