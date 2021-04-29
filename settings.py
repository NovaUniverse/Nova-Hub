import os

version = 1.00
development_stage = "DEV"
app_name = "NOVA HUB V{} ({})".format(version, development_stage)

nova_universe_url = "https://www.youtube.com/c/TheGoldenPro"

forge_ver_name = "1.12.2-forge-14.23.5.2854"

forge_1_12_2_identifiers = ["1.12.2-forge-", "forge-1.12.2-", "1.12.2-forge1"]

#Paths
appdata_dir = "C:" + (os.path.join(os.environ["HOMEPATH"], "AppData\\Roaming"))
path_to_appdata_folder = f"{appdata_dir}\\.NovaUniverse"
path_to_mc_versions_folder = f"{appdata_dir}\\.minecraft\\versions"
path_to_terra_smp_folder = f"{path_to_appdata_folder}\\TerraSMP"
path_to_mods_folder = f"{path_to_terra_smp_folder}\\mods"
path_to_mc_launcher_exe = "C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe"


path_to_logs = "logs\\"
path_to_installers = "installers\\"
path_to_images = "images\\"
temp_folder_path = "temp\\"
path_to_old_forge_folder = "old_forge\\"

button_list = []