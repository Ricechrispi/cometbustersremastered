import sys

import pygame

class GameFunctions():

	def __init__(self,ships,control_list):
		self.ships = ships
		self.control_list = control_list
		#TODO we kinda rely on these two lists having the same length, and ok contents..

	def check_events(self):
		"""this responds to keypresses and other events"""

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				sys.exit() #if the game is closed by pressing the X

			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

				if event.key == pygame.K_ESCAPE: #TODO maybe remove this, escape closes the game
					sys.exit()

				for i in list(range(0,len(self.control_list))):
					if event.key in self.control_list[i].controls:
						if event.type == pygame.KEYDOWN:
							print("debug: key pressed: " + str(event.key))
							self.check_keydown_events(event, self.ships[i], self.control_list[i].controls)
						elif event.type == pygame.KEYUP:
							self.check_keyup_events(event, self.ships[i], self.control_list[i].controls)


	def check_keydown_events(self, event, ship, controls):

		if event.key == controls[0]:
			ship.b_thrusting = True
		elif event.key == controls[1]:
			#starting to rotate left stops rotating right
			ship.b_rotating_right = False
			ship.b_rotating_left = True
		elif event.key == controls[2]:
			#starting to rotate right stops rotating left
			ship.b_rotating_right = True
			ship.b_rotating_left = False
		elif event.key == controls[3]:
			ship.weapon.shoot()
		elif event.key == controls[4]:
			#TODO call special here!
			pass


		#TODO: same as other function above
	def check_keyup_events(self, event, ship, controls):
		if event.key == controls[0]:
			ship.b_thrusting = False
		elif event.key == controls[1]:
			ship.b_rotating_left = False
		elif event.key == controls[2]:
			ship.b_rotating_right = False
		elif event.key == controls[4]:
			#TODO call undo special here!
			pass




	def update_screen(self, bg_color, screen, level):

		screen.fill(bg_color) #filling the background with a color

		level.update()
		level.blitme()

		for ship in self.ships:
			ship.update()
			ship.blitme()

		pygame.display.flip() #makes the most recently drawn frame/screen visible


	#note: this is basically the same as creating a new GameFunctions object..
	def refresh_settings(self, ships, control_list):
		if (len(ships) == len(control_list)):
			self.ships = ships
			self.control_list = control_list
		else:
			print("error while refreshing settings!") #TODO log and react?
