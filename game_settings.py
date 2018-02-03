class Settings():
	"""A class to store the settings of the main game"""
	
	def __init__(self, resolution=(1280,720), difficulty=0, fx_volume=100, music_volume=100): 
		#TODO: add the other options here, all of them with default values!!
		#TODO: I am currently trusting the input values, nothing is checked!
		
		#Screen settings:
		self.screen_width = resolution[0] #e.g. 1920
		self.screen_height = resolution[1] #e.g. 1080
		
		self.difficulty = difficulty #0 is easy, 1 is normal, 2 is hard etc.
		
		self.fx_volume = fx_volume #from 0-100
		self.old_fx_volume = fx_volume
		self.fx_is_muted = False
		self.music_volume = music_volume #from 0-100
		self.old_music_volume = music_volume
		self.music_is_muted = False
		
	
	def toggle_fx(self):
		if self.fx_is_muted:
			self.fx_is_muted = False
			self.fx_volume = self.old_fx_volume
		else:
			self.fx_is_muted = True
			self.old_fx_volume = self.fx_volume
			self.fx_volume = 0
	
	def toggle_music(self):
		#TODO: either copy the toggle_fx code or come up with better solution
		print("This is not done yet, @toggle_music")


	def reset_all(self):
		"""method to reset all values to the defaults"""
		
		#easily done by creating a new Settings object and getting it's defaults
		default_settings = Settings()
		self.screen_width = default_settings.screen_width
		self.screen_height = default_settings.screen_height
		
		self.difficulty = default_settings.difficulty
		
		self.fx_volume = default_settings.fx_volume
		self.old_fx_volume = self.fx_volume
		self.fx_is_muted = False
		self.music_volume = default_settings.music_volume
		self.old_music_volume = self.music_volume
		self.music_is_muted = False
		
		#TODO: add additional values here if they are added
	#TODO: def __str__(self):
