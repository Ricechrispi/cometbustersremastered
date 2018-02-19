import pygame
import json

import ship
import game_settings as gs
import game_functions
import player_settings as ps
import hostiles
import levels


def run_game():

	profile = ps.ProfileFileHandler.load_profile("./config/p1.json")
	ps.ProfileFileHandler.save_profile("testSave",profile) #TODO this is testing stuff, remove later!
	
	#init the game window
	pygame.init()
	
	#TODO: load a settings file (json) here instead
	settings = gs.Settings() #loading the defaults
	
	screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
	pygame.display.set_caption("WIP: _project") #TODO get the proper name here

	bg_color = (0,0,0) #black, background_color
	
	test_ship_props = profile.ship_props
	test_ship_controls = profile.control_scheme
	test_ship = ship.Ship((640,360), screen, 31, test_ship_props, 1)

	#ships = pygame.sprite.Group()
	#ships.add(test_ship)
	ships = [test_ship] #TODO: sprite.Group() allows for more functions, but game_functions needs a list for now... CHANGE GAME_FUNCTIONS KEYDOWN STUFF
	controls = [test_ship_controls] #TODO make this a list of all the ships/controls later
	gf = game_functions.GameFunctions(ships,controls)
	clock = pygame.time.Clock()
	
	level = levels.Level(screen)
	level.spawn_comets(9, 0.4)
	#level 1: 9 on easy, 12 on challengeing, 14 on impossible
	#

	# Starting the main game loop
	while True:
		
		#makes the loop wait a certain amount of time to achieve 60 ticks per s
		clock.tick(60) 
		
		gf.check_events()
		gf.update_screen(bg_color, screen, level)
		

run_game() #actually starting the game

#anything after run_game() is effectively ignored
