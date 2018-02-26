import pygame
import utility_functions as util

class Hud:

	def __init__(self, screen, pos, ship):
		self.screen = screen
		self.pos = pos
		self.ship = ship

		self.image = pygame.image.load("pics/numbers.png")

		#these cropped_rects are the parts from the picture to be drawn
		self.cropped_rects = util.cropped_image_rects(14,17,12)

		#these digit_rects are the position of each digit
		self.digit_rects = []
		d_offset = 0
		x_offset = 31 #measured from the original game
		y_offset = 18
		for i in list(range(0,7)):
			self.digit_rects.append(pygame.Rect(pos[0]+x_offset+d_offset, pos[1]+y_offset,
												pos[0]+x_offset+d_offset+14, pos[1]+y_offset+17))
			d_offset += 14


		self.life_image = pygame.image.load("pics/life_" + ship.props.color + ".png")
		self.life_rects = []
		l_offset = 5 #starts at 5 to the right of the first image
		for i in list(range(0, 5)): #max of 5 lives? TODO check this later and prevent 6 lives?
			self.life_rects.append(pygame.Rect(pos[0]+x_offset+l_offset, pos[1]+y_offset+8+17, #8 + 17 since it's 8px under the 17px score digit
											   pos[0]+x_offset+l_offset+15, pos[1]+y_offset+8+15)) #15 since image is 15x15
			l_offset += 20 #15 width image + 5 px between images

		#pics/life_x.png is 15x15
		#5px between lives
		#8px under score, 5px to the right from far left digit


	def blitme(self):
		self.draw_box()
		self.draw_lives()
		self.draw_score()

	def draw_score(self):

		digits = self.number_to_digits(self.ship.score)
		for i in list(range(0,len(digits))):
			self.draw_digit(digits[i], self.digit_rects[i])

	def draw_digit(self, digit, rect):

		if digit > 9:
			print("debug: digit > 9 was passed, reducing to 9, FIX THIS")
			digit = 9

		self.screen.blit(self.image, rect, self.cropped_rects[digit])

	def number_to_digits(self, number):

		#TODO is string conversion easier/faster?
		ret = []
		for d in self.digit_rects:
			ret.append(0)

		i = len(ret) -1
		while number > 0 and i >= 0:
			ret[i] = int(number % 10)
			number /= 10
			i -= 1

		return ret

	def draw_lives(self):

		#TODO most right vanishes
		for i in list(range(0, self.ship.lives)):
			self.screen.blit(self.life_image, self.life_rects[i])


	def draw_box(self):
		pass #TODO maybe an outlying box around the stuff, not that important, not in original

