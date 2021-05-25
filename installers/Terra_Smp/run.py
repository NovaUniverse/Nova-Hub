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


from . import settings
from . import game_directory_finder

#Try using Nova Hub's function file first. (Only works if runing script from Nova Hub.)
try:
    from . import nova_func
    from nova_func import print_and_log
    print_and_log("info", "Using functions from Nova Hub.")

except ImportError: #If error import function file from root.
    import nova_func
    from nova_func import print_and_log
    print_and_log("warn", "The script failed to use functions from Nova Hub so it's own temporary functions.\n(Runing the script alone without Nova Hub is not recommended as they may be bugs and we won't be able to fix those bugs.)")


current_dir = os.path.dirname(os.path.realpath(__file__)) #Current Working Dir

temp_folder_path = settings.temp_folder_path
path_to_logs = settings.path_to_logs
path_to_appdata_folder = settings.path_to_appdata_folder
path_to_terra_smp_dir = settings.path_to_terra_smp_folder
path_to_mods_folder = settings.path_to_mods_folder
path_to_mc_versions_folder = settings.path_to_mc_versions_folder
forge_ver_name = settings.forge_ver_name
path_to_old_forge_folder = settings.path_to_old_forge_folder
path_to_mc_launcher_exe = settings.path_to_mc_launcher_exe

ran_as_script = False

live_installer_status = "Starting script..." #Status for installer gui.
live_installer_progress_bar = 0

def get_time_and_date(option):

    if option.lower() == 'date':
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%d-%m-%Y")
        return current_date

    if option.lower() == 'time':
        t = time.localtime()
        # hh/mm/ss
        current_time = time.strftime("%H.%M.%S", t)
        return current_time

    if option.lower() == 'both':
        #Date
        today = date.today()
        current_date = today.strftime("%d-%m-%Y")

        #Time
        t = time.localtime()
        current_time = time.strftime("%H.%M.%S", t)

        both = "({}) [{}]".format(current_date, current_time)
        return both

log_date_and_time = get_time_and_date("both") #Time run file was ran.

def print_and_log(importance_level=None, text=None):
    
    if text == None: #Just makes a new line.
        print ("")
        log("")
        return

    if not text == None:
        if importance_level == None:
            time = get_time_and_date("time")
            context = ("({}) {}".format(time, text))

            print (f"\u001b[37m{context}\u001b[0m")
            log(context)
            return

        if importance_level.upper() == 'INFO':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print (f"\u001b[36m{context}\u001b[0m") #Clay
            log(context)
            return

        if importance_level.upper() == 'INFO_2':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print (f"\u001b[32m{context}\u001b[0m") #Green
            log(context)
            return

        if importance_level.upper() == 'WARN':
            time = get_time_and_date("time")
            context = ("({}) [WARN] {}".format(time, text))

            print (f"\u001b[33m{context}\u001b[0m") #Yellow
            log(context)
            return

        if importance_level.upper() == 'ERROR':
            time = get_time_and_date("time")
            context = ("({}) [ERROR] {}".format(time, text))

            print (f"\u001b[31m{context}\u001b[0m") #Red
            log(context)
            return

        if importance_level.upper() == 'APP_NAME':
            context = (text)

            print (f"\u001b[35m{context}\u001b[0m")
            log(context)
            return

def log(text):
    #Create Logs Folder.
    try:
        os.mkdir(path_to_logs)

    except FileExistsError as e:
        live_installer_status = "[Log Folder Already Exists]"

    f = open(f"{settings.path_to_logs}{log_date_and_time}.txt", "a")
    f.write(text + "\n")

def create_temp_folder(path=""):
    global live_installer_status
    #Create Temp Folder.
    live_installer_status = "Creating Temp Folder..."
    print_and_log(None, "Creating Temp Folder in '" + path + temp_folder_path + "'")
    try:
        os.mkdir(path + temp_folder_path)
        os.chmod("temp", stat.S_IWRITE) #Turn off read only.
        return True

    except FileExistsError as e:
        live_installer_status = "[Temp Folder Already Exists]"
        print_and_log("INFO", "Temp Folder Already Exists.")
        print_and_log()
        return None

def clear_temp_folder():
    global live_installer_status
    live_installer_status = "Clearing Temp Folder..."
    print_and_log(None, "Clearing Temp Folder...")
    temp_files = os.listdir(temp_folder_path)

    try:
        for f in temp_files:
            print_and_log(None, f"Removing {f}")
            try:
                os.remove(temp_folder_path + f) #Deleting as fiile
            except WindowsError as e:
                shutil.rmtree(temp_folder_path + f) #If not file delete as directory with it's contexts.
            print_and_log(None, "[Done]")

        print_and_log()
        return True

    except OSError as e:
        print_and_log("ERROR", f"Error occured while clearing temp folder. \n {e}")
        return False

def clear_mods_folder():
    global live_installer_status
    live_installer_status = "Clearing Mods Folder..."
    print_and_log(None, "Clearing Mods Folder...")
    temp_files = os.listdir(path_to_mods_folder)

    try:
        for f in temp_files:
            print_and_log(None, f"Removing {f}")
            try:
                os.remove(path_to_mods_folder + f) #Deleting as fiile
            except WindowsError as e:
                shutil.rmtree(path_to_mods_folder + f) #If not file delete as directory with it's contexts.
            print_and_log(None, "[Done]")

        print_and_log()
        return True

    except OSError as e:
        print_and_log("ERROR", f"Error occured while clearing temp folder. \n {e}")
        print_and_log()
        return False

def delete_file(file):
    global live_installer_status

    live_installer_status = f"Deleting {file}..."
    print_and_log(None, f"Deleting {file}...")

    try:
        try:
            os.remove(file) #Deleting as fiile
        except WindowsError as e:
            shutil.rmtree(file) #If not file delete as directory with it's contexts.
        print_and_log(None, "[Done]")
        live_installer_status = "[Done]"

        print_and_log()
        return True

    except OSError as e:
        print_and_log("ERROR", f"Error occured while removing {file} \n {e}")
        live_installer_status = e
        return False

def create_appdata_folder():
    global live_installer_status
    live_installer_status = "Creating AppData Folder..."
    print_and_log(None, "Creating AppData Folder in '" + path_to_appdata_folder + "'")
    try:
        os.mkdir(path_to_appdata_folder)
        os.chmod(path_to_appdata_folder, stat.S_IWRITE)
        return True

    except FileExistsError as e:
        live_installer_status = "[AppData Folder Already Exists]"
        print_and_log("INFO", "AppData Folder Already Exists.")
        print_and_log()
        return None

def create_folder(path):
    global live_installer_status
    live_installer_status = "Creating a Folder..."
    print_and_log(None, "Creating Folder '" + path + "'")
    try:
        os.mkdir(path)
        os.chmod(path, stat.S_IWRITE)
        print_and_log(None, "[DONE]")
        return path

    except FileExistsError as e:
        live_installer_status = "[Folder Already Exists]"
        print_and_log("INFO", "This Folder Already Exists.")
        print_and_log()
        return path

def download_file(url, download_path):
    global live_installer_status
    global live_installer_progress_bar
    try: 
        headers = {'User-Agent': str(settings.app_name)}

        r = requests.get(url, allow_redirects=True, headers=headers)
        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        return True

    except OSError as e:
        print_and_log("ERROR", e)
        live_installer_status = e
        return False

def extract_zip(path_to_zip):
    global live_installer_status
    try:
        with ZipFile(path_to_zip, 'r') as zip:
            print_and_log()
            zip.printdir()
            print_and_log()
            zip.extractall(temp_folder_path)
            print_and_log(None, "[Done]")
            print_and_log()
            zip.close()
        return True

    except OSError as e:
        print_and_log("ERROR", e)
        print_and_log()
        live_installer_status = e
        return False

def move_files(from_dir, target_dir): #Move multiple files from a directory.
    global live_installer_status
    try:
        files = os.listdir(from_dir)
 
        for f in files:
            print_and_log(None, f"Moving {f} to {target_dir}")
            shutil.move(from_dir + f, target_dir)
            print_and_log(None, "[Done]")

        print_and_log()
        return True

    except FileExistsError as e:
        print_and_log("INFO", "This File Already Exists.")
        print_and_log()
        return False

    except OSError as e:
        print_and_log("ERROR", e)
        print_and_log()
        live_installer_status = e
        return False

def move_file(f, target_dir): #Move a single file
    global live_installer_status
    try:
        print_and_log(None, f"Moving {f} to {target_dir}")
        shutil.move(f, target_dir)
        print_and_log(None, "[Done]")
        print_and_log()
        return True

    except FileExistsError as e:
        print_and_log("INFO", "This File Already Exists.")
        print_and_log()
        return False

    except OSError as e:
        print_and_log("ERROR", e)
        print_and_log()
        live_installer_status = e
        return False

def create_mc_launcher_profile():
    global live_installer_status

    try:
        pass #Work in progress

    except Exception as e:
        pass

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
    print_and_log("APP_NAME", "[{}]".format(settings.app_name))
    global live_installer_status
    global live_installer_progress_bar

    if option == None:
        option = "NORMAL"

    if option.upper() == 'NORMAL': #Creates terra smp folder, installs forge and installs mods.

        #Create Temp Folder.
        create_temp_folder()
        live_installer_progress_bar = 3

        #Create Nova Universe App Data Folder.
        create_appdata_folder()
        live_installer_progress_bar = 6

        #Create Terra SMP Folder.
        create_folder(f"{path_to_appdata_folder}\\TerraSMP")
        live_installer_progress_bar = 9

        #Download Forge.
        live_installer_status = "Downloading Forge..."
        print_and_log(None, "Downloading Forge...")

        forge_zip_dir = temp_folder_path + "forge.zip"
        download_file(settings.forge_zip_url, forge_zip_dir)
        live_installer_progress_bar = 20

        #Extract Forge Zip.
        live_installer_status = "Extracting Forge..."
        print_and_log(None, "Extracting Forge...")
        extract_zip(forge_zip_dir)
        live_installer_progress_bar = 40

        #If 1.12.2 forge exists in mc versions, move to old_forge folder.
        found_old_forge = None
        found_replacement_forge = None
        live_installer_status = "Checking if Forge is already installed..."
        print_and_log(None, "Checking if a version of Forge is already installed...")

        files_in_mc_versions_dir = os.listdir(settings.path_to_mc_versions_folder)
        live_installer_progress_bar = 42
        
        for version in files_in_mc_versions_dir:
            print_and_log(None, version)
            if str(version[ 0 : 13 ]) in settings.forge_1_12_2_identifiers:#
                live_installer_progress_bar = 44
                found_replacement_forge = True
                found_old_forge = False
                if not version == settings.forge_ver_name: #If the version it has found is exact same
                    found_old_forge = True                          #version as replacement forge then do not replace.
                    found_replacement_forge = False
                    live_installer_progress_bar = 46
                    print_and_log("INFO_2", f"Found {version}")

                    #Create old_forge folder.
                    create_folder("old_forge")
                    live_installer_progress_bar = 48

                    #Move this forge version to old_forge folder.
                    old_forge_dir = settings.path_to_mc_versions_folder + "\\" + version
                    move_file(old_forge_dir, "./" + path_to_old_forge_folder)
                    live_installer_progress_bar = 52

                    break

        live_installer_progress_bar = 52

        if found_old_forge == None:
            print_and_log("INFO", "Forge was not Found")
            print_and_log()

        if found_replacement_forge == True:
            print_and_log("INFO", "Replacement Forge Already Exsits")
            print_and_log()

        if not found_replacement_forge == True:
            #Move Forge to mc versions folder.
            live_installer_status = "Moving Forge..."
            print_and_log(None, "Moving Forge...")
            forge_dir = temp_folder_path + "\\" + settings.forge_ver_name
            move_file(forge_dir, settings.path_to_mc_versions_folder)
            live_installer_progress_bar = 60

        live_installer_progress_bar = 60
        clear_temp_folder() #Deletes all files in temp folder.
        live_installer_progress_bar = 64

        #Download Mods Zip.
        live_installer_status = "Downloading Mods..."
        print_and_log(None, "Downloading Mods...")

        mod_zip_dir = temp_folder_path + "mods.zip"
        download_file(settings.modpack_zip_url, mod_zip_dir)
        live_installer_progress_bar = 74

        #Extract Mods Zip.
        live_installer_status = "Extracting Mods..."
        print_and_log(None, "Extracting Mods...")
        extract_zip(mod_zip_dir)
        live_installer_progress_bar = 84

        #Delete Mods Zip.
        delete_file(mod_zip_dir)
        live_installer_progress_bar = 86

        #Move the mods to TerraSMP appdata folder.
        mods_folder = create_folder(path_to_terra_smp_dir + "\\mods")
        live_installer_progress_bar = 88
        clear_mods_folder() #Makes sure there are no mods in the folder.
        live_installer_progress_bar = 90
        move_files(temp_folder_path, path_to_mods_folder)
        live_installer_progress_bar = 96

        #Create MC Launcher Profile
        '''
        "2fd04fe264ce3770d509522f1698cdb1" : {
          "created" : "2021-05-12T23:12:28.655Z",
          "gameDir" : "C:\\Users\\pc\\AppData\\Roaming\\.NovaUniverse\\TerraSMP",
          "icon" : "Dirt_Podzol",
          "javaArgs" : "-Xmx3G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M",
          "lastUsed" : "1970-01-01T00:00:00.000Z",
          "lastVersionId" : "1.12.2-forge-14.23.5.2854",
          "name" : "Terra Smp - v2.00",
          "type" : "custom"

        '''
        #Where I left off. (14/05/2021)

        #Open MC Launcher
        live_installer_status = "Opening MC Launcher..."
        print_and_log(None, "Opening MC Launcher...")

        live_installer_progress_bar = 100

        live_installer_status = "[READY TO LAUNCH]"
        print_and_log(None, "[DONE]")
        print_and_log()

        if ran_as_script == True:
            subprocess.call(path_to_mc_launcher_exe)
            exit_run()

        if ran_as_script == False:
            sys.exit()

        return True

    if option.upper() == 'RESTORE_FORGE': #Restores the forge version that got removed during the install.

        live_installer_status = "Restoring Forge..."
        print_and_log(None, "Restoring Forge...")

        path_exist = None
        path_exist = os.path.exists(path_to_old_forge_folder)

        if path_exist == True:
            move_files("./" + path_to_old_forge_folder, path_to_mc_versions_folder) #Move all versions of forge in here to mc versions folder.
            delete_file(path_to_mc_versions_folder + "\\" + forge_ver_name) #Delete replacement forge.
            return True

        if path_exist == False:
            live_installer_status = "[No Forge Versions to Restore]"
            print_and_log("info", "No Forge Versions to Restore")
            return None

    if option.upper() == 'UNINSTALL':
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
    is_supported = game_directory_finder.GameDirectoryFinder.is_supported()
    
    if is_supported == True:
        run(option)

    if is_supported == False:
        print_and_log("ERROR", "This OS is not supported. The installer only supports Windows and Linix.")
        print_and_log()

        exit_run()
