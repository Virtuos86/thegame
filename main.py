import sys;reload(sys)
sys.setdefaultencoding('utf-8')

import Map
import Lowlevel
import Hero
import Game
import Monsters

def main():
	Lowlevel.VideoInitialize()
	Map.MapGeneration(1)
	Monsters.GenerateMonsters(Map.CurMap)
	Hero.InitHeroes()
	Game.ShowGame()

if __name__ == '__main__':
	main()
