import pygame
import numpy as np
import math

from movable import Movable

class Smiley(Movable):
	
	def __init__(self, pos, size, screen, vector):
		super().__init__(pos, screen, size)
		
		#worth 100 points
		self.points = 100
		print("This is not even remotely done yet @Smiley init")
		
		
class EnemyShip(Movable):
	
	def __init__(self, pos, screen, size):
		super().__init__(pos, screen, size)
		
		#worth 250 points
		self.points = 100
		print("This is not even remotely done yet @EnemyShip init")


class Comet(Movable):
	
	def __init__(self, pos, screen, size, level, image_obj, v_start, points):
		super().__init__(pos, screen, size)
		
		#big worth 20, middle 50, small 100
		
		self.level = level
		self.image = image_obj
		self.v_moving = v_start
		self.points = points
		
		
	def update_impl(self):
		pass
		#TODO: do something here?
	
	def blitme_impl(self):
		self.screen.blit(self.image, self.rect)

	def killme_impl(self, killer_v=None):
		self.kill()
		self.level.spawn_comet_children(self, killer_v)
