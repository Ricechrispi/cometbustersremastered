import sys
import pygame

class UserInterface:

	def __init__(self, screen):

		self.chosen_number_of_players = -1
		self.buttons = []

		# TODO adjust these values
		button_height = 60
		button_width = 200
		button_pos = (screen.get_rect().center[0], 200)
		button_font = pygame.font.SysFont("arial", 30, True)  # TODO size?
		button_text_color =  (255, 32, 128)
		button_background_color =  (60, 76, 102)
		offset = 0
		space_between_buttons = 10

		for i in list(range(1,5)):
			if i == 1:
				s = "Single Player"
			else:
				s = str(i) + " Players"
			player_button = PlayerSelectButton(screen, button_width, button_height,
											   (button_pos[0], button_pos[1]+offset), button_font, s,
											   button_text_color, button_background_color, self, i)

			offset += button_height + space_between_buttons
			self.buttons.append(player_button)

		settings_button = SettingsButton(screen, button_width, button_height, (button_pos[0], button_pos[1]+offset),
									  button_font, "Settings", button_text_color, button_background_color, self)
		offset += button_height + space_between_buttons
		self.buttons.append(settings_button)

		exit_button = ExitButton(screen, button_width, button_height, (button_pos[0], button_pos[1]+offset),
									  button_font, "Exit", button_text_color, button_background_color, self)
		offset += button_height + space_between_buttons
		self.buttons.append(exit_button)



	def update(self):
		self.check_events()

	def check_events(self):
		"""this responds to keypresses and other events"""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()  # if the game is closed by pressing the X

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				self.check_button_collision(mouse_x,mouse_y)

			elif event.type == pygame.MOUSEMOTION:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				self.check_button_hover(mouse_x,mouse_y)


	def blitme(self):
		for button in self.buttons:
			button.blitme()

	def check_button_collision(self, mouse_x, mouse_y):
		for button in self.buttons:
			if button.rect.collidepoint(mouse_x,mouse_y):
				button.click()

	def check_button_hover(self, mouse_x, mouse_y):
		for button in self.buttons:
			if button.rect.collidepoint(mouse_x,mouse_y):
				button.is_hovered = True
			else:
				button.is_hovered = False

class Button:

	def __init__(self, screen, width, height, pos, font, text, text_color, background_color, user_interface):

		self.screen = screen

		self.width = width
		self.height = height
		self.font = font
		self.text_color = text_color
		hover_factor = 0.25 #the higher this is the lighter the hover color gets
		self.hover_text_color = (text_color[0] + int((255-text_color[0])*hover_factor),
								 text_color[1] + int((255-text_color[1])*hover_factor),
								 text_color[2] + int((255-text_color[2])*hover_factor))
		self.background_color = background_color
		self.hover_background_color = (background_color[0] + int((255-background_color[0])*hover_factor),
									   background_color[1] + int((255-background_color[1])*hover_factor),
									   background_color[2] + int((255-background_color[2])*hover_factor))

		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.center = pos #(x,y)

		self.image = self.font.render(text, True, self.text_color, self.background_color)
		self.image_rect = self.image.get_rect()
		self.hover_image = self.font.render(text, True, self.hover_text_color, self.hover_background_color)
		self.image_rect.center = self.rect.center

		self.is_hovered = False

		self.user_interface = user_interface


	def click(self):
		print("button clicked, this should be overridden!")

	def blitme(self):
		if self.is_hovered:
			#self.screen.fill(self.hover_background_color, self.rect)
			self.fill_roundedRect(self.rect,self.hover_background_color)
			self.screen.blit(self.hover_image, self.image_rect)
		else:
			#self.screen.fill(self.background_color, self.rect)
			self.fill_roundedRect(self.rect,self.background_color)
			self.screen.blit(self.image, self.image_rect)


	#copied from https://pastebin.com/wL3ZWxEu
	#only made minor adjustments
	def fill_roundedRect(self, rect, color, radius=0.4):
		""" Draw a rounded rectangle """
		rect = pygame.Rect(rect)
		color = pygame.Color(*color)
		alpha = color.a
		color.a = 0
		pos = rect.topleft
		rect.topleft = 0, 0
		rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

		circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
		pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
		circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

		radius = rectangle.blit(circle, (0, 0))
		radius.bottomright = rect.bottomright
		rectangle.blit(circle, radius)
		radius.topright = rect.topright
		rectangle.blit(circle, radius)
		radius.bottomleft = rect.bottomleft
		rectangle.blit(circle, radius)

		rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
		rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

		rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
		rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

		return self.screen.blit(rectangle, pos)


class PlayerSelectButton(Button):

	def __init__(self, screen, width, height, pos, font, text, text_color, background_color, user_interface,
				 number_of_players):
		super().__init__(screen, width, height, pos, font, text, text_color, background_color, user_interface)
		self.number_of_players = number_of_players

	def click(self):
		self.user_interface.chosen_number_of_players = self.number_of_players


class SettingsButton(Button):

	def __init__(self, screen, width, height, pos, font, text, text_color, background_color, user_interface):
		super().__init__(screen, width, height, pos, font, text, text_color, background_color, user_interface)

	def click(self):
		print("implement this shit") #TODO this
		# ps.ProfileFileHandler.save_profile("testSave",profile)
		# settings.save_settings("testsavesettings.json")


class ExitButton(Button):

	def __init__(self, screen, width, height, pos, font, text, text_color, background_color, user_interface):
		super().__init__(screen, width, height, pos, font, text, text_color, background_color, user_interface)

	def click(self):
		sys.exit()