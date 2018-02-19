import json


class Settings:
	"""A class to store the settings of the main game"""

	def __init__(self, filename):
		with open(filename) as f_obj:
			args = json.load(f_obj)

			# TODO: add the other options here, all of them with default values!!
			# TODO: I am currently trusting the input values, nothing is checked!

			# Screen settings:
			self.screen_width = args[0][0]  # e.g. 1920
			self.screen_height = args[0][1]  # e.g. 1080

			self.difficulty = args[1]  # 0 is easy, 1 is normal, 2 is hard etc.

			self.fx_volume = args[2]  # from 0-100
			self.fx_is_muted = args[3]
			self.music_volume = args[4]  # from 0-100
			self.music_is_muted = args[5]
			self.profile_paths = args[6]

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
		s = [[self.screen_width, self.screen_height], self.difficulty, self.fx_volume, self.fx_is_muted,
			 self.music_volume, self.music_is_muted, self.profile_paths]
		with open(filename, "w") as f_obj:
			json.dump(s, f_obj)

	def __str__(self):
		return "res: " + str(self.screen_width) + "x" + str(self.screen_height) + ", dif: " + str(self.difficulty) + \
			   ", fx_v: " + str(self.fx_volume) + ", fx_muted: " + str(self.fx_is_muted) + \
			   ", music_v: " + str(self.music_volume) + ", music_muted: " + str(self.music_is_muted) + \
			   ", paths: " + ",".join(self.profile_paths)
