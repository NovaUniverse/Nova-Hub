import os
import sys
import json
from nova_func import print_and_log

class Nova_Dir:
	@staticmethod
	def get_terra_smp_directory():
		platform = sys.platform 

		if platform == "win32":
			return os.getenv('APPDATA') + "\\.NovaUniverse\\TerraSMP"
		elif platform == "linux":
			return os.getenv("HOME") + "/.NovaUniverse/TerraSMP"
		else:
			return None

	@staticmethod
	def get_nova_universe_directory():
		platform = sys.platform 

		if platform == "win32":
			return os.getenv('APPDATA') + "\\.NovaUniverse"
		elif platform == "linux":
			return os.getenv("HOME") + "/.NovaUniverse"
		else:
			return None

	@staticmethod
	def get_appdata_directory():
		platform = sys.platform 

		if platform == "win32":
			return os.getenv('APPDATA')
		elif platform == "linux":
			return os.getenv("HOME")
		else:
			return None

	@staticmethod
	def get_mc_game_directory():
		platform = sys.platform

		path = Nova_Dir.get_nova_universe_directory()
		with open(path + "\\#.nova_hub\\user_settings.json", "r") as f:
			user_settings_json = json.load(f)

		if not user_settings_json["paths"][".mc_path"] == None: #For Players that dump .minecraft in a different directory.
			custom_path = user_settings_json["paths"][".mc_path"]
			return custom_path

		if platform == "win32":
			return os.getenv('APPDATA') + "\\.minecraft"
		elif platform == "linux":
			return os.getenv("HOME") + "/.minecraft"
		else:
			return None

	@staticmethod
	def get_mc_launcher_directory():
		platform = sys.platform

		path = Nova_Dir.get_nova_universe_directory()
		with open(path + "\\#.nova_hub\\user_settings.json", "r") as f:
			user_settings_json = json.load(f)

		if not user_settings_json["paths"]["mc_launcher_exe_path"] == None: #For Players that installed minecraft launcher in a different directory.
			custom_path = user_settings_json["paths"]["mc_launcher_exe_path"]
			return custom_path

		if platform == "win32":
			return os.getenv('PROGRAMFILES(X86)') + "\\Minecraft Launcher\\MinecraftLauncher.exe"
		elif platform == "linux":
			return os.getenv("HOME") + "/.minecraft"
		else:
			return None

	@staticmethod
	def get_programs_folder():
		platform = sys.platform

		if platform == "win32":
			return os.getenv('PROGRAMFILES')
		elif platform == "linux":
			return os.getenv("HOME")
		else:
			return None

	@staticmethod
	def is_supported():
		return Nova_Dir.get_nova_universe_directory() != None

#Open user_settings.json
path = Nova_Dir.get_nova_universe_directory()
try:
	with open(path + "\\#.nova_hub\\user_settings.json", "r") as f:
		user_settings_json = json.load(f)

	print_and_log("INFO", "Nova Hub user settings loaded. \n")

except FileNotFoundError as e:
	pass

#arabic nokia car drip - https://youtu.be/C8N-XudEKuc