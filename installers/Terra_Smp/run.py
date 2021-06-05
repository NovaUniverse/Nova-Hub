import os
import urllib
from datetime import date
import time
import urllib.request
from zipfile import ZipFile
import sys
import shutil
import requests
import stat
import subprocess

script_name = "TERRA SMP : SCRIPT"
modpack_code_name = "terra_smp"

#Try using Nova Hub's function file first. (Only works if running script from Nova Hub.)
try:
    sys.path.append(os.path.abspath(os.path.join('..','..', 'nova_func')))

    from nova_func import *
    print_and_log("info", f"[{script_name}] Using functions from Nova Hub.")

except ImportError: #If error import function file from root if avalible.
    import nova_func
    from nova_func import *
    print_and_log("warn", "The script failed to use functions from Nova Hub so it's using it's own temporary functions now.\n(Runing the script alone without Nova Hub is not recommended as they may be bugs and we won't be able to remotely fix those bugs.)")

#Try using Nova Hub's nova_dir file first. (Only works if running script from Nova Hub.)
try:
    sys.path.append(os.path.abspath(os.path.join('..','..', 'nova_dir')))
    from nova_dir import *
    print_and_log("info", f"[{script_name}] Using nova_dir from Nova Hub.")
    print_and_log()

except ImportError:
    import nova_dir
    from nova_dir import *
    print_and_log("warn", "The script failed to import nova_dir from Nova Hub so it's using it's own nova_dir module.\n(Runing the script alone without Nova Hub is not recommended as they may be bugs and we won't be able to remotely fix those bugs.)")
    
    print_and_log()

ran_as_script = False

current_dir = os.path.dirname(os.path.realpath(__file__)) #Current Working Dir

'''
temp_folder_path = settings.temp_folder_path
path_to_logs = settings.path_to_logs
path_to_appdata_folder = settings.path_to_appdata_folder
path_to_terra_smp_dir = settings.path_to_terra_smp_folder
path_to_mods_folder = settings.path_to_mods_folder
path_to_mc_versions_folder = settings.path_to_mc_versions_folder
forge_ver_name = settings.forge_ver_name
path_to_old_forge_folder = settings.path_to_old_forge_folder
path_to_mc_launcher_exe = settings.path_to_mc_launcher_exe
'''

live_installer_status = "Starting script..." #Status for installer gui.
live_installer_progress_bar = 0

def exit_run(): 
    #Exit script
    print_and_log(None, "Exiting in...")
    time.sleep(1)
    print_and_log(None, "5")
    time.sleep(1)
    print_and_log(None, "4")
    time.sleep(1)
    print_and_log(None, "3")
    time.sleep(1)
    print_and_log(None, "2")
    time.sleep(1)
    print_and_log(None, "1")
    time.sleep(1)
    exit

def run(option=None): #This is the main run script that actualy runs the script to install the modpack.
    print_and_log("APP_NAME", "[{}]".format(script_name))
    global live_installer_status
    global live_installer_progress_bar

    if option == None:
        option = "NORMAL"

    if option.upper() == 'NORMAL': #Creates terra smp folder, installs forge and installs mods.

        #Create and clear Temp Folder.
        create_temp_folder()
        clear_temp_folder()
        live_installer_progress_bar = 3

        #Create Nova Universe App Data Folder.
        create_nova_hub_appdata_folder()
        live_installer_progress_bar = 6

        #Create Terra SMP Folder.
        path_to_appdata_folder = Nova_Dir.get_nova_universe_directory()
        create_folder(f"{path_to_appdata_folder}\\TerraSMP")
        live_installer_progress_bar = 9

        #Download Forge.
        live_installer_status = "Downloading Forge..."
        print_and_log(None, "Downloading Forge...")

        destination_path = download_modpack_file(modpack_code_name, "forge.zip")
        live_installer_progress_bar = 20

        #Extract Forge Zip.
        live_installer_status = "Extracting Forge..."
        print_and_log(None, "Extracting Forge...")
        extract_zip(destination_path + "\\forge.zip")
        live_installer_progress_bar = 40

        #Find versions folder.
        nova_hub_json = get_nova_hub_json()
        path_to_dot_minecraft = Nova_Dir.get_mc_game_directory()
        path_to_mc_versions_folder = path_to_dot_minecraft + "\\versions"

        #Move Forge to mc versions folder.
        live_installer_status = "Moving Forge..."
        print_and_log(None, "Moving Forge...")
        mc_version_name = nova_hub_json["packs"]["terra_smp"]["mc_version"]
        forge_dir = destination_path + "\\forge" + f"\\{mc_version_name}"

        extract_zip(forge_dir + ".zip")
        move_confirmation = move_file(forge_dir, path_to_mc_versions_folder)

        if move_confirmation == False:
            #Delete previous forge and move new forge.
            delete_file(path_to_mc_versions_folder + f"\\{mc_version_name}")
            move_file(forge_dir, path_to_mc_versions_folder)

        live_installer_progress_bar = 58
        clear_temp_folder() #Deletes all files in temp folder.
        live_installer_progress_bar = 60

        #Download Mods Zip.
        live_installer_status = "Downloading Mods..."
        print_and_log(None, "Downloading Mods...")
        destination_path = download_modpack_file(modpack_code_name, "mods.zip")
        live_installer_progress_bar = 62

        #Extract Mods Zip.
        live_installer_status = "Extracting Mods..."
        print_and_log(None, "Extracting Mods...")
        extract_zip(destination_path + "\\mods.zip")
        live_installer_progress_bar = 64

        #Delete Mods Zip.
        delete_file(destination_path + "\\mods.zip")
        live_installer_progress_bar = 66

        #Find nova_universe dir
        path_to_nova_universe_dir = Nova_Dir.get_nova_universe_directory()

        #Move the mods to TerraSMP appdata folder.
        mods_folder = create_folder(path_to_nova_universe_dir + "\\TerraSMP\\mods")
        live_installer_progress_bar = 68
        clear_mods_folder("terra_smp") #Makes sure there are no mods in the folder.
        live_installer_progress_bar = 70
        move_files(destination_path + "\\mods", path_to_nova_universe_dir + "\\TerraSMP\\mods", replace=True)
        live_installer_progress_bar = 72

        #Clear temp
        clear_temp_folder()

        #Download Shaders Zip.
        live_installer_status = "Downloading Shaders..."
        print_and_log(None, "Downloading Shaders...")

        destination_path = download_modpack_file("terra_smp", "shaders.zip")
        live_installer_progress_bar = 74

        #Extract Shaders Zip.
        live_installer_status = "Extracting Shaders..."
        print_and_log(None, "Extracting Shaders...")
        extract_zip(destination_path + "\\shaders.zip")
        live_installer_progress_bar = 84

        #Delete Shaders Zip.
        delete_file(destination_path + "\\shaders.zip")
        live_installer_progress_bar = 86

        #Move shaders to TerraSMP appdata folder.
        path_to_nova_universe_dir = Nova_Dir.get_nova_universe_directory()
        live_installer_progress_bar = 88
        create_folder(path_to_nova_universe_dir + "\\TerraSMP\\shaderpacks")
        live_installer_progress_bar = 90
        move_files(destination_path + "\\shaders", path_to_nova_universe_dir + "\\TerraSMP" + "\\shaderpacks", replace=True)
        live_installer_progress_bar = 94

        #Download Modpack assets
        live_installer_status = "Downloading Other Assets..."
        print_and_log(None, "Downloading Other Assets...")

        destination_path = download_modpack_file("terra_smp", "modpack_assets.zip")
        live_installer_progress_bar = 95

        #Extract modpack_assets.zip
        live_installer_status = "Extracting Other Assets..."
        print_and_log(None, "Extracting Other Assets...")
        extract_zip(destination_path + "\\modpack_assets.zip")
        live_installer_progress_bar = 96

        #Delete modpack_assets.zip.
        delete_file(destination_path + "\\modpack_assets.zip")
        live_installer_progress_bar = 97

        #Move assets to TerraSMP game folder.
        path_to_nova_universe_dir = Nova_Dir.get_nova_universe_directory()
        live_installer_progress_bar = 98
        create_folder(path_to_nova_universe_dir + "\\TerraSMP\\config")
        create_folder(path_to_nova_universe_dir + "\\TerraSMP\\resources")
        live_installer_progress_bar = 99
        move_files(destination_path + "\\modpack_assets\\config", path_to_nova_universe_dir + "\\TerraSMP\\config", replace=True)
        move_files(destination_path + "\\modpack_assets\\resources", path_to_nova_universe_dir + "\\TerraSMP\\resources", replace=True)

        #Clear temp
        clear_temp_folder()

        #Open MC Launcher
        live_installer_status = "Opening MC Launcher..."
        print_and_log(None, "Opening MC Launcher...")

        live_installer_progress_bar = 100

        live_installer_status = "[READY TO LAUNCH]"
        print_and_log(None, "[DONE]")
        print_and_log()

        if ran_as_script == True:
            path_to_mc_launcher_exe = Nova_Dir.get_mc_launcher_directory()
            subprocess.call(path_to_mc_launcher_exe)
            exit_run()

        if ran_as_script == False:
            sys.exit()

        return True

    if option.upper() == 'UPDATE':
        if not ran_as_script == True:
            live_installer_progress_bar = 0
            live_installer_status = "Clearing temp folder..."
            clear_temp_folder()
            live_installer_progress_bar = 5

            live_installer_status = "Downloading forge.zip..."
            download_modpack_file("terra_smp", "forge.zip")
            live_installer_progress_bar = 10

            live_installer_status = "Downloading mods.zip..."
            download_modpack_file("terra_smp", "mods.zip")
            live_installer_progress_bar = 15

            live_installer_status = "Downloading shaders.zip..."
            destination_path = download_modpack_file("terra_smp", "shaders.zip")
            live_installer_progress_bar = 20

            for file in check_dir(destination_path): #Extract all zips in temp folder.
                extract_zip(destination_path + f"\\{file}")

            live_installer_progress_bar = 40

            live_installer_progress_bar = 42

            nova_hub_json = get_nova_hub_json()
            path_to_dot_minecraft = Nova_Dir.get_mc_game_directory()
            path_to_mc_versions_folder = path_to_dot_minecraft + "\\versions"

            #Move Forge to mc versions folder.
            live_installer_status = "Moving Forge..."
            print_and_log(None, "Moving Forge...")
            mc_version_name = nova_hub_json["packs"]["terra_smp"]["mc_version"]
            forge_dir = destination_path + "\\forge" + f"\\{mc_version_name}"

            extract_zip(forge_dir + ".zip")
            move_confirmation = move_file(forge_dir, path_to_mc_versions_folder)

            if move_confirmation == False:
                #Delete previous forge and move new forge.
                delete_file(path_to_mc_versions_folder + f"\\{mc_version_name}")
                move_file(forge_dir, path_to_mc_versions_folder)

            live_installer_progress_bar = 60

            path_to_nova_universe_dir = Nova_Dir.get_nova_universe_directory()

            #Move new mods to mods folder.
            mods_dir = destination_path + "\\mods"
            clear_mods_folder("terra_smp") #Makes sure there are no mods in the folder.
            move_files(mods_dir, path_to_nova_universe_dir + "\\TerraSMP\\mods", replace=True)
            live_installer_progress_bar = 80

            #Move new shaders to shaders folder.
            shaders_dir = destination_path + "\\shaders"
            move_files(mods_dir, path_to_nova_universe_dir + "\\TerraSMP\\shaderpacks", replace=True)

            #Download Modpack assets
            live_installer_status = "Downloading Other Assets..."
            print_and_log(None, "Downloading Other Assets...")

            destination_path = download_modpack_file("terra_smp", "modpack_assets.zip")
            live_installer_progress_bar = 85

            #Extract modpack_assets.zip
            live_installer_status = "Extracting Other Assets..."
            print_and_log(None, "Extracting Other Assets...")
            extract_zip(destination_path + "\\modpack_assets.zip")
            live_installer_progress_bar = 88

            #Delete modpack_assets.zip.
            delete_file(destination_path + "\\modpack_assets.zip")
            live_installer_progress_bar = 90

            #Move assets to TerraSMP game folder.
            path_to_nova_universe_dir = Nova_Dir.get_nova_universe_directory()
            live_installer_progress_bar = 92
            create_folder(path_to_nova_universe_dir + "\\TerraSMP\\config")
            create_folder(path_to_nova_universe_dir + "\\TerraSMP\\resources")
            live_installer_progress_bar = 94
            move_files(destination_path + "modpack_assets\\config", path_to_nova_universe_dir + "\\TerraSMP\\config", replace=True)
            move_files(destination_path + "modpack_assets\\resources", path_to_nova_universe_dir + "\\TerraSMP\\resources", replace=True)

            live_installer_progress_bar = 100

            clear_temp_folder()

            live_installer_status = "[DONE]"
            print_and_log("info_2", "[DONE]")
            print_and_log()

            if ran_as_script == True:
                subprocess.call(path_to_mc_launcher_exe)
                exit_run()

            if ran_as_script == False:
                sys.exit()

            return True

        else:
            print_and_log("error", "Updating isn't supported yet for stand alone script exacution. The script will need to be ran by Nova Hub.")
            return False

    if option.upper() == 'UNINSTALL':
        live_installer_progress_bar = 0
        print_and_log(None, "Deleting TerraSMP folder...")
        live_installer_status = "Deleting TerraSMP folder..."
        path = Nova_Dir.get_nova_universe_directory()
        live_installer_progress_bar = 40
        delete_file(path + "\\TerraSMP")
        live_installer_progress_bar = 100
        live_installer_status = "[DONE]"
        print_and_log("info_2", "[DONE]")

        if ran_as_script == True:
            exit_run()

        if ran_as_script == False:
            sys.exit()

        return True

if __name__ == '__main__':
    #This executes only if the file is run as a script.
    ran_as_script = True

    option = None
    try:
        option = sys.argv[1]

    except IndexError as e:
        print_and_log("WARN", "Couldn't grab command line argument, if you didn't pass an argument ignore this.")
        print_and_log()
    
    #Check if os is supported.
    is_supported = Nova_Dir.is_supported()
    
    if is_supported == True:
        run(option)

    if is_supported == False:
        print_and_log("ERROR", "This OS is not supported. The installer only supports Windows at the moment.")
        print_and_log()

        exit_run()
