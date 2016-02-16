# coding: utf-8

"""
lowlevel.py - низкоуровневые платформозависимые детали
"""

###############################################################################

# Модули игры.
import Const

# Модули Kivy.
from kivy.clock import Clock
# Перезагружаем конфиг каждую минуту, чтобы можно было редактировать его
# на лету.
Clock.schedule_interval(lambda dt: reload(Const), 60)
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

# Объект приложения(см. функцию `main`).
app = None

###############################################################################

def TileSize():
	"""Вычисляет размеры тайла."""
	x = _Window.width * Const.AREA_WIDTH / Const.MAP_WIDTH
	y = _Window.height * Const.AREA_HEIGHT / Const.MAP_HEIGHT
	return x, y

def PrepareMap():
	"""Подготовка карты. Должна очищать окно."""
	pass

def  VideoInitialize():
	pass

def ShowCell(cell, x, y):
	"""Рисует ячейку (тайл) на карте по переданным координатам."""
	sources = {
		Const.tileGrass        : './resource/img/grass.png',
		Const.tileGround       : './resource/img/ground.png',
		Const.tileStairsUp     : './resource/img/stairs_up.png',
		Const.tileStairsDown   : './resource/img/stairs_down.png',

		Const.tileTree         : './resource/img/tree.png',
		Const.tileStone        : './resource/img/stone.png',
	}
	if not cell.IsVisible:
		# Получаем все виджеты карты, соответствующие тайлам.
		tiles = window.area.children
		# Вычисляем позицию тайла для отрисовки.
		position = window.area.cols * y + x
		# Получаем виджет, соответствующий тайлу.
		tile = tiles[position]
		# Меняем картинку виджета на картинку, соответствующую тайлу.
		tile.source = sources[cell.Tile]

###############################################################################

class TileImage(Image):
	"""
	Изображение, соответствующее ячейке (тайлу) карты.
	"""
	def __init__(self, **kwargs):
		super(TileImage, self).__init__(**kwargs)
		self.source = './resource/img/shadow.png'
		self.size = TileSize()
		self.allow_stretch = True
		self.keep_ratio = False
		self.mipmap = False
		self.texture_size = [1,1]
		self.spacing = 0

class Window(Screen):
	"""
	Основной игровой экран, поделенный на две колонки:
		* левая (большая) - игровая карта;
		* правая (меньшая) - различная информация.
	"""

	def __init__(self, **kwargs):
		self.name = u'main'
		super(Window, self).__init__(**kwargs)
		self.root = root = GridLayout(cols=2)
		self.area = area = GridLayout(
		    cols=Const.MAP_WIDTH, size_hint_x=Const.AREA_WIDTH)
		for y in xrange(Const.MAP_HEIGHT):
			for x in xrange(Const.MAP_WIDTH):
				area.add_widget(TileImage())
		self.infopane = infopane = GridLayout(rows=10, size_hint_x=(1 - Const.AREA_WIDTH))
		infopane.add_widget(Label(text=u"Text"))
		infopane.add_widget(Label(text=u"Text1"))
		infopane.add_widget(Label(text=u"Text2"))
		infopane.add_widget(Label(text=u"Text3"))
		infopane.add_widget(Label(text=u"Text4"))
		infopane.add_widget(Label(text=u"Text5"))
		infopane.add_widget(Label(text=u"Text6"))
		infopane.add_widget(Label(text=u"Text7"))
		infopane.add_widget(Label(text=u"Text8"))
		infopane.add_widget(Label(text=u"Text9"))
		root.add_widget(area)
		root.add_widget(infopane)
		self.hero = hero = Scatter(do_rotation=False, do_scale=False)
		image = Image(source='./resource/img/hero.png',
		              size_hint=(1, 1), size=TileSize())
		hero.add_widget(image)
		self.add_widget(root)

# Основной игровой экран.
window = Window()

class Game(App):
	"""
	Представляет саму программу (приложение).
	"""
	def __init__(self):
		super(Game, self).__init__()
		self.title = u"The Game"

	def build(self):
		root = ScreenManager(transition=FadeTransition())
		root.add_widget(window)
		return root


###############################################################################

def global_keyboard_callback(key, scancode, codepoint, modifiers):
	"""Обработка нажатий клавиш клавиатуры."""
	print('key:', key, 'scancode:', scancode,
	    'codepoint:', repr(codepoint), 'modifiers:', modifiers)
	if key == 275:
		app.current = u"other" if app.current == u"main" else u"main"

_Window.on_keyboard = global_keyboard_callback
#_Window.clearcolor = (200, 0, 0, 1)

###############################################################################

def main():
	global app
	app = Game().build()
	runTouchApp(app)
