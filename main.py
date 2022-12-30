"""
imports:
plyer
kivy
- python -m pip install kivy --pre --no-deps --index-url  https://kivy.org/downloads/simple/
- python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/
kivy-garden
"""

import plyer

import gui

gui = gui.PyCalendarApp()

print("finished init")

if __name__ == "__main__":
    gui.run()
