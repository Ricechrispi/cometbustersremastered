"""
	TODO: 	be able to choose a file to load
			reset button?
"""
import json

import ship

class ControlScheme():
	"""a class that contains the relevant button mappings"""
	
	def __init__(self, forward, left, right, shoot, special):
		self.controls = [forward,left,right,shoot,special]

	def __str__(self):
		return str(self.controls)


class PlayerProfile():
	"""a profile containter that saves ships configuration and control scheme"""

	def __init__(self, control_scheme, ship_props):
		self.control_scheme = control_scheme
		self.ship_props = ship_props
		
	#TODO: def __str__(self):

class ProfileFileHandler():
	"""a class to load and save a profile from a file, using json"""
		
	def load_profile(filename):
		with open(filename) as f_obj:
			list = json.load(f_obj)
			#TODO verify integrity of the file!
			controls = list[0]
			props = list[1]
			control_scheme = ControlScheme(controls[0],controls[1],controls[2],controls[3],controls[4])
			ship_props = ship.ShipProperties(props[0],props[1],props[2],props[3],props[4],props[5],props[6])
			return PlayerProfile(control_scheme,ship_props)

		
	def save_profile(filename, player_profile):

		list = [player_profile.control_scheme.controls, player_profile.ship_props.props]
		with open(filename, "w") as f_obj:
			json.dump(list, f_obj)

