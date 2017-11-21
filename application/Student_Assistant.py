#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 23:11:38 2017

@author: allo0o2a
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty



Window.size = (600, 1000)
Window.clearcolor = (1, 1, 1, 1)



class HomeScreen(Screen):
	pass
class StudyPlanScreen(Screen):
	pass
class CoursesScreen(Screen):
	pass
class ProfessorsScreen(Screen):
	pass
class BuildingsScreen(Screen):
    pass
class Student_AssistantApp(App):
    def build(self):
        self.title = 'Student Assistant Application'
    pass

if __name__ == '__main__':
    Student_AssistantApp().run()