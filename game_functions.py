import sys

import pygame


def check_events(ships):
	"""this responds to keypresses and other events"""
	
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit() #if the game is closed by pressing the X
				
			#TODO: have this somehow check for the player defined buttons
			# and also update all the ships, including shooting and special
		elif event.type == pygame.KEYDOWN:
			
			#TODO: if event.key in ship[x].control_scheme, then check_keydown_events etc.
			#		somehow load this in gamemangaer, read from json
			check_keydown_events(event, ships[0])
				
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ships[0])
			
			
					
	#TODO: the ships parameter here has to be replaced at some point!
	#TODO: also custom keybinds etc.
def check_keydown_events(event, ship):
	if event.key == pygame.K_RIGHT:
		#starting to rotate right stops rotating left
		ship.b_rotating_right = True
		ship.b_rotating_left = False
		
	elif event.key == pygame.K_LEFT:
		#starting to rotate left stops rotating right
		ship.b_rotating_right = False
		ship.b_rotating_left = True
		
	elif event.key == pygame.K_UP:
		ship.b_thrusting = True
			
	elif event.key == pygame.K_SPACE:
		ship.weapon.shoot()
		
	elif event.key == pygame.K_ESCAPE:
		sys.exit() #TODO: remove this, only for debugging faster
					
					
	#TODO: same as other function above
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.b_rotating_right = False
		
	elif event.key == pygame.K_LEFT:
		ship.b_rotating_left = False
		
	elif event.key == pygame.K_UP:
		ship.b_thrusting = False
		
				

def update_screen(bg_color, screen, ships, level):
	
	screen.fill(bg_color) #filling the background with a color		
	
	level.update()
	level.blitme()
	
	for ship in ships:
		ship.update()
		ship.blitme()
			
	pygame.display.flip() #makes the most recently drawn frame/screen visible
