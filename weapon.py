import pygame
import numpy as np
import math

from movable import Movable


class Weapon():
	
	def __init__(self, owner, size, hp, spawn_offset, image_file, sound_file):
		
		self.owner = owner
		self.size = size
		self.hp = hp
		self.spawn_offset = spawn_offset
		self.image = pygame.image.load(image_file)
		#TODO: sound file needs mixer? https://www.pygame.org/docs/ref/mixer.html
		
		self.bullets = [] #for refrence in global list of movables (for disruptor)
		
		#TODO: balance me, this is in ticks, 60 ticks a second (now)
		self.cooldown = 20
		self.cur_cooldown = 0
		
	
	def blitme(self):
		for bullet in self.bullets:
			bullet.blitme()
	
	
	def update(self):
		
		if self.cur_cooldown > 0:
			self.cur_cooldown -= 1
		
		for bullet in self.bullets:
			bullet.update()
			#TODO: if bullet.hp <= 0:
			#		bullet.destroy() animation????? how???
		
		#filtering out any bullet that is supposed to be dead
		self.bullets = [b for b in self.bullets if b.hp > 0]
			
			
	def shoot(self):
		#this is offsetting the spawn point of the bullet in the direction
		#the ship is facing
		if self.cur_cooldown <= 0 and len(self.bullets) < 4: #max 4 bullets	
			pos = (self.owner.rect.centerx + self.owner.v_facing[0] * self.spawn_offset,
					self.owner.rect.centery + self.owner.v_facing[1] * self.spawn_offset)
			bullet = Bullet(pos, self.owner.screen, self.size, self.owner, 
								self.hp, self.image)
			
			self.bullets.append(bullet) 
			#we shot, so the cooldown is up again
			self.cur_cooldown += self.cooldown
	


class Bullet(Movable):
	
	def __init__(self, pos, screen, size, creator, hp, image_obj):
		super().__init__(pos, screen, size)
		
		self.creator = creator
		self.hp = hp
		self.image = image_obj
		
		#TODO: balance me, maybe move this to the arguments
		self.base_speed = 2.0
		
		self.v_facing[0] = creator.v_facing[0]
		self.v_facing[1] = creator.v_facing[1]
		
		self.v_moving[0] = creator.v_moving[0] + self.v_facing[0] * (self.base_speed * creator.props.f_bullet_speed)
		self.v_moving[1] = creator.v_moving[1] + self.v_facing[1] * (self.base_speed * creator.props.f_bullet_speed)
		
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)	
		
	def update_impl(self):
		self.hp -= 1	
