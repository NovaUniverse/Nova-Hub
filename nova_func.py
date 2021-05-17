import time
import os
from datetime import date
import json
import urllib.request
import requests
import stat
import subprocess
from zipfile import ZipFile
import shutil

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
    import settings

    #Create Logs Folder.
    try:
        os.mkdir(settings.path_to_logs)

    except FileExistsError as e:
        live_installer_status = "[Log Folder Already Exists]"

    f = open(f"{settings.path_to_logs}{log_date_and_time}.txt", "a")
    f.write(text + "\n")

    del settings

def delete_file(file):
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
    import settings

    live_installer_status = "Creating AppData Folder..."
    print_and_log(None, "Creating AppData Folder in '" + settings.path_to_appdata_folder + "'")
    try:
        os.mkdir(settings.path_to_appdata_folder)
        os.chmod(settings.path_to_appdata_folder, stat.S_IWRITE)
        return True

    except FileExistsError as e:
        live_installer_status = "[AppData Folder Already Exists]"
        print_and_log("INFO", "AppData Folder Already Exists.")
        print_and_log()
        return None

    del settings

def create_folder(path):
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

def extract_zip(path_to_zip, text_label=None):
    import settings
    try:
        with ZipFile(path_to_zip, 'r') as zip:
            if not text_label == None:
                text_label.config(text=f"Excracting {path_to_zip}...")
    
            print_and_log()
            zip.printdir()
            print_and_log()
            zip.extractall(settings.temp_folder_path)
            print_and_log(None, "[Done]")
            if not text_label == None:
                text_label.config(text="[DONE]")

            print_and_log()
            zip.close()
        return True

    except OSError as e:
        print_and_log("ERROR", e)
        print_and_log()
        if not text_label == None:
            text_label.config(text=e)
        return False

    del settings

def move_files(from_dir, target_dir, text_label=None, replace=False): #Move multiple files from a directory.
    files = os.listdir(from_dir)

    for f in files:
        try:
            print_and_log(None, f"Moving {f} to {target_dir}")
            if not text_label == None:
                text_label.config(text=f"Moving {f} to {target_dir}")

            shutil.move(from_dir + f, target_dir)
            print_and_log(None, "[Done]")

            if not text_label == None:
                text_label.config(text="[Done]")

        except OSError as e:
            if replace == True: #Deletes File and replaces it with new file. (Basically overwrites the file.)
                print_and_log("INFO", "Deleting file '{}'...".format(f))
                if not text_label == None:
                    text_label.config(text="Deleting file '{}'...".format(f))
                os.remove(from_dir + f)

                print_and_log(None, "[DONE]")
                if not text_label == None:
                    text_label.config(text="[DONE]")

                #Try moving again
                print_and_log(None, f"Moving {f} to {target_dir}")
                if not text_label == None:
                    text_label.config(text=f"Moving {f} to {target_dir}")

                shutil.move(from_dir + f, target_dir)
                print_and_log(None, "[Done]")

                if not text_label == None:
                    text_label.config(text="[Done]")

            else:
                print_and_log("ERROR", e)
                print_and_log()
                if not text_label == None:
                    text_label.config(text=e)
                return False


    print_and_log()
    return True

def move_file(f, target_dir): #Move a single file
    try:
        print_and_log(None, f"Moving {f} to {target_dir}")
        shutil.move(f, target_dir)

        print_and_log(None, "[Done]")
        print_and_log()
        return True

    except FileExistsError as e:
        print_and_log("INFO", "This File Already Exists.")
        print_and_log()

        if os.path.isdir(target_dir): #Checks if it's a directory and removes all the contexts within it.
            if os.path.exists(target_dir):
                print_and_log("INFO", "Deleting directory '{}'...".format(target_dir))
                shutil.rmtree(target_dir)

        return False

    except OSError as e:
        print_and_log("ERROR", e)
        print_and_log()
        live_installer_status = e
        return False

def download_file(url, download_path, text_label=None):
    import settings
    try:
        print_and_log(None, "Downloading {}...".format(download_path))
        headers = {'User-Agent': str(settings.app_name)}
        if not text_label == None:
            text_label.config(text="Downloading {}...".format(download_path))

        r = requests.get(url, allow_redirects=True, headers=headers)
        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        print_and_log(None, "[DONE]")
        if not text_label == None:
            text_label.config(text="[DONE]")

        return True

    except OSError as e:
        print_and_log("ERROR", e)
        if not text_label == None:
            text_label.config(text=e)
        return False

    del settings

def check_dir(path_to_dir):
    files = os.listdir(path_to_dir)
    return files

def create_mc_launcher_profile():
    try:
        pass #Work in progress

    except Exception as e:
        pass

def create_nova_hub_appdata_folder():
    import settings

    try:
        #Create .NovaUniverse
        path = f"{settings.appdata_dir}\\.NovaUniverse"
        create_folder(path)

        #Create #.nova_hub
        create_folder(path + "\\#.nova_hub")

    except Exception as e:
        print_and_log("ERROR", e)
        return False

class check_modpack:

    def is_installed(self, modpack_folder_name):
        import nova_dir

        path = nova_dir.Nova_Dir.get_nova_universe_directory()
        if modpack_folder_name in check_dir(path):
            return True

        else:
            return False

    def is_script_downloaded(self, modpack_code_name):
        import settings

        path = settings.path_to_installers
        del settings
        if modpack_code_name in check_dir(path):
            return True
        else:
            return False