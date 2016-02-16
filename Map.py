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
import Const
import Lowlevel


###############################################################################

# Функции и процедуры.

def FreeTile(tile):
	"""Проверяет, проходим ли тайл."""
	return tile < Const.tileFirstStopTile

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

	for x in xrange(Const.MAP_WIDTH):
		for y in xrange(Const.MAP_HEIGHT):
			cell = GameMap[CurMap].Cells[x][y]
			if (  x <= Const.LOCAL_MAP_WIDTH) \
			  or (x >= Const.MAP_WIDTH - Const.LOCAL_MAP_WIDTH) \
			  or (y <= Const.LOCAL_MAP_HEIGHT) \
			  or (y >= Const.MAP_HEIGHT - Const.LOCAL_MAP_HEIGHT):
	   			cell.Tile = Const.tileStone
			else:
				if random.randint(0, 100) < 35:
					cell.Tile = Const.tileTree
				elif random.randint(0, 2) == 0:
					cell.Tile = Const.tileGrass
				else:
					cell.Tile = Const.tileGround
			cell.IsVisible = False

	GameMap[CurMap].LocalMapLeft = Const.MAP_WIDTH / 2
	GameMap[CurMap].LocalMapTop = Const.MAP_HEIGHT / 2

	# Создаем два спуска на нижележащие уровни.
	if maplevel < Const.MaxDungeonLevel:
		for i in (0, 1):
			x1, y1 = FreeMapPoint(x, y)
			GameMap[CurMap].Cells[x][y].Tile = Const.tileStairsDown

	# Создаем один подъем на вышележащий уровень.
	if maplevel > 1:
		x1, y1 = FreeMapPoint(x, y)
		GameMap[CurMap].Cells[x][y].Tile = Const.tileStairsUp

def  FreeMapPoint(x, y):
	"""Возвращает координаты рандомно найденной свободной ячейки карты."""
	def _():
		return (random.randint(0, Const.MAP_WIDTH - Const.LOCAL_MAP_WIDTH * 2) + Const.LOCAL_MAP_WIDTH,
		        random.randint(0, Const.MAP_HEIGHT - Const.LOCAL_MAP_HEIGHT * 2) + Const.LOCAL_MAP_HEIGHT)
	x, y = _()
	while not FreeTile(GameMap[CurMap].Cells[x][y].Tile):
		x, y = _()
	return x, y

def  ShowMap():
	"""Рисует карту."""
	Lowlevel.PrepareMap()
	for x in xrange(GameMap[CurMap].LocalMapLeft,
				                GameMap[CurMap].LocalMapLeft + Const.LOCAL_MAP_WIDTH - 1):
					for y in xrange(GameMap[CurMap].LocalMapTop,
					                GameMap[CurMap].LocalMapTop + Const.LOCAL_MAP_HEIGHT - 1):
						Lowlevel.ShowCell(GameMap[CurMap].Cells[x][y], x, y)
	Lowlevel.main()

###############################################################################

# Классы.

class TMapCell(object):
	"""Ячейка карты."""
	__slots__ = 'Tile', 'IsVisible'
	def __init__(self, tile=0, isvisible=False):
		super(TMapCell, self).__init__()
		self.Tile = tile
		self.IsVisible = isvisible
	def __repr__(self):
		return "(%s, %s)" % (self.Tile, self.IsVisible)

class TMap(object):
	"""Карта."""
	__slots__ = 'Cells', 'LocalMapLeft', 'LocalMapTop'
	def __init__(self, localmapleft=0, localmaptop=0):
		super(TMap, self).__init__()
		self.Cells = [[TMapCell() for col in xrange(Const.MAP_HEIGHT)] for row in xrange(Const.MAP_WIDTH)]
		self.LocalMapLeft = localmapleft
		self.LocalMapTop = localmaptop

class TGameMap(list):
	"""Список всех игровых уровней (карт)."""
	def __init__(self):
		super(TGameMap, self).__init__()
		for m in xrange(Const.MaxDungeonLevel):
			self.append(TMap())

###############################################################################

# Создаем список игровых уровней.
GameMap = TGameMap()

# Текущая карта.
CurMap = 0

