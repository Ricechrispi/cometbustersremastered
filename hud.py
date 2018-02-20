import pygame

class Hud:

	def __init__(self, screen, pos, ship):
		self.screen = screen
		self.pos = pos
		self.ship = ship

		self.image = pygame.image.load("pics/numbers.png")

		#these cropped_rects are the parts from the picture to be drawn
		self.cropped_rects = []
		for i in list(range(0,12)):
			offset = i * 17
			self.cropped_rects.append((0,offset,14,17))

		#these digit_rects are the position of each digit
		self.digit_rects = []
		d_offset = 0
		x_offset = 31 #measured from the original game
		y_offset = 18
		for i in list(range(0,7)):
			self.digit_rects.append(pygame.Rect(pos[0]+x_offset+d_offset, pos[1]+y_offset,
												pos[0]+x_offset+d_offset+14, pos[1]+y_offset+17))
			d_offset += 14


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

		#pics/life_x.png is 15x15
		#5px between lives
		#8px under score, 5px to the right from far left digit
		#most right vanishes


		pass #TODO in the right color

	def draw_box(self):
		pass #TODO maybe an outlying box around the stuff, not that important

