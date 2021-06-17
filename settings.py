import os

version = 1.01
development_stage = "ALPHA"
app_name = "NOVA HUB V{} ({})".format(version, development_stage)

#Be careful when changing the locations. If you type a false location the auto updater will stop functioning.
option = None
api_mode = "prod"
try:
    import sys
    option = sys.argv[2] #Grab command line arg
except IndexError as e:
    pass

if not option == None:
    if option.lower() == "dev":
        api_mode = "dev"
        print("DEV MODE HURRAY!!!")
        import ctypes
        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 3)

if api_mode == "dev":
    ip = "https://nhcdn.novauniverse.net/"
    api = ip + "dev/nova_hub"

if api_mode == "prod":
    ip = "https://nhcdn.novauniverse.net/"
    api = ip + "prod/nova_hub"

#ip = "http://192.168.1.176/"
#api = ip + "files/nova_hub"

nova_hub_json_location = "/nova_hub.json" #Where the json file is stored on the webserver.
nova_hub_update_package_location = "/update.zip" #Where the update package is stored on the webserver.
mod_pack_installers_location = "/installers" #Web directory where the modpack installers will be located.
nova_hub_modpack_location = "/mod_packs"
user_settings_json_template_location = "/user_settings_template.json"
updater_script_location = "/updater_script.zip"

nova_universe_url = "https://novauniverse.net/" #Change this to novauniverse website domain.

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