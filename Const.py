# coding: utf-8

"""
Const.py - константы игры (по сути, конфиг)
"""

from kivy import platform as _platform

###############################################################################

# Клавиша-модификатор ("shift", "alt", "ctrl")
KEYMOD = 'alt'

# Управление героем.
KEYUP = 273
KEYDOWN = 274
KEYLEFT = 275
KEYRIGHT = 276

###############################################################################

class Colors:
	#COLOR = (R,    G,    B,    A)
	blue   = (0,    0,    1,    1)
	gray   = (0.5,  0.5,  0.5,  1)
	green  = (0,    0.5,  0,    1)
	lime   = (0,    1,    0,    1)
	maroon = (0.5,  0,    0,    1)
	navy   = (0,    0,    0.5,  1)
	purple = (0.5,  0,    0.5,  1)
	red    = (1,    0,    0,    1)
	silver = (0.75, 0.75, 0.75, 1)
	teal   = (0,    0.5,  0.5,  1)

# Ширина игрового поля относительно ширины всего экрана.
AREA_WIDTH = 0.8
# Высота игрового поля относительно высоты всего экрана.
AREA_HEIGHT = 1

if _platform == 'android':
	TILE_WIDTH = 20
	TILE_HEIGHT = 25
	# ширина видимой области
	LOCAL_MAP_WIDTH = 8
	# высота видимой области
	LOCAL_MAP_HEIGHT = 8

	# ширина карты
	MAP_WIDTH = 32 + LOCAL_MAP_WIDTH * 2
	# высота карты
	MAP_HEIGHT = 32 + LOCAL_MAP_HEIGHT * 2
else:
	TILE_WIDTH = 21
	TILE_HEIGHT = 20
	LOCAL_MAP_WIDTH = 8
	LOCAL_MAP_HEIGHT = 8

	MAP_WIDTH = 16 + LOCAL_MAP_WIDTH * 2
	MAP_HEIGHT = 16 + LOCAL_MAP_HEIGHT * 2

# Начало окна вывода видимой части карты (оставлено для совместимости).
WINDOW_LEFT = 0
WINDOW_TOP = 0

###############################################################################

# проходимые тайлы
tileGrass = 1;
tileGround = 2;
tileStairsUp = 3;
tileStairsDown = 4;

# непроходимые тайлы
tileFirstStopTile = 5;
tileTree = tileFirstStopTile;
tileStone = tileFirstStopTile + 1;
tileLast = tileFirstStopTile + 1

###############################################################################

# глубина пещеры
MaxDungeonLevel = 7

###############################################################################

MaxChars = 4
chrSTR = 1 # сила
chrDEX = 2 # ловкость
chrCON = 3 # телосложение
chrIQ  = 4 # ум

MaxSkills = 2
skillHandWeapon = 1 # ближний бой
skillTrapSearch = 2 # обнаружение ловушек

MaxHeroes = 1

###############################################################################

MaxMonsterTypes = 7

###############################################################################
