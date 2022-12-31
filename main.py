"""
imports:
plyer
kivy
- python -m pip install kivy --pre --no-deps --index-url  https://kivy.org/downloads/simple/
- python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/
kivy-garden
"""

import logging
import datetime
from kivy.logger import Logger

timestamp = datetime.datetime.now().strftime("%y_%j_%H-%M-S")

l = open(f"logs/{timestamp}_log.log", "w+")
l.close()

logging.basicConfig(filename=f"logs/{timestamp}_log.log",
                    format="[%(name)-5s] [%(levelname)-8s] :: %(asctime)s - %(message)s",
                    filemode="a",
                    datefmt="%D",
                    level=logging.INFO)

handle = logging.FileHandler(f"logs/{timestamp}_log.log", encoding="utf-8")
handle.set_name("Logger")
handle.setLevel(logging.INFO)
handle.setFormatter(logging.Formatter("[%(levelname)-8s] [%(name)-5s] :: %(asctime)s - %(message)s"))
Logger.addHandler(handle)

import plyer

import gui

logging.info("Starting PyCalendar")

gui = gui.PyCalendarApp()

logging.info("Finished Initialization")


if __name__ == "__main__":
    gui.run()
