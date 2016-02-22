# coding: utf-8

"""
Lowlevel.py - низкоуровневые платформозависимые детали
"""

###############################################################################

# Python модули.
import sys
import random

# Модули игры.
import Const
import Texts
import Game
import Hero

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

def ChangeTileSource(x, y, source):
	# Получаем все виджеты карты, соответствующие тайлам.
	tiles = window.area.children
	# Вычисляем позицию тайла для отрисовки.
	position = window.area.cols * y + x
	# Получаем виджет, соответствующий тайлу.
	tile = tiles[position]
	# Меняем картинку виджета на картинку, соответствующую тайлу.
	tile.source = source

def ChangeTileSourceWithSavingPrevious(x, y, source):
	"""
	Служит для реализации перемещения героя: на тайле поверхности, где находит-
	ся герой, рисуется его картинка, при этом изначальное изображение тайла со-
	храняется в специальном слоте-стеке. На одном тайле одновременно могут на-
	ходиться до трех сущностей (например, герой-артефакт-поверхность), поэтому
	просто переменная-слот не подходит, нужен массив.
	"""
	# Получаем все виджеты карты, соответствующие тайлам.
	tiles = window.area.children
	# Вычисляем позицию тайла для отрисовки.
	position = window.area.cols * y + x
	# Получаем виджет, соответствующий тайлу.
	tile = tiles[position]
	# Сохраняем предыдущую картинку,
	# добавляя её в стек предыдущих картинок тайла.
	tile.on.append(tile.source)
	# Меняем картинку виджета на картинку, соответствующую тайлу.
	tile.source = source

def CleaningUp(x, y):
	"""Подчищает тайл при перемещении героя и монстров, возвращая предыдущую
	  картинку тайла."""
	tiles = window.area.children
	position = window.area.cols * y + x
	tile = tiles[position]
	tile.source = tile.on.pop()

def TileSize():
	"""Вычисляет размеры тайла."""
	x = _Window.width * Const.AREA_WIDTH / Const.MAP_WIDTH
	y = _Window.height * Const.AREA_HEIGHT / Const.MAP_HEIGHT
	return x, y

def PrepareMap():
	"""Подготовка карты. Должна очищать окно."""
	pass

def  VideoInitialize():
	"""Оставлено для совместимости."""
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
	if cell.IsVisible:
		ChangeTileSource(x, y, sources[cell.Tile])

def ShowMonster(mns):
	"""Отображает монстра на экране."""
	sources = {
	    Texts.STR_MONSTER1: './resource/img/monster1.png',
	    Texts.STR_MONSTER2: './resource/img/monster2.png',
	    Texts.STR_MONSTER3: './resource/img/monster3.png',
	    Texts.STR_MONSTER4: './resource/img/monster4.png',
	    Texts.STR_MONSTER5: './resource/img/monster4.png',
	    Texts.STR_MONSTER6: './resource/img/monster4.png',
	    Texts.STR_MONSTER7: './resource/img/monster4.png',
	}
	x, y = (Const.WINDOW_LEFT + mns.x,
	        Const.WINDOW_TOP + mns.y)
	ChangeTileSourceWithSavingPrevious(x, y, sources[mns.Name])

def ShowHeroInfo(HeroNum):
	hero = Hero.Heroes[HeroNum]
	window.infopane.children[0].text = u''.join((str(Texts.STR_HERO_HP),
	                                         str(hero.HP),
	                                         ' / ',
	                                         str(hero.MaxHP),
	                                         '\n',
	                                         Texts.STR_HERO_XY,
	                                         str(hero.x),
	                                         ' , ',
	                                         str(hero.y)))

def DeathHero():
	def _():
		return './resource/img/%s.png' % ['black', 'red'][random.randint(0, 1)]
	tiles = window.area.children
	for t in tiles:
		t.source = _()
	else:
		_Window.update_viewport()
	Clock.schedule_once(sys.exit, 5)

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
		self.texture_size = 1, 1
		self.spacing = 0
		self.on = []

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
		root.add_widget(area)
		root.add_widget(infopane)
		self.add_widget(root)

# Основной игровой экран.
window = Window()

class GameApp(App):
	"""
	Представляет саму программу (приложение).
	"""
	def __init__(self):
		super(GameApp, self).__init__()
		self.title = u"The Game"

	def build(self):
		root = ScreenManager(transition=FadeTransition())
		root.add_widget(window)
		return root


###############################################################################

def global_keyboard_callback(key, scancode, codepoint, modifiers):
	"""Обработка нажатий клавиш клавиатуры."""
	#print('key:', key, 'scancode:', scancode,
	#    'codepoint:', repr(codepoint), 'modifiers:', modifiers)
	if not modifiers:
		if key == 273:
			Game.MoveHero(0, 1)
		elif key == 274:
			Game.MoveHero(0, -1)
		elif key == 275:
			Game.MoveHero(-1, 0)
		elif key == 276:
			Game.MoveHero(1, 0)
	elif modifiers == ['alt']:
		# Alt+d[eath]
		if key == 100:
			DeathHero()

_Window.on_keyboard = global_keyboard_callback
#_Window.clearcolor = (200, 0, 0, 1)

###############################################################################

def main():
	global app
	app = GameApp().build()
	runTouchApp(app)
