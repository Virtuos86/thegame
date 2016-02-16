# coding: utf-8

"""
map.py - графический модуль игры

Условимся о двух типах свободной местности (например, земля и трава) и двух типах непроходимых зон (например, камни и дерево).
Кроме того, подготовим такие тайлы, как "ступеньки вверх" (переход на уровень выше) и "ступеньки вниз" (переход на уровень ниже).


"""

# Python модули.
import random

# Модули Kivy.
import kivy

# Модули игры.
import const
import lowlevel


###############################################################################

# Функции и процедуры.

def FreeTile(tile):
	"""Проверяет, проходим ли тайл."""
	return tile < const.tileFirstStopTile

def  MapGeneration(maplevel):
	"""Следующий шаг - генерация карты.
	Для этого существует немало хороших алгоритмов,
	  причем все они отличаются достаточно высокой сложностью.
	Мы возьмем простой вариант и будем расставлять непроходимые тайлы на пустой
	  карте случайно.
	Практика показывает, что если на карте около 35% непроходимых, случайно
	  "набросанных" тайлов, то перемещаться по ней становится ничуть не легче,
	  чем по лабиринту."""
	global GameMap, CurMap

	CurMap = maplevel

	for x in xrange(const.MAP_WIDTH):
		for y in xrange(const.MAP_HEIGHT):
			cell = GameMap[CurMap].Cells[x][y]
    		if (x <= const.LOCAL_MAP_WIDTH)
    		  or (x >= const.MAP_WIDTH - const.LOCAL_MAP_WIDTH)
    		  or (y <= const.LOCAL_MAP_HEIGHT)
    		  or (y >= const.MAP_HEIGHT - const.LOCAL_MAP_HEIGHT):
       			cell.Tile = const.tileStone
   			else:
   				if random.randint(0, 100) < 35:
          			cell.Tile = const.tileTree
      			elif random(0, 2) == 0:
      				cell.Tile = const.tileGrass
            	else:
            		cell.Tile = const.tileGround
    		cell.IsVisible = False

	GameMap[CurMap].LocalMapLeft = const.MAP_WIDTH / 2
	GameMap[CurMap].LocalMapTop = const.MAP_HEIGHT / 2

	# Создаем два спуска на нижележащие уровни.
	if maplevel < const.MaxDungeonLevel:
    	for i in (0, 1):
    		x1, y1 = FreeMapPoint(x, y)
    		GameMap[CurMap].Cells[x][y].Tile = const.tileStairsDown

	# Создаем один подъем на вышележащий уровень.
	if maplevel > 1:
    	x1, y1 = FreeMapPoint(x, y)
    	GameMap[CurMap].Cells[x][y].Tile = const.tileStairsUp

def  FreeMapPoint(x, y):
	"""Возвращает координаты рандомно найденной свободной ячейки карты."""
	def _():
		return (random.randint(0, const.MAP_WIDTH - const.LOCAL_MAP_WIDTH * 2) + const.LOCAL_MAP_WIDTH
	            random.randint(0, const.MAP_HEIGHT - const.LOCAL_MAP_HEIGHT * 2) + const.LOCAL_MAP_HEIGHT)
	x, y = _()
	while not FreeTile(GameMap[CurMap].Cells[x][y].Tile):
		x, y = _()
	return x, y

def  ShowMap():
	"""Рисует карту."""
	lowlewel.PrepareMap()
	for x in xrange(GameMap[CurMap].LocalMapLeft,
	                GameMap[CurMap].LocalMapLeft + const.LOCAL_MAP_WIDTH - 1):
		for y in xrange(GameMap[CurMap].LocalMapTop,
		                GameMap[CurMap].LocalMapTop + const.LOCAL_MAP_HEIGHT - 1):
	    	lowlevel.ShowCell(GameMap[CurMap].Cells[x][y], x, y)

###############################################################################

# Классы.

class TMapCell(object):
	"""Ячейка карты."""
	__slots__ = 'Tile', 'IsVisible'
	def __init__(self, tile=0, isvisible=False):
		super(TMapCell, self).__init__()
		self.Tile = tile
		self.IsVisible = isvisible

class TMap(object):
	"""Карта."""
	__slots__ = 'Cells', 'LocalMapLeft', 'LocalMapTop'
	def __init__(self, localmapleft=0, localmaptop=0):
		super(TMap, self).__init__()
    	self.Cells = [TMapCell() for row in xrange(const.MAP_WIDTH)
    	                        for col in xrange(const.MAP_HEIGHT)]
    	self.LocalMapLeft = localmapleft
    	self.LocalMapTop = localmaptop

class TGameMap(list):
	"""Список всех игровых уровней (карт)."""
	def __init__(self):
		super(TGameMap, self).__init__()
		for m in xrange(const.MaxDungeonLevel):
			self.append(TMap())

###############################################################################

# Создаем список игровых уровней.
GameMap = TGameMap()

# Текущая карта.
CurMap = 0

