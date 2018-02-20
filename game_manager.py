import pygame

import ship
import game_settings as gs
import game_functions
import player_settings as ps
import hud
import hostiles
import levels


def run_game():

	settings = gs.Settings("config/settings.json")

	number_of_players = 4

	profiles = []
	for s in settings.profile_paths:
		profiles.append(ps.ProfileFileHandler.load_profile(s))

	#ps.ProfileFileHandler.save_profile("testSave",profile) #TODO this is testing stuff, remove later!
	#settings.save_settings("testsavesettings.json")
	
	#init the game window
	pygame.init()

	screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
	pygame.display.set_caption("WIP: _project") #TODO get the proper name here

	bg_color = (0,0,0) #black, background_color

	level = levels.Level(screen)
	# level 1: 9 on easy, 12 on challenging, 14 on impossible
	if settings.difficulty == 0:
		amount_of_comets = 9
	elif settings.difficulty == 1:
		amount_of_comets = 12
	elif settings.difficulty == 2:
		amount_of_comets = 14
	else:
		print("debug: settings file has unknown difficulty, defaulting to 0")
		amount_of_comets = 9
	level.spawn_comets(amount_of_comets, 0.4)

	upper_left = (settings.screen_width/4,settings.screen_height/4)
	upper_right = (3*(settings.screen_width/4),settings.screen_height/4)
	lower_left = (settings.screen_width/4,3*(settings.screen_height/4))
	lower_right = (3*(settings.screen_width/4),3*(settings.screen_height/4))
	ship_spawns = []
	if number_of_players == 1:
		ship_spawns.append((settings.screen_width/2,settings.screen_height/2))
	elif number_of_players == 2:
		ship_spawns.append(upper_left)
		ship_spawns.append(lower_right)
	elif number_of_players == 3:
		ship_spawns.append(upper_left)
		ship_spawns.append(lower_right)
		ship_spawns.append(upper_right)
	elif number_of_players == 4:
		ship_spawns.append(upper_left)
		ship_spawns.append(lower_right)
		ship_spawns.append(upper_right)
		ship_spawns.append(lower_left)

	hud_size = (156,70) #TODO these are measured values from the actual game, find a way to adjust these to screen size?
	hud_positions = [(0,0),
					 (settings.screen_width - hud_size[0], settings.screen_height - hud_size[1]),
					 (settings.screen_width-hud_size[0], 0),
					 (0, settings.screen_height-hud_size[1])]


	ships = []
	controls = []
	huds = []
	for i in list(range(0,number_of_players)):
		s = ship.Ship(ship_spawns[i],screen, 31,profiles[i].ship_props,i+1, level) #I start counting players from 1
		ships.append(s)
		controls.append(profiles[i].control_scheme)
		huds.append(hud.Hud(screen, hud_positions[i], s))

	gf = game_functions.GameFunctions(ships, controls, huds)
	clock = pygame.time.Clock()


	# Starting the main game loop
	while True:
		
		#makes the loop wait a certain amount of time to achieve 60 ticks per s
		clock.tick(60)
		
		gf.check_events()
		gf.update_screen(bg_color, screen, level)



run_game() #actually starting the game

#anything after run_game() is effectively ignored
