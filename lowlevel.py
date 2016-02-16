# coding: utf-8

"""
lowlevel.py - низкоуровневые платформозависимые детали
"""

###############################################################################

import os

import const

from kivy.clock import Clock
# Перезагружаем конфиг каждую минуту, чтобы можно было редактировать его
# на лету.
Clock.schedule_interval(lambda: reload(const), 60)
from kivy.metrics import sp
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import (WipeTransition, FadeTransition,
                                    NoTransition, FallOutTransition,
                                    SwapTransition, SlideTransition,
                                    RiseInTransition)
from kivy.properties import (NumericProperty, BooleanProperty, AliasProperty,
                            ObjectProperty, ListProperty,
                            ReferenceListProperty, OptionProperty)
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.base import runTouchApp
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window as _Window

###############################################################################

def TileSize():
	x = _Window.width * const.AREA_WIDTH / const.MAP_WIDTH
    y = _Window.height * const.AREA_HEIGHT / const.MAP_HEIGHT
	return x, y

def PrepareMap():
	"""Подготовка карты. Должна очищать окно."""
	os.system('clear')

def  VideoInitialize():
	os.system('clear')

def ShowCell(cell, x, y):
	tiles = {
		"tileGrass"        : './resource/img/grass.png',
		"tileGround"       : './resource/img/ground.png',
		"tileStairsUp"     : './resource/img/stairs_up.png',
		"tileStairsDown"   : './resource/img/stairs_down.png',

		"tileTree"         : './resource/img/tree.png',
		"tileStone"        : './resource/img/stone.png',
	}
    app.to.area.add_widget(Image(source=tiles[cell.Tile]))

class Window(Screen):
	"""
	"""

	def __init__(self, **kwargs):
		super(Window, self).__init__(**kwargs)
		self.name = u'Area'
		self.root = root = GridLayout(cols=2, rows=1)
		self.area = area = GridLayout(
		    cols=const.MAP_WIDTH, rows=const.MAP_HEIGHT, size_hint_x=0.7)
		self.infopane = infopane = GridLayout(cols=1, rows=10, size_hint_x=0.3)
		self.hero = hero = Scatter(do_rotation=False, do_scale=False)
		image = Image(source='./resource/img/hero.png',
		size_hint=(1, 1), size=TileSize())
		hero.add_widget(image)

class Game(App):
	"""
	"""
	def __init__(self):
		super(Game, self).__init__()

	def build(self):
		root = ScreenManager(transition=FadeTransition())
		root.to = to = Window()
		root.add_widget(to)
		return root


###############################################################################

def global_keyboard_callback(key, scancode, codepoint, modifiers):
	print('key:', key, 'scancode:', scancode,
	    'codepoint:', repr(codepoint), 'modifiers:', modifiers)

_Window.on_keyboard = global_keyboard_callback

###############################################################################

def main():
	app = Game().build()
	runTouchApp(app)
