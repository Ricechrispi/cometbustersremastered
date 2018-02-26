import pygame
import numpy as np
import math

class Movable(pygame.sprite.Sprite):
	
	def __init__(self, pos, screen, size):
		super().__init__()
		
		self.spawn_pos = [pos[0],pos[1]] #spawn is the same as the start location
		self.hidden = True

		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.screen_dims = screen.get_size() #(width, height)
	
		self.v_facing = np.array([0.0, -1.0]) #everything starts facing upwards
		self.v_moving = np.array([0.0, 0.0]) #everythings starts by not moving
		
		self.f_drag = 1.0 #no drag normally
		
		self.size = size
		self.rect = pygame.Rect(0,0, size, size)
		self.rect.centerx = pos[0]
		self.rect.centery = pos[1]
		self.f_centerx = float(self.rect.centerx)
		self.f_centery = float(self.rect.centery)

		self.points = 0 #everything is worth 0 points unless overridden
		self.score = 0 #everything keeps score.. even comets? xD

		self.targets = [] #everybody needs to override this to collide with something..

	def spawn(self):
		self.rect.centerx = self.spawn_pos[0]
		self.rect.centery = self.spawn_pos[1]
		self.f_centerx = float(self.spawn_pos[0])
		self.f_centery = float(self.spawn_pos[1])
		self.hidden = False

	def update(self):

		if not self.hidden:
			for i in [0,1]: #this is to prevent absurd calculations of drag
				if math.fabs(self.v_moving[i]) <= 0.0005:
					self.v_moving[i] = 0.0

			#TODO: does this work correctly? is drag evenly applied? x/y? ???
			self.v_moving = self.v_moving * self.f_drag #every update, we apply drag

			self.update_impl()

			#keeping a more accuarte position for calculations
			self.f_centerx += self.v_moving[0]
			self.f_centery += self.v_moving[1]

			#this is to wrap items around the edges
			self.f_centerx = self.f_centerx % self.screen_dims[0]
			self.f_centery = self.f_centery % self.screen_dims[1]

			#rect.centerxy is used for drawing, but is limited to ints
			self.rect.centerx = int(round(self.f_centerx))
			self.rect.centery = int(round(self.f_centery))

			self.check_collision()

		else:
			self.update_impl()
		
		
	def update_impl(self):
		print("NEVER USE THIS, OVERRIDE ME! @update_impl, Movable")

	def blitme(self):
		if not self.hidden:
			self.blitme_impl()

	def blitme_impl(self):
		print("NEVER USE THIS, OVERRIDE ME! @blitme, Movable")

	def killme(self, v_killer=None, killer=None):
		self.hidden = True
		if killer:
			killer.score += self.points
		self.killme_impl(v_killer, killer)

	def killme_impl(self, v_killer=None, killer=None):
		print("NEVER USE THIS, OVERRIDE ME! @killme, Movable")


	def check_collision(self):
		for i in list(range(0,len(self.targets))):
			collisions = pygame.sprite.spritecollide(self, self.targets[i], False)
			if len(collisions) > 0:
				for j in list(range(0, len(collisions))):
					if not collisions[j].hidden and collisions[j] != self:
						collisions[j].killme(self.v_moving, self)
						self.killme(collisions[j].v_moving, collisions[j])
						return
