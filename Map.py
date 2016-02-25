# coding: utf-8

"""
Map.py - графический модуль игры

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
import Hero
import Monsters


###############################################################################

# Функции и процедуры.

def FreeTile(tile):
	"""Проверяет, проходим ли тайл."""
	return tile < Const.tileFirstStopTile

def  MapGeneration(maplevel):
	"""
	Следующий шаг - генерация карты.
	Для этого существует немало хороших алгоритмов,
	  причем все они отличаются достаточно высокой сложностью.
	Мы возьмем простой вариант и будем расставлять непроходимые тайлы на пустой
	  карте случайно.
	Практика показывает, что если на карте около 35% непроходимых, случайно
	  "набросанных" тайлов, то перемещаться по ней становится ничуть не легче,
	  чем по лабиринту.
	"""
	global GameMap, CurMap

	CurMap = maplevel
	curmap = GameMap[CurMap]

	for x in xrange(Const.MAP_WIDTH):
		for y in xrange(Const.MAP_HEIGHT):
			cell = curmap.Cells[x][y]
			if (  x <= Const.LOCAL_MAP_WIDTH / 2) \
			  or (x >= Const.MAP_WIDTH - Const.LOCAL_MAP_WIDTH / 2) \
			  or (y <= Const.LOCAL_MAP_HEIGHT / 2) \
			  or (y >= Const.MAP_HEIGHT - Const.LOCAL_MAP_HEIGHT / 2):
	   			cell.Tile = Const.tileStone
			else:
				if random.randint(0, 100) < 33:
					cell.Tile = Const.tileTree
				elif random.randint(0, 2) == 0:
					cell.Tile = Const.tileGrass
				else:
					cell.Tile = Const.tileGround
			cell.IsVisible = False

	curmap.LocalMapLeft = Const.MAP_WIDTH / 2
	curmap.LocalMapTop = Const.MAP_HEIGHT / 2

	# Создаем два спуска на нижележащие уровни.
	if maplevel > 1:
		for i in (0, 1):
			x1, y1 = FreeMapPoint()
			curmap.Cells[x1][y1].Tile = Const.tileStairsDown

	# Создаем один подъем на вышележащий уровень.
	if maplevel < Const.MaxDungeonLevel:
		x1, y1 = FreeMapPoint()
		curmap.Cells[x1][y1].Tile = Const.tileStairsUp

def  FreeMapPoint():
	"""Возвращает координаты рандомно найденной свободной ячейки карты."""
	curmap = GameMap[CurMap]
	def _():
		return (random.randint(0, Const.MAP_WIDTH - Const.LOCAL_MAP_WIDTH * 2) \
		    + Const.LOCAL_MAP_WIDTH,
		      random.randint(0, Const.MAP_HEIGHT - Const.LOCAL_MAP_HEIGHT * 2) \
		    + Const.LOCAL_MAP_HEIGHT)
	x, y = _()
	while not FreeTile(curmap.Cells[x][y].Tile):
		x, y = _()
	return x, y

def  VisiblePoint(x, y):
	"""Функция проверки, лежит ли некая точка в видимой части карты."""
	curmap = GameMap[CurMap]
	return (
	           curmap.Cells[x][y].IsVisible and
	           (x >= curmap.LocalMapLeft) and
	           (x < curmap.LocalMapLeft + Const.LOCAL_MAP_WIDTH) and
	           (y >= curmap.LocalMapTop) and
	           (y < curmap.LocalMapTop + Const.LOCAL_MAP_HEIGHT)
	        )

def  ShowMap():
	"""Рисует карту."""
	curmap = GameMap[CurMap]
	Lowlevel.PrepareMap()
	for x in xrange(
	    curmap.LocalMapLeft,
	    curmap.LocalMapLeft + Const.LOCAL_MAP_WIDTH + 1):
		for y in xrange(curmap.LocalMapTop,
		                curmap.LocalMapTop + Const.LOCAL_MAP_HEIGHT + 1):
			Lowlevel.ShowCell(curmap.Cells[x][y], x, y)
	# Хак.
	Monsters.ShowMonsters()
	Hero.ShowHero(Hero.CurHero)
	Lowlevel.main()

def ScrollMap():
	"""Прокрутка карты."""
	hero = Hero.Heroes[Hero.CurHero]
	curmap = GameMap[CurMap]
	curmap.LocalMapLeft = hero.x - Const.LOCAL_MAP_WIDTH / 2
	curmap.LocalMapTop = hero.y - Const.LOCAL_MAP_HEIGHT / 2

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
		self.Cells = [[TMapCell() for x in xrange(Const.MAP_HEIGHT)] for y in xrange(Const.MAP_WIDTH)]
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

# Определяет допустимую близость героя к краям видимого окна.
SCROLL_DELTA = 3
