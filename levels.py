import pygame
import numpy as np
import random
import math

import utility_functions as util
import hostiles

class Level:
	
	def __init__(self, screen, difficulty):
		#TODO: chance of enemies spawning, difficulty etc.
		self.screen = screen
		self.screen_dims = screen.get_size()

		# level 1: 9 on easy, 12 on challenging, 14 on impossible
		if difficulty == 0:
			self.amount_of_comets = 9
		elif difficulty == 1:
			self.amount_of_comets = 12
		elif difficulty == 2:
			self.amount_of_comets = 14
		else:
			print("debug: settings file has unknown difficulty, defaulting to 0")
			self.amount_of_comets = 9

		self.comets = pygame.sprite.Group()
		self.enemy_ships = pygame.sprite.Group()
		self.smilies = pygame.sprite.Group()

		self.smiley_chances = []
		self.comet_images_big = []
		self.comet_images_med = []
		self.comet_images_small = []
		image_string = "pics/comet"
		
		for i in range(1,9):
			self.comet_images_big.append(pygame.image.load(image_string + str(i) + "b.png"))
			self.comet_images_med.append(pygame.image.load(image_string + str(i) + "m.png"))
			self.comet_images_small.append(pygame.image.load(image_string + str(i) + "s.png"))
			self.smiley_chances.append(100) #TODO factor in difficulty, round_number etc.
			


	def update(self):
		for comet in self.comets:
			comet.update()
		for enemy in self.enemy_ships:
			enemy.update()
		for smiley in self.smilies:
			smiley.update()

		#TODO random chance to spawn an enemy ship here! factor in difficulty?

		
	def blitme(self):
		for comet in self.comets:
			comet.blitme()
		for enemy in self.enemy_ships:
			enemy.blitme()
		for smiley in self.smilies:
			smiley.blitme()


	def spawn_comet_children(self, comet, v_killer):

		if comet.type == "big":
			new_points = 50
			image = self.comet_images_med[comet.round_number]
		elif comet.type == "medium":
			new_points = 100
			image = self.comet_images_small[comet.round_number]
		else:
			return

		new_size = max(image.get_size()[0], image.get_size()[1]) #some are not squares, but this is close enough

		new_v = np.array([comet.v_moving[0] + v_killer[0], comet.v_moving[1] + v_killer[1]])
		#TODO: this is not very realistic, mostly bullshit and way too fast
		new_v1 = util.rotate_v(new_v, 45)
		new_v2 = util.rotate_v(new_v, -45)

		new_comet1 = hostiles.Comet([comet.rect.centerx,comet.rect.centery], self.screen, new_size,
						self, image, new_v1, new_points, comet.round_number)

		new_comet2 = hostiles.Comet([comet.rect.centerx,comet.rect.centery], self.screen, new_size,
						self, image, new_v2, new_points, comet.round_number)

		#print("debug: parent comet.v_moving: " + str(comet.v_moving))
		#print("debug: parent rect.centerx: " + str(comet.rect.centerx))
		#print("debug: parent rect.centery: " + str(comet.rect.centery))

		#print("debug: child1 v_moving: " + str(new_comet1.v_moving))
		#print("debug: child1 rect.centerx: " + str(new_comet1.rect.centerx))
		#print("debug: child1 rect.centery: " + str(new_comet1.rect.centery))

		#print("debug: child2 v_moving: " + str(new_comet2.v_moving))
		#print("debug: child2 rect.centerx: " + str(new_comet2.rect.centerx))
		#print("debug: child2 rect.centery: " + str(new_comet2.rect.centery))

		self.comets.add(new_comet1)
		self.comets.add(new_comet2)

		new_comet1.spawn()
		new_comet2.spawn()


	def spawn_comets(self, amount, velocity, round_number):
		
		points = self.generate_spawn_points(amount)
		vectors = self.generate_vectors(amount)
		
		new_vectors = []
		for v in vectors:
			new_vectors.append(v*velocity)
		
		for i in list(range(0,amount)): #TODO: balance these values (smiley)

			size = max(self.comet_images_big[round_number].get_size()[0],  #this is not perfect, but close enough
						self.comet_images_big[round_number].get_size()[1])

			new_comet = hostiles.Comet(points[i], self.screen, size, self, self.comet_images_big[round_number],
									   	new_vectors[i], 20, round_number)

			self.comets.add(new_comet)
			new_comet.spawn()

	
	def generate_spawn_points(self, amount):
	
		points = []
		border_pixels = 10
		
		x_range_ver1 = [0, border_pixels]
		x_range_ver2 = [self.screen_dims[0] - border_pixels, self.screen_dims[0]]
		x_range_hor = [border_pixels, self.screen_dims[0] - border_pixels]
		
		y_range_ver = [0,self.screen_dims[1]]
		y_range_hor1 = [0, border_pixels]
		y_range_hor2 = [self.screen_dims[1] - border_pixels, self.screen_dims[1]]
		
		#ranges = [x_range_ver1, x_range_ver2, x_range_hor, y_range_ver, y_range_hor1, y_range_hor2]
		#print("ranges: " + str(ranges))
		
		#this is ugly af, but it works and im am lazy
		a1 = a2 = a3 = a4 = int(amount/4)
		if amount % 4 == 1:
			a1 += 1
		if amount % 4 == 2:
			a1 += 1
			a2 += 1
		if amount % 4 == 3:
			a1 += 1
			a2 += 1
			a3 += 1

		#there is no point in making this a loop, these 4 statements work
		b1 = self.generate_points_in_rect(a1, x_range_ver1, y_range_ver)
		b2 = self.generate_points_in_rect(a2, x_range_ver2, y_range_ver)
		b3 = self.generate_points_in_rect(a3, x_range_hor, y_range_hor1)
		b4 = self.generate_points_in_rect(a4, x_range_hor, y_range_hor2)
		
		boxes = [b1,b2,b3,b4]
		
		for b in boxes:
			for p in b:
				points.append(p)
		
		return points
		
	def generate_points_in_rect(self, amount, x_range, y_range):
		
		points = []
		
		for i in range(0, amount):
			x = random.randint(x_range[0], x_range[1])
			y = random.randint(y_range[0], y_range[1])
			p = np.array([x, y])
			points.append(p)
		
		return points
		
	def generate_vectors(self, amount):
		
		vectors = []
		for i in range(0, amount):
			x = random.random() * 2 -1
			y = random.random() * 2 -1
			
			new_v = np.array([x, y])
			mag = util.mag_v(new_v)
			if mag is not 0.0:
				new_v = new_v / mag
			
			vectors.append(new_v)
		
		return vectors
