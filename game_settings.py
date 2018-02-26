import json


class Settings:
	"""A class to store the settings of the main game"""

	def __init__(self, filename):
		with open(filename) as f_obj:
			dic = json.load(f_obj)

			self.screen_width = dic["screen_width"]
			self.screen_height = dic["screen_height"]
			self.difficulty = dic["difficulty"]

			self.fx_volume = dic["fx_volume"]
			self.fx_is_muted = dic["fx_is_muted"]
			self.music_volume = dic["music_volume"]
			self.music_is_muted = dic["music_is_muted"]

			self.profile_paths = dic["profile_paths"]

			# TODO: I am currently trusting the input values, nothing is checked!

	def toggle_fx(self):
		self.fx_is_muted = not self.fx_is_muted

	def toggle_music(self):
		self.music_is_muted = not self.music_is_muted

	def reset_all(self):
		# done by creating a new Settings object based on backup settings
		default_settings = Settings("config/backup/settings.json")
		self.screen_width = default_settings.screen_width
		self.screen_height = default_settings.screen_height

		self.difficulty = default_settings.difficulty

		self.fx_volume = default_settings.fx_volume
		self.fx_is_muted = default_settings.fx_is_muted
		self.music_volume = default_settings.music_volume
		self.music_is_muted = default_settings.music_is_muted

	def save_settings(self, filename):
		s = {
			"screen_width": self.screen_width,
			"screen_height": self.screen_height,
			"difficulty": self.difficulty,
			"fx_volume": self.fx_volume,
			"fx_is_muted":  self.fx_is_muted,
			"music_volume":  self.music_volume,
			"music_is_muted": self.music_is_muted,
			"profile_paths":  self.profile_paths,
		}

		with open(filename, "w") as f_obj:
			json.dump(s, f_obj)

	def __str__(self):
		return "res: " + str(self.screen_width) + "x" + str(self.screen_height) + ", dif: " + str(self.difficulty) + \
			   ", fx_v: " + str(self.fx_volume) + ", fx_muted: " + str(self.fx_is_muted) + \
			   ", music_v: " + str(self.music_volume) + ", music_muted: " + str(self.music_is_muted) + \
			   ", paths: " + ",".join(self.profile_paths)
