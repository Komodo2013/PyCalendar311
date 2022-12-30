import re

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.utils import get_color_from_hex

import threading
import time

import kivy
from kivy.factory import Factory
import kivy_garden.contextmenu
from kivy.uix.gridlayout import GridLayout

from kivy.core.text import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView

from crypto import is_valid_pass, AuthToken
from data import my_db


class CreateAccountWindow(Screen):
    message = StringProperty(defaultvalue="")

    box_color = get_color_from_hex("#0ab26c")

    def create(self):
        token = AuthToken(self.ids.user_input.text or " ", self.ids.pass_input_1.text or " ")
        if my_db.user_exists(token.user_id):
            self.message = "User already taken"
        elif not is_valid_pass(self.ids.pass_input_1.text) or \
                self.ids.pass_input_1.text is not self.ids.pass_input_2.text:
            self.message = "Invalid password"
        else:
            my_db.add_user(token)
            self.manager.current = "login"

    def validate(self):
        self.message = is_valid_pass(self.ids.pass_input_1.text)[1]

    def validate_confirm(self):
        if not self.ids.pass_input_1.text == self.ids.pass_input_2.text:
            self.message = "Passwords must Match!"
        else:
            self.message = ""


class LoginWindow(Screen):
    box_color = get_color_from_hex("#0ab26c")

    def __init__(self, **kw):
        super().__init__(**kw)

    def login(self):
        token = AuthToken(self.ids.user_input.text or " ", self.ids.pass_input.text or " ")
        print(token.get_key())
        self.manager.current = "loading"

        todoist_api_key = "c0c9886ed9370c334b7df1329ffd02024d1d2b01"
        canvas_api_key = "2974~Ymjt5hMUEQ5Lay30hzwKSc3o4UPnY6vjhFgz3RSRUAPiMtEWacW6wAIqYV81FX6Y"
        google_api = "AIzaSyDav-7cHMWNDrBDGKYsR0dBdqU3V2WzWJA"
        canvas_header = {"Authorization": "Bearer " + canvas_api_key}

    def new_account(self):
        self.manager.current = "create"


class LoadingWindow(Screen):
    box_color = get_color_from_hex("#0c6021")

    def animate(self, i, **kwargs):
        pb = self.ids.progress_bar
        pb.value += 5
        if pb.value >= pb.max:
            self.manager.current = "pycalendar"

    def on_enter(self):
        print("running")
        Clock.schedule_interval(self.animate, 0.05)


class PyCalendarWindow(Screen):
    def _settings(self, val):
        if val == 0:
            print("Settings....")
        elif val == 1:
            print("Changing Todoist Key....")
        elif val == 2:
            print("Changing Canvas Key....")
        elif val == 3:
            print("Changing Google Calendar Key....")
        else:
            raise Exception("Invalid menu choice")
        self.ids['app_menu'].close_all()

    def _sync(self, val):
        if val == 0:
            print("Syncing all data....")
        elif val == 1:
            print("Syncing Todoist....")
        elif val == 2:
            print("Syncing Canvas....")
        elif val == 3:
            print("Syncing Calendar....")
        else:
            raise Exception("Invalid menu choice")
        self.ids['app_menu'].close_all()

    def _todoist(self, val):
        if val == 0:
            print("Todoist Today....")
        elif val == 1:
            print("Todoist Weekly Overview....")
        elif val == 2:
            print("Todoist by Class....")
        else:
            raise Exception("Invalid menu choice")
        self.ids['app_menu'].close_all()

    def _canvas(self, val):
        if val == 0:
            print("Canvas Class Summary....")
        elif val == 1:
            print("Canvas Class Details....")
        elif val == 2:
            print("Canvas Grades....")
        elif val == 3:
            print("Canvas Minimum work....")
        elif val == 4:
            print("Canvas Assignments....")
        else:
            raise Exception("Invalid menu choice")
        self.ids['app_menu'].close_all()

    def _calendar(self, val):
        if val == 0:
            print("calendar Today....")
        elif val == 1:
            print("calendar Weekly....")
        else:
            raise Exception("Invalid menu choice")
        self.ids['app_menu'].close_all()

    def _get_main(self):
        return self.ids['main_panel']

    def get_mini_1(self):
        return self.ids['mini_panel_1']

    def get_mini_2(self):
        return self.ids['mini_panel_2']


class WindowManager(ScreenManager):
    pass


class PyCalendarApp(App):

    def build(self):
        return kv

    def get_main(self):
        return PyCalendarWindow.get_main()

    def get_mini_1(self):
        return PyCalendarWindow.get_mini_1()

    def get_mini_2(self):
        return PyCalendarWindow.get_mini_2()


kv = Builder.load_file("gui/PyCalendar.kv")
