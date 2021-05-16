import os
import sys

class GameDirectoryFinder:
	@staticmethod
	def get_game_directory():
		platform = sys.platform 

		if platform == "win32":
			return os.getenv('APPDATA') + "\\.NovaUniverse\\TerraSMP"
		elif platform == "linux":
			return os.getenv("HOME") + "/.NovaUniverse/TerraSMP"
		else:
			return None

	@staticmethod
	def get_mc_game_directory():
		platform = sys.platform 

		if platform == "win32":
			return os.getenv('APPDATA') + "\\.minecraft"
		elif platform == "linux":
			return os.getenv("HOME") + "/.minecraft"
		else:
			return None

	@staticmethod
	def is_supported():
		return GameDirectoryFinder.get_game_directory() != None