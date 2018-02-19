"""
	TODO: 	be able to choose a file to load
			reset button?
"""
import json

import ship

class ControlScheme:
	"""a class that contains the relevant button mappings"""
	
	def __init__(self, forward, left, right, shoot, special):
		self.controls = [forward,left,right,shoot,special]

	def __str__(self):
		return str(self.controls)


class PlayerProfile:
	"""a profile containter that saves ships configuration and control scheme"""

	def __init__(self, control_scheme, ship_props):
		self.control_scheme = control_scheme
		self.ship_props = ship_props
		
	def __str__(self):
		return str(self.control_scheme)+", "+str(self.ship_props)

class ProfileFileHandler:
	"""a class to load and save a profile from a file, using json"""
		
	def load_profile(filename):
		with open(filename) as f_obj:
			args = json.load(f_obj)
			#TODO verify integrity of the file!
			controls = args[0]
			props = args[1]
			control_scheme = ControlScheme(controls[0],controls[1],controls[2],controls[3],controls[4])
			ship_props = ship.ShipProperties(props[0],props[1],props[2],props[3],props[4],props[5],props[6])
			return PlayerProfile(control_scheme,ship_props)

		
	def save_profile(filename, player_profile):

		p = [player_profile.control_scheme.controls, player_profile.ship_props.props]
		with open(filename, "w") as f_obj:
			json.dump(p, f_obj)

