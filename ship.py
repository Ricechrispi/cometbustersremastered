import pygame
import numpy as np
import math

import utility_functions as util
from weapon import Weapon
from movable import Movable

class ShipProperties():
	"""container class to hold all the properties"""
	
	def __init__(self, color, f_bullet_speed, f_thrust, 
					f_max_speed, f_rot_speed, 
					f_special, special_type=None):
		check_bool = self.check_values(f_bullet_speed, f_thrust, f_max_speed, f_rot_speed,
						f_special, special_type)
		#print("the values check returns: " + str(check_bool)) # TODO move this, and/or hide it
		self.color = color	#TODO make this an actual color, and check it
		self.f_bullet_speed = f_bullet_speed
		self.f_thrust = f_thrust
		self.f_max_speed = f_max_speed
		self.f_rot_speed = f_rot_speed
		self.f_special = f_special
		self.special_type = special_type

		self.props = [color,f_bullet_speed,f_thrust,f_max_speed,f_rot_speed,f_special,special_type]
		
		
	def check_values(self, bs, th, ms, rs, sp, st): #TODO color?
		float_flag = True
		try:
			bs = float(bs)
			th = float(th)
			ms = float(ms)
			rs = float(rs)
			sp = float(sp)
		except ValueError:
			float_flag = False
		else:
			f_sum = (bs + th + ms + rs + sp)
			float_flag = f_sum >= 2.45 and f_sum <= 2.55 #this is for balance
		type_flag = st in [None, "hyperspace", "shields", "disruptor"]
		return float_flag and type_flag
		
		
	def __str__(self):	#this way we can get this by calling str()
		"""to easily display all stats"""
		return ("ShipProperties: \nColor: " + str(self.color)
					+ "\nBullet speed: " + str(self.f_bullet_speed)
					+ "\nThrust: " + str(self.f_thrust)
					+ "\nMaximum speed: " + str(self.f_max_speed)
					+ "\nRotation speed: " + str(self.f_rot_speed)
					+ "\nSpecial ability: " + str(self.f_special)
					+ "\nSpecial Type: " + str(self.special_type))
			
		

class Ship(Movable):
	"""The player controlled ship"""
	
	def __init__(self, pos, screen, size, props, player_number):	
		super().__init__(pos, screen, size)

		#TODO: balance these!
		self.f_drag = 0.995
		self.base_speed = 4.0 
		self.base_rot = 1.2
		self.base_bullet_speed = 1.0
		self.base_shield = 1.0
		self.base_disruptor = 1.0
		self.base_hyperspace = 1.0
		
		self.props = props
		self.player_number = player_number
		#TODO the values are unchecked

		image_name = "pics/"+props.color+".png"
		self.image = pygame.image.load(image_name) #TODO: subject to change!
		
		#bools for moving by input
		self.b_rotating_right = False
		self.b_rotating_left = False
		self.b_thrusting = False
		
		self.b_is_shooting = False
		self.b_using_special = False
		
		#TODO: balance hp and size here!
		self.weapon = Weapon(self, 5, 160, 13, "pics/bullet_dummy.png", "TODO:soundfile")
		


	def blitme_impl(self):
		"""drawing the current ship ()and it's bullets via the weapon)"""
		
		self.weapon.blitme() #drawing projectiles before, so ship is on top

		angle = math.degrees(math.acos(np.dot(np.array([0.0, -1.0]), self.v_facing)))

		if self.v_facing[0] > 0:
			angle = -angle

		rotated_img_rect = util.rot_center(self.image, self.rect, angle)

		self.screen.blit(rotated_img_rect[0], rotated_img_rect[1]) #TODO: add color from properties
		
		
	def update_impl(self):
		"""updating the thrust/rotation of the ship based on pressed keys
			and velocity"""
			
		self.weapon.update()

		if self.b_rotating_left and self.b_rotating_right:
			pass #both cancel each other out, but this should not really happen

		elif self.b_rotating_left:

			angle = self.base_rot * self.props.f_rot_speed
			self.v_facing = util.rotate_v(self.v_facing, -angle, True)
			#notice the '-' for rotating the other way

		elif self.b_rotating_right:

			angle = self.base_rot * self.props.f_rot_speed
			self.v_facing = util.rotate_v(self.v_facing, angle, True)

		if self.b_thrusting:
			#TODO: check and balance this

			added_thrust = self.v_facing * self.props.f_thrust
			#print("added thrust: " + str(added_thrust))

			self.v_moving += added_thrust

			current_speed = util.mag_v(self.v_moving)
			max_speed = self.base_speed * self.props.f_max_speed

			if current_speed > max_speed:
				self.v_moving = (self.v_moving / current_speed) * max_speed
			
				

	#TODO def ___str__(self):	
