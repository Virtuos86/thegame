import Map
import Lowlevel
import Hero
import Game

def main():
	Lowlevel.VideoInitialize()
	Map.MapGeneration(1)
	Hero.InitHeroes()
	Game.ShowGame()

if __name__ == '__main__':
	main()
