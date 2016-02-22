# coding: utf-8

"""
Game.py - модуль, ответственный за детали управления игрой.
"""

import Const
import Map
import Hero
import Monsters
import Lowlevel

def ShowGame():
	Lowlevel.ShowHeroInfo(Hero.CurHero)
	Map.ShowMap()


def MoveHero(dx, dy):
	hero = Hero.Heroes[Hero.CurHero]
	curmap = Map.GameMap[Map.CurMap]
	if not Map.FreeTile(curmap.Cells[hero.x + dx][hero.y + dy].Tile):
		return
	x, y = hero.x, hero.y
	hero.x += dx
	hero.y += dy
	Hero.SetHeroVisible(Hero.CurHero)
	Hero.CleaningUp(x, y)
	Monsters.ShowMonsters()
	Hero.ShowHero(Hero.CurHero)
	if (abs(hero.x - curmap.LocalMapLeft) < Map.SCROLL_DELTA) or \
	   (abs(hero.y - curmap.LocalMapTop) < Map.SCROLL_DELTA) or \
	   (abs(hero.x - (curmap.LocalMapLeft + Const.LOCAL_MAP_WIDTH)) < Map.SCROLL_DELTA) or \
	   (abs(hero.y - (curmap.LocalMapTop + Const.LOCAL_MAP_HEIGHT)) < Map.SCROLL_DELTA):
		Map.ScrollMap()
	Lowlevel.ShowHeroInfo(Hero.CurHero)
