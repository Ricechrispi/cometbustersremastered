import numpy as np
import pygame
import math

def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect
	
	
def rotate_v(v, angle, fix_to_one=False):
	"""rotate a 2-dim vector around (0,0) for the given angle in deg."""
	#fix_to_one makes sure the resulting vector has length of 1.0
	#positive is clockwise
	cosphi = math.cos(math.radians(angle))
	sinphi = math.sin(math.radians(angle))
	
	new_vector = np.array([v[0]*cosphi - v[1]*sinphi, 
					v[0]*sinphi + v[1]*cosphi])
	
	if fix_to_one:
		return new_vector / mag_v(new_vector)
	else:
		return new_vector
	
	
def mag_v(v):
	"""returns the magnitude of a 2-dim vector"""
	return math.sqrt(v[0]**2 + v[1]**2)


def cropped_image_rects(width, height, number_of_parts):
	"""creates rects to draw parts of an image"""
	ret = []
	for i in list(range(0, number_of_parts)):
		offset = i * height
		ret.append((0, offset, width, height))
	return ret