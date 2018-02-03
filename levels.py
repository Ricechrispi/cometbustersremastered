import pygame
import pygame
import numpy as np
import random
import math

import utility_functions as util
import hostiles

class Level():
	
	def __init__(self, screen):
		#TODO: things like, start round, points, background color?
		#		chance of enemies spawning, difficulty etc.
		self.screen = screen
		self.screen_dims = screen.get_size()
		
		self.round_number = 0
		
		self.comets = []
		self.smiley_chances = []
		self.comet_images_big = []
		self.comet_images_med = []
		self.comet_images_small = []
		image_string = "pics/level"
		
		for i in range(0,2): #TODO: increase this as I make more pictures
			self.comet_images_big.append(pygame.image.load(image_string + str(i) + "b.png"))
			self.comet_images_med.append(pygame.image.load(image_string + str(i) + "m.png"))
			self.comet_images_small.append(pygame.image.load(image_string + str(i) + "s.png"))
			self.smiley_chances.append(0.0)
			

	def update(self):
		for comet in self.comets:
			comet.update()
			
		
	def blitme(self):
		for comet in self.comets:
			comet.blitme()

	def spawn_comet_children(self, comet):
		
		#TODO: I am not comfortable with using exact pixel sizes here
		new_size = 0
		new_points = 0
		image = None
		if comet.size == 65:
			new_size = 37
			new_points = 50
			image = self.comet_images_med[self.round_number]
		if comet.size == 37:
			new_size = 17
			new_points = 100
			image = self.comet_images_small[self.round_number]
			
		original_v = comet.v_moving
			

		new_comet1 = hostiles.Comet(comet.pos, self.screen, new_size,
						self, image, None, new_points) #TODO vector1
		
		new_comet2 = hostiles.Comet(comet.pos, self.screen, new_size,
						self, image, None, new_points) #TODO vector2
						
						
		self.comets.append(new_comet1)
		self.comets.append(new_comet2)


	def spawn_comets(self, amount, velocity):
		
		points = self.generate_spawn_points(amount)
		vectors = self.generate_vectors(amount)
		
		new_vectors = []
		for v in vectors:
			new_vectors.append(v*velocity)
		
		i = 0
		while i < amount: #TODO: balance these values (smiley)
			new_comet = hostiles.Comet(points[i], self.screen, 65, self,
						self.comet_images_big[self.round_number], new_vectors[i], 20)
						
						
						
			self.comets.append(new_comet)
			i += 1
			
			
			
	
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
