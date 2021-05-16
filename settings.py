import os

version = 1.30
development_stage = "DEV"
app_name = "NOVA HUB V{} ({})".format(version, development_stage)

#Be careful when changing the locations. If you type a false location the auto updater will stop functioning.
api = "http://192.168.1.176"
nova_hub_json_location = "/files/nova_hub.json" #Where the json file is stored on the webserver.
nova_hub_update_package_location = "/files/update.zip" #Where the update package is stored on the webserver.
mod_pack_installers_location = "/files/installers" #Web directory where the modpack installers will be located.

nova_universe_url = "https://www.youtube.com/c/TheGoldenPro" #Change this to novauniverse website domain.

#Paths
appdata_dir = "C:" + (os.path.join(os.environ["HOMEPATH"], "AppData\\Roaming"))
path_to_appdata_folder = f"{appdata_dir}\\.NovaUniverse"
path_to_minecraft_folder = f"{appdata_dir}\\.minecraft"

path_to_mc_versions_folder = f"{path_to_minecraft_folder}\\versions"
path_to_terra_smp_folder = f"{path_to_appdata_folder}\\TerraSMP"
path_to_mods_folder = f"{path_to_terra_smp_folder}\\mods"
path_to_mc_launcher_exe = "C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe"

path_to_logs = "logs\\"
path_to_installers = "installers\\"
path_to_images = "assets\\"
path_to_assets = path_to_images
temp_folder_path = "temp\\"
path_to_old_forge_folder = "old_forge\\"

button_list = []