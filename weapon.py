import pygame
import numpy as np
import math

from movable import Movable


class Weapon:
	
	def __init__(self, owner, size, hp, base_speed, spawn_offset, image_file, targets, sound_file):
		
		self.owner = owner
		self.size = size
		self.hp = hp
		self.base_speed = base_speed
		self.spawn_offset = spawn_offset
		self.image = pygame.image.load(image_file)
		self.targets = targets
		#TODO: sound file needs mixer? https://www.pygame.org/docs/ref/mixer.html
		
		self.bullets = pygame.sprite.Group()

		#TODO: balance me, this is in ticks, 60 ticks a second (now)
		self.cooldown = 10
		self.cur_cooldown = 0
		
	
	def blitme(self):
		for bullet in self.bullets:
			bullet.blitme()
	
	
	def update(self):
		
		if self.cur_cooldown > 0:
			self.cur_cooldown -= 1

		for bullet in self.bullets:
			if bullet.hp <= 0:
				bullet.kill()
				continue
				#TODO: animation????? how???
			else:
				bullet.update()
			
			
	def shoot(self):
		#this is offsetting the spawn point of the bullet in the direction
		#the ship is facing
		if self.cur_cooldown <= 0 and len(self.bullets) < 4: #max 4 bullets	
			pos = (self.owner.rect.centerx + self.owner.v_facing[0] * self.spawn_offset,
					self.owner.rect.centery + self.owner.v_facing[1] * self.spawn_offset)
			bullet = Bullet(pos, self.owner.screen, self.size, self.owner, 
								self.hp, self.base_speed, self.image, self.targets)
			
			self.bullets.add(bullet)
			bullet.spawn()
			#we shot, so the cooldown is up again
			self.cur_cooldown += self.cooldown
	


class Bullet(Movable):
	
	def __init__(self, pos, screen, size, owner, hp, base_speed, image_obj, targets):
		super().__init__(pos, screen, size)

		self.name = "bullet"

		self.owner = owner
		self.hp = hp
		self.image = image_obj
		self.targets = targets
		
		self.base_speed = base_speed
		
		self.v_facing[0] = owner.v_facing[0]
		self.v_facing[1] = owner.v_facing[1]
		
		self.v_moving[0] = owner.v_moving[0] + self.v_facing[0] * (self.base_speed * owner.props.f_bullet_speed)
		self.v_moving[1] = owner.v_moving[1] + self.v_facing[1] * (self.base_speed * owner.props.f_bullet_speed)

		
	def blitme_impl(self):
		self.screen.blit(self.image, self.rect)	
		
	def update_impl(self):
		self.hp -= 1

	def killme_impl(self, v_killer=None, killer=None):
		self.kill()

	#override since self.owner is the killer not the bullet itself
	def check_collision(self):
		for i in list(range(0,len(self.targets))):
			collisions = pygame.sprite.spritecollide(self, self.targets[i], False)
			if len(collisions) > 0:
				for j in list(range(0, len(collisions))):
					if not collisions[j].hidden and collisions[j] != self and collisions[j] != self.owner:
						collisions[j].killme(self.v_moving, self.owner)
						self.killme(collisions[j].v_moving, collisions[j])
						return