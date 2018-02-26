import pygame
import numpy as np
import math

from movable import Movable
from weapon import Weapon


class Smiley(Movable):
	
	def __init__(self, pos, screen, size, level, image_obj, v_start):
		super().__init__(pos, screen, size)
		
		#worth 100 points
		self.level = level
		self.image = image_obj #TODO?
		self.v_moving = v_start #TODO at first it should move a bit away from it's spawn location
		self.homing_targets = [level.enemy_ships, level.ships_group]

		self.points = 100
		print("This is not even remotely done yet @Smiley init")

	def update_impl(self): #not needed
		pass #TODO seek homing_targets, move towards them

	def check_collision(self): #overridden since others check for this
		pass

	def blitme_impl(self):
		self.screen.blit(self.image, self.rect) #TODO do smileys rotate images?

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()
		
		
class EnemyShip(Movable):
	
	def __init__(self, pos, screen, size, level, image_obj):
		super().__init__(pos, screen, size)

		self.level = level
		self.image = image_obj

		#worth 250 points
		self.points = 100
		print("This is not even remotely done yet @EnemyShip init")

		self.targets = [level.comets, level.smilies, level.ships_group] #TODO so far enemyShips do not have friendly fire

		#TODO: balance hp, size, speed, image and sound here
		self.weapon = Weapon(self, 5, 120, 2.0, 13, "pics/bullet_dummy.png", self.targets, "TODO:soundfile")


	def update_impl(self): #not needed
		self.weapon.update() #this just decreases cooldown and kills old bullets
		#TODO I need to acquire targets from self.targets and shoot at them, also move around (also target != self)
		#use the self.weapon.shoot(), adjust the self.v_facing for that!
		#TODO kinda completely redo the movement here since it's weird


	def blitme_impl(self):
		self.weapon.blitme() #drawing projectiles before, so ship is on top
		self.screen.blit(self.image, self.rect) #TODO do ships rotate images?

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()

class Comet(Movable):
	
	def __init__(self, pos, screen, size, level, image_obj, v_start, points, round_number):
		super().__init__(pos, screen, size)
		
		#big worth 20, middle 50, small 100
		
		self.level = level
		self.image = image_obj
		self.v_moving = v_start
		self.points = points
		self.round_number = round_number

		if size >= 50:
			self.type = "big"
		elif size >= 27:
			self.type = "medium"
		else:
			self.type = "small"

		print("debug: created comet with size: "+str(size) + " in round_number: "+str(round_number))
		
		
	def update_impl(self): #not needed
		pass

	def check_collision(self): #overridden since comets don't check for this, the other sprites do
		pass

	def blitme_impl(self):
		self.screen.blit(self.image, self.rect)

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()
		self.level.spawn_comet_children(self, v_killer)
