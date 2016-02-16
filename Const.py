# coding: utf-8

"""
const.py - константы игры (по сути, конфиг)
"""

from kivy import platform as _platform

###############################################################################

class Colors:
    blue   = (0, 0, 1, 1)
    gray   = (0.5, 0.5, 0.5, 1)
    green  = (0, 0.5, 0, 1)
    lime   = (0, 1, 0, 1)
    maroon = (0.5, 0, 0, 1)
    navy   = (0, 0, 0.5, 1)
    purple = (0.5, 0, 0.5, 1)
    red    = (1, 0, 0, 1)
    silver = (.75, .75, .75, 1)
    teal   = (0, 0.5, 0.5, 1)

# Ширина игрового поля относительно ширины всего экрана.
AREA_WIDTH = 0.8
# Высота игрового поля относительно высоты всего экрана.
AREA_HEIGHT = 1

if _platform == 'android':
	# ширина видимой области
	LOCAL_MAP_WIDTH = 8
	# высота видимой области
	LOCAL_MAP_HEIGHT = 8

	# ширина карты
	MAP_WIDTH = 32 + LOCAL_MAP_WIDTH * 2
	# высота карты
	MAP_HEIGHT = 32 + LOCAL_MAP_HEIGHT * 2
else:
	LOCAL_MAP_WIDTH = 8
	LOCAL_MAP_HEIGHT = 8

	MAP_WIDTH = 24 + LOCAL_MAP_WIDTH * 2
	MAP_HEIGHT = 24 + LOCAL_MAP_HEIGHT * 2

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
