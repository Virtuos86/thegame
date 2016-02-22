# coding: utf-8

"""
Hero.py - модуль, описывающий героя, главного персонажа игры.
"""

###############################################################################

import random

###############################################################################

import Const
import Tables
import Map
import Lowlevel

###############################################################################

def InitHero(HeroNum):
	"""Инициализация героя."""
	hero = Heroes[HeroNum]
	for i in xrange(Const.MaxChars):
	  hero.Chars[i] = 0
	for i in xrange(Const.MaxSkills):
	  hero.Skills[i] = 0

	hero.Level = 0
	hero.MaxHP = Tables.HPLevel_Table[hero.Level]
	hero.HP = hero.MaxHP
	hero.Exp = 0
	hero.MaxExp = Tables.ExpLevel_Table[hero.Level]
	hero.VisLong = 2

	curmap = Map.GameMap[Map.CurMap]
	def _():
		return ((curmap.LocalMapLeft + Const.LOCAL_MAP_WIDTH / 3 +
		    random.randint(0, Const.LOCAL_MAP_WIDTH / 3)),
		(curmap.LocalMapTop + Const.LOCAL_MAP_HEIGHT / 3 +
		    random.randint(0, Const.LOCAL_MAP_HEIGHT / 3)))

	x, y = _()
	while not Map.FreeTile(Map.GameMap[Map.CurMap].Cells[x][y].Tile):
		x, y = _()
	else:
		hero.x, hero.y = x, y

	SetHeroVisible(HeroNum)

def InitHeroes():
	global CurHero
	for i in xrange(Const.MaxHeroes):
	  InitHero(i)
	CurHero = 0

def  SetHeroVisible(HeroNum):
	hero = Heroes[HeroNum]
	curmap = Map.GameMap[Map.CurMap]
	for x in xrange(hero.x - hero.VisLong, hero.x + hero.VisLong + 1):
		for y in xrange(hero.y - hero.VisLong, hero.y + hero.VisLong + 1):
			curmap.Cells[x][y].IsVisible = True
			Lowlevel.ShowCell(curmap.Cells[x][y], x, y)

def ShowHero(HeroNum):
	hero = Heroes[HeroNum]
	x, y = (Const.WINDOW_LEFT + hero.x,
		    Const.WINDOW_TOP + hero.y)
	Lowlevel.ChangeTileSourceWithSavingPrevious(x, y, './resource/img/hero.png')

def CleaningUp(x, y):
	Lowlevel.CleaningUp(x, y)

###############################################################################

class THero(object):
	"""
	Представляет героя.
	"""
	__slots__ = ("Chars", "Skills", "x", "y", "HP", "MaxHP",
	             "Exp", "MaxExp", "Level", "VisLong")
	def __init__(self):
		super(THero, self).__init__()
		self.Chars = [0 for i in xrange(Const.MaxChars)]
		self.Skills = [0 for i in xrange(Const.MaxSkills)]
		self.x = 0
		self.y = 0
		self.HP = 0
		self.MaxHP = 0
		self.Exp = 0
		self.MaxExp = 0
		self.Level = 0
		self.VisLong = 0

# Список героев.
Heroes = [THero() for i in xrange(Const.MaxHeroes)]

# Индекс текущего героя.
CurHero = 0
