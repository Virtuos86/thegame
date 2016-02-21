# coding: utf-8

"""
Модуль, ответственный за детали управления игрой.
"""

import Map
import Hero

def ShowGame():
	Map.ShowMap()

def MoveHero(dx, dy):
	hero = Hero.Heroes[Hero.CurHero]
	if not Map.FreeTile(Map.GameMap[Map.CurMap].Cells[hero.x + dx][hero.y + dy].Tile):
		return
	x, y = hero.x, hero.y
	hero.x += dx
	hero.y += dy
	Hero.SetHeroVisible(Hero.CurHero)
	Hero.CleaningUp(x, y)
	Hero.ShowHero(Hero.CurHero)
