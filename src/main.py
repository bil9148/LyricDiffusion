from output import configure_logging
from lyrics2Images import run


if __name__ == "__main__":
    configure_logging()
    run("Gangstas Paradise", "Coolio",
        "stabilityai/stable-diffusion-2-1", 50)
