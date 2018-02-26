import pygame

from movable import Movable
from weapon import Weapon
import utility_functions as util
import levels



class Smiley(Movable):
	
	def __init__(self, pos, screen, size, level, v_start):
		super().__init__(pos, screen, size)

		self.name = "smiley"

		self.level = level
		self.image = pygame.image.load("pics/smiley.png")
		self.cropped_rects = util.cropped_image_rects(14, 14, 32)
		self.frames_per_image = 4  # TODO adjust
		self.cur_image_frames = 0
		self.cur_image_index = 0

		self.v_moving = v_start #TODO at first it should move a bit away from it's spawn location
		self.homing_targets = [level.enemy_ships, level.ships_group]

		#worth 100 points
		self.points = 100

	def update_impl(self): #not needed
		#TODO seek homing_targets, move towards them
		pass

	def check_collision(self): #overridden since others check for this
		pass

	def blitme_impl(self):
		if self.cur_image_frames >= self.frames_per_image:
			self.cur_image_index = (self.cur_image_index + 1) % len(self.cropped_rects)
			self.cur_image_frames = 0

		self.screen.blit(self.image, self.rect, self.cropped_rects[self.cur_image_index])

		self.cur_image_frames += 1

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()
		
		
class EnemyShip(Movable):
	
	def __init__(self, pos, screen, size, level):
		super().__init__(pos, screen, size)

		self.name = "enemyShip"


		self.level = level
		self.image = pygame.image.load("pics/enemy_ship.png")
		self.cropped_rects = util.cropped_image_rects(40,36,8)
		self.frames_per_image = 4 #TODO adjust
		self.cur_image_frames = 0
		self.cur_image_index = 0

		#worth 250 points
		self.points = 250

		self.targets = [level.comets, level.smilies, level.ships_group] #TODO so far enemyShips do not have friendly fire

		#TODO: balance hp, speed, and sound here
		self.weapon = Weapon(self, (9,9), 120, 2.0, 13, "pics/enemy_bullet.png", self.targets, "TODO:soundfile")


	def update_impl(self): #not needed
		self.weapon.update() #this just decreases cooldown and kills old bullets
		#TODO I need to acquire targets from self.targets and shoot at them, also move around (also target != self)
		#use the self.weapon.shoot(), adjust the self.v_facing for that!
		#TODO kinda completely redo the movement here since it's weird


	def blitme_impl(self):
		self.weapon.blitme() #drawing projectiles before, so ship is on top

		if self.cur_image_frames >= self.frames_per_image:
			self.cur_image_index = (self.cur_image_index + 1) % len(self.cropped_rects)
			self.cur_image_frames = 0

		self.screen.blit(self.image, self.rect, self.cropped_rects[self.cur_image_index])

		self.cur_image_frames += 1

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()

class Comet(Movable):
	
	def __init__(self, pos, screen, size, level, image_obj, v_start, points, round_number):
		super().__init__(pos, screen, size)

		self.name = "comet"

		#big worth 20, middle 50, small 100

		self.level = level
		self.image = image_obj
		self.v_moving = v_start
		self.points = points
		self.round_number = round_number

		if size[0] >= 50 or size[1] >= 50:
			self.type = "big"
		elif size[0] >= 27 or size[1] >= 27:
			self.type = "medium"
		else:
			self.type = "small"

		
	def update_impl(self): #not needed
		pass

	def check_collision(self): #overridden since comets don't check for this, the other sprites do
		pass

	def blitme_impl(self):
		self.screen.blit(self.image, self.rect)

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()
		self.level.spawn_comet_children(self, v_killer)
