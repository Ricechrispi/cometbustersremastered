"""
	TODO: 	read and load with json!
			maybe even be able to choose a file to load
			maybe make a class with like 'forwad = "w"' etc.
			things like ShipProperties, (color, floats..)
			things like keybindings
			reset button?
	
"""
import json

import ship

class ControlScheme():
	"""a class that containts the relevant button mappings"""
	
	def __init__(self, forward, left, right, shoot, special):
		#TODO: do is save these things as strings?
		
		self.forwad = forwad
		self.left = left
		self.right = right
		self.shoot = shoot
		self.special = special
		
	#TODO: def __str__(self):


class PlayerProfile():
	"""a profile containter that saves ships configuration and control scheme"""
	
	
	def __init__(self, control_scheme, ship_props):
		self.control_scheme = control_scheme
		self.ship_props = ship_props
		
	#TODO: def __str__(self):

class ProfileFileHandler():
	"""a class to load and save a profile from a file, using json"""
	
	def __init__(self):
		pass #TODO implement?
		
	def load_profile(self, filename, slot_number):
		pass #TODO implement!
		
	def save_profile(self, filename, player_profile):
		pass #TODO implement!
