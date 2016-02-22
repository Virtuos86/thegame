# coding: utf-8

"""
Monsters.py - модуль, описывающий монстров.
"""

# Python модули.
import random

# Модули игры.
import Texts
import Map
import Lowlevel

###############################################################################

class TMonster(object):
	__slots__ = ("Name", "ID", "x", "y", "HP", "MaxHP", "XP", "Level",
	             "Ad1", "Ad2", "Dd1", "Dd2",
	             "ViewZone", "RandomStep")
	def __init__(self, **kwargs):
		"""
		Поле ID - некий уникальный идентификатор, позволяющий отличить один тип
		монстров от другого.
		Значение полей Ad1, Ad2 задает величину поражения, которое наносится
		  монстром герою (бросается Ad1 кубиков, каждый из которых описывается
		  Ad2 гранями, и выброшенные результаты суммируются).
		Поля Dd1 и Dd2, которые можно условно отнести к толщине шкуры,
		  определяют величину, которую монстр отражает (вычитает) из поражения,
		  которое ему нанесено.
		Уровень монстра (Level) позволит корректно определять количество опыта,
		  получаемое героем при победе. Если уровень героя выше, опыт будет
		  меньше - и наоборот.
		Монстр с уровнем здоровья (HP), меньшим или равным нулю, считается
		  мертвым и на карте не показывается.
		"""
		super(TMonster, self).__init__()
		self.Name = kwargs.get('Name', "")
		self.ID = kwargs.get('ID', 0)

		self.x = kwargs.get('x', 0)
		self.y = kwargs.get('y', 0)
		self.HP = kwargs.get('HP', 0)
		self.MaxHP = kwargs.get('MaxHP', 0)
		self.XP = kwargs.get('XP', 0)
		self.Level = kwargs.get('Level', 0)
		self.Ad1 = kwargs.get('Ad1', 0)
		self.Ad2 = kwargs.get('Ad2', 0)
		self.Dd1 = kwargs.get('Dd1', 0)
		self.Dd2 = kwargs.get('Dd2', 0)
		self.ViewZone = kwargs.get('ViewZone', 0)
		self.RandomStep = kwargs.get('RandomStep', 0)

	def __str__(self):
		res = "{"
		res += ''.join(['"%s": %s,' % (s, getattr(self, s)) for s in self.__slots__])
		res += "}"
		return res

	def update_scills(self, MonsterType):
		for k, v in MonsterType.items():
			setattr(self, k, v)

MonsterTypes = [mns for mns in (
	{
	    'Name': Texts.STR_MONSTER1,
	    'ID': 1, 'x': 0, 'y': 0,
	    'HP': 1, 'MaxHP': 1, 'XP': 1, 'Level': 1,
	    'Ad1': 1, 'Ad2': 3, 'Dd1': 1, 'Dd2': 2,
	    'ViewZone': 4,
	    'RandomStep': 3
	},
	{
	    'Name': Texts.STR_MONSTER2,
	    'ID': 2, 'x': 0, 'y': 0,
	    'HP': 2, 'MaxHP': 2, 'XP': 2, 'Level': 1,
	    'Ad1': 1, 'Ad2': 6, 'Dd1': 1, 'Dd2': 2,
	    'ViewZone': 3,
	    'RandomStep': 4
	},
	{
	    'Name': Texts.STR_MONSTER3,
	    'ID': 3, 'x': 0, 'y': 0,
	    'HP': 5, 'MaxHP': 5, 'XP': 3, 'Level': 1,
	    'Ad1': 1, 'Ad2': 2, 'Dd1': 2, 'Dd2': 2,
	    'ViewZone': 4,
	    'RandomStep': 5
	},
	{
	    'Name': Texts.STR_MONSTER4,
	    'ID': 4, 'x': 0, 'y': 0,
	    'HP': 9, 'MaxHP': 9, 'XP': 7, 'Level': 2,
	    'Ad1': 2, 'Ad2': 4, 'Dd1': 1, 'Dd2': 6,
	    'ViewZone': 3,
	    'RandomStep': 5
	},
	{
	    'Name': Texts.STR_MONSTER5,
	    'ID': 5, 'x': 0, 'y': 0,
	    'HP': 12, 'MaxHP': 12, 'XP': 9, 'Level': 2,
	    'Ad1': 3, 'Ad2': 3, 'Dd1': 3, 'Dd2': 2,
	    'ViewZone': 3,
	    'RandomStep': 4
	},
	{
	    'Name': Texts.STR_MONSTER6,
	    'ID': 6, 'x': 0, 'y': 0,
	    'HP': 20, 'MaxHP': 20, 'XP': 15, 'Level': 3,
	    'Ad1': 2, 'Ad2': 6, 'Dd1': 1, 'Dd2': 10,
	    'ViewZone': 4,
	    'RandomStep': 4
	},
	{
	    'Name': Texts.STR_MONSTER7,
	    'ID': 7, 'x': 0, 'y': 0,
	    'HP': 35, 'MaxHP': 35, 'XP': 30, 'Level': 4,
	    'Ad1': 4, 'Ad2': 10, 'Dd1': 2, 'Dd2': 6,
	    'ViewZone': 5,
	    'RandomStep': 3
	})]

MaxMonsters = 50
Monsters = [TMonster() for mns in xrange(MaxMonsters)]

def GenerateMonsters(CurMap):
	"""
	Отбираем типы монстров, чей уровень соответствует уровню карты.
	Инициализируем всех монстров, рандомно выбирая их тип из ранее отобранных, и
	  в случайном порядке помещаем их на свободные тайлы.
	"""
	AllowedMonsterTypes = [MonsterType for MonsterType in MonsterTypes if MonsterType['Level'] == CurMap]
	for mns in Monsters:
		mns.update_scills(random.choice(AllowedMonsterTypes))
		mns.x, mns.y = Map.FreeMapPoint()


def ShowMonsters():
	"""Сканирует список монстров, определяет, какие из живых созданий находятся
	  в видимой части окна, и выводит их на экран."""
	for mns in Monsters:
		if (mns.HP > 0) and Map.VisiblePoint(mns.x, mns.y):
			Lowlevel.ShowMonster(mns)
