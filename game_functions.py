import sys

import pygame

class GameFunctions():

	def __init__(self,ships,control_list, huds, screen, level):
		self.ships = ships
		self.control_list = control_list
		self.huds = huds
		#TODO we kinda rely on these three lists having the same length, and ok contents..

		self.screen = screen
		self.level = level

		self.game_has_ended = False

		self.font1 = pygame.font.SysFont("arial", 70, True) #TODO size?
		self.label = self.render_label("LEVEL 1")
		self.label_pos = (self.screen.get_rect().center[0], int(self.screen.get_rect().height/4))

		self.round_in_progress = False
		self.round_number = -1
		self.round_cooldown = 180 #TODO adjust
		self.cur_cooldown = self.round_cooldown

	def game_loop(self):
		self.check_events()
		self.update()
		self.draw_screen()

	def render_label(self, s):
		#TODO shadow: https://stackoverflow.com/questions/18974194/text-shadow-with-python
		return self.font1.render(s, True, (255,32, 128))

	def check_events(self):
		"""this responds to keypresses and other events"""

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				sys.exit() #if the game is closed by pressing the X

			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				#print("debug: key pressed: " + str(event.key))
				for i in list(range(0,len(self.control_list))):
					if event.key in self.control_list[i].controls:
						if event.type == pygame.KEYDOWN:
							self.check_keydown_events(event, self.ships[i], self.control_list[i].controls)
						else: #must be KEYUP
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


	def start_round(self):
		print("debug: round starts")
		self.round_in_progress = True
		self.round_number += 1
		self.level.spawn_comets(self.level.amount_of_comets, 0.4, self.round_number) #TODO adjust starting speed here
		self.label = None


	def end_round(self):
		print("debug: round ended, setting cooldown")
		#TODO stuff, display, points?
		self.round_in_progress = False
		self.cur_cooldown = self.round_cooldown
		self.label = self.render_label("LEVEL "+str(self.round_number+1))


	def update(self):

		if len(self.level.comets) == 0:
			if not self.round_in_progress: #round is not in progress and there are no comets!
				if self.cur_cooldown == 0:
					self.start_round()
				else:
					self.cur_cooldown -= 1
			else: #round is in progress and there are no comets!
				self.end_round()

		self.level.update()

		for ship in self.ships:
			ship.update()


	def draw_screen(self):

		self.screen.fill((0,0,0)) #filling the background with black

		for h in self.huds:
			h.blitme()

		self.level.blitme()

		for ship in self.ships:
			ship.blitme()

		if self.label is not None:
			self.screen.blit(self.label, (int(self.label_pos[0]-self.label.get_rect().width/2),self.label_pos[1]))



	#note: this is basically the same as creating a new GameFunctions object..
	def refresh_settings(self, ships, control_list):
		if len(ships) == len(control_list):
			self.ships = ships
			self.control_list = control_list
		else:
			print("error while refreshing settings!") #TODO log and react?
