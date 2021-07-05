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
import traceback

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
        print("")
        path_to_log = log("")
        return path_to_log

    if not text == None:
        if importance_level == None:
            time = get_time_and_date("time")
            context = ("({}) {}".format(time, text))

            print(f"\u001b[37m{context}\u001b[0m")
            log(context)
            return

        if importance_level.upper() == 'INFO':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[36m{context}\u001b[0m") #Clay
            log(context)
            return

        if importance_level.upper() == 'INFO_2':
            time = get_time_and_date("time")
            context = ("({}) [INFO] {}".format(time, text))

            print(f"\u001b[32m{context}\u001b[0m") #Green
            log(context)
            return

        if importance_level.upper() == 'WARN':
            time = get_time_and_date("time")
            context = ("({}) [WARN] {}".format(time, text))

            print(f"\u001b[33m{context}\u001b[0m") #Yellow
            log(context)
            return

        if importance_level.upper() == 'ERROR':
            time = get_time_and_date("time")
            context = ("({}) [ERROR] {}".format(time, text))

            print(f"\u001b[31m{context}\u001b[0m") #Red
            log(context)
            return

        if importance_level.upper() == 'APP_NAME':
            context = (text)

            print(f"\u001b[35m{context}\u001b[0m")
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

    return f"{settings.path_to_logs}{log_date_and_time}.txt"

def delete_file(file):
    live_installer_status = f"Deleting {file}..."
    print_and_log(None, f"Deleting {file}...")

    try:
        try:
            os.remove(file) #Deleting as fiile
        except OSError as e:
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
            print(f)
            print_and_log(None, f"Moving {f} to {target_dir}")
            if not text_label == None:
                text_label.config(text=f"Moving {f} to {target_dir}")

            shutil.move(from_dir + f"\\{f}", target_dir)
            print_and_log(None, "[Done]")

            if not text_label == None:
                text_label.config(text="[Done]")

        except Exception as e:
            if replace == True: #Deletes File and replaces it with new file. (Basically overwrites the file.)
                print_and_log("INFO", "Deleting file '{}'...".format(f))
                if not text_label == None:
                    text_label.config(text="Deleting file '{}'...".format(f))
                delete_file(target_dir + "\\" + f)

                print_and_log(None, "[DONE]")
                if not text_label == None:
                    text_label.config(text="[DONE]")

                #Try moving again
                print_and_log(None, f"Moving {f} to {target_dir}")
                if not text_label == None:
                    text_label.config(text=f"Moving {f} to {target_dir}")

                try:
                    shutil.move(from_dir + f, target_dir)
                except Exception as e:
                    print_and_log("WARN", f"Could not replace {f}, so we skiping the file.")
                    pass

                print_and_log(None, "[Done]")

                if not text_label == None:
                    text_label.config(text="[Done]")

            else:
                print_and_log("ERROR", e)
                print_and_log()
                if not text_label == None:
                    text_label.config(text=e)


    print_and_log()
    return True

def move_file(path_to_file, target_dir, file_name=None, text_label=None, replace=False): #Move a single file
    try:
        print_and_log(None, f"Moving {path_to_file} to {target_dir}")
        shutil.move(path_to_file, target_dir)

        print_and_log(None, "[Done]")
        print_and_log()
        return True

    except Exception as e:
        if replace == True: #Deletes File and replaces it with new file. (Basically overwrites the file.)
            print_and_log("INFO", "Deleting file '{}'...".format(path_to_file))
            if not text_label == None:
                text_label.config(text="Deleting file '{}'...".format(path_to_file))
            delete_file(target_dir + "\\" + file_name)

            print_and_log(None, "[DONE]")
            if not text_label == None:
                text_label.config(text="[DONE]")

            #Try moving again
            print_and_log(None, f"Moving {file_name} to {target_dir}")
            if not text_label == None:
                text_label.config(text=f"Moving {file_name} to {target_dir}")

            try:
                shutil.move(path_to_file, target_dir)
            except Exception as e:
                print_and_log("WARN", f"Could not replace {path_to_file}, so we skiping the file.")
                pass

            print_and_log(None, "[Done]")

            if not text_label == None:
                text_label.config(text="[Done]")

        else:
            print_and_log("ERROR", e)
            print_and_log()
            if not text_label == None:
                text_label.config(text=e)

def download_file(url, download_path, text_label=None):
    import settings
    try:
        print_and_log(None, "Downloading file to {}...".format(download_path))
        headers = {'User-Agent': str(settings.app_name)}
        if not text_label == None:
            text_label.config(text="Downloading file to {}...".format(download_path))

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

def create_nova_hub_appdata_folder():
    import settings
    from nova_dir import Nova_Dir

    try:
        #Create .NovaUniverse
        path = f"{Nova_Dir.get_appdata_directory()}\\.NovaUniverse"
        create_folder(path)

        #Create #.nova_hub
        create_folder(path + "\\#.nova_hub")

    except Exception as e:
        print_and_log("ERROR", e)
        return False

def clear_mods_folder(modpack_code_name):
    import nova_dir
    from nova_dir import Nova_Dir

    print_and_log(None, "Clearing Mods Folder...")

    nova_hub_json = get_nova_hub_json(silent=True)
    modpack_folder_name = nova_hub_json["packs"][modpack_code_name]["names"]["folder_name"]
    path_to_mods_folder = (Nova_Dir.get_nova_universe_directory() + f"\\{modpack_folder_name}\\mods")

    mod_files = os.listdir(path_to_mods_folder)

    try:
        for f in mod_files:
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

def clear_temp_folder():
    print_and_log(None, "Clearing Temp Folder...")
    temp_files = os.listdir(".\\temp")

    try:
        for f in temp_files:
            print_and_log(None, f"Removing {f}")
            try:
                os.remove(".\\temp\\" + f) #Deleting as fiile
            except WindowsError as e:
                shutil.rmtree(".\\temp\\" + f) #If not file delete as directory with it's contexts.
            print_and_log(None, "[Done]")

        print_and_log()
        return True

    except OSError as e:
        print_and_log("ERROR", f"Error occured while clearing temp folder. \n {e}")
        return False

def create_temp_folder():
    #Create Temp Folder.
    print_and_log(None, "Creating Temp Folder...")
    try:
        os.mkdir(".\\logs")
        os.chmod("temp", stat.S_IWRITE) #Turn off read only.
        return True

    except FileExistsError as e:
        live_installer_status = "[Temp Folder Already Exists]"
        print_and_log("INFO", "Temp Folder Already Exists.")
        print_and_log()
        return None

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def download_modpack_file(modpack_code_name, file_name):
    import settings
    download_file(settings.api + settings.nova_hub_modpack_location + f"/{modpack_code_name}/{file_name}", f"temp\\{file_name}")

    return "temp"

def download_optifine(modpack_code_name, nova_hub_json):
    import settings
    import nova_dir
    from nova_dir import Nova_Dir

    print_and_log(None, "Finding Optifine version...")
    optifine_ver = nova_hub_json["packs"][modpack_code_name]["files"]["optifine"]
    folder_name = nova_hub_json["packs"][modpack_code_name]["names"]["folder_name"]
    print_and_log(None, "[DONE]")

    print_and_log(None, "Finding mods folder")
    nova_universe_dir = Nova_Dir.get_nova_universe_directory()
    modpack_game_dir = nova_universe_dir + f"\\{folder_name}"
    mods_folder = modpack_game_dir + "\\mods"
    print_and_log(None, "[DONE]")

    print_and_log(None, "Downloading OptiFine...")
    download_file(settings.api + f"/optifine/{optifine_ver}", mods_folder + f"\\{optifine_ver}")
    print_and_log("info_2", "[DONE]\n")

    del settings
    del nova_dir

def migrate_settings(modpack_code_name, nova_hub_json):
    pass

def get_nova_hub_json(silent=False, save_the_api=None):
    import settings

    #Save the API: I'm saving you bandwidth zeeraa, just take it...
     #Basically when I call this "get_nova_hub_json()" fucuntion I can choose if I want to save bandwidth and just load from cache or stream the data
      # from the api and cache it.

    if silent == False:
        print_and_log(None, "Connecting to API to grab nova_hub.json...")

    def cache_api_stream(nova_hub_json):
        cache_folder = create_folder(".\\nova_api_cache")

        #Cache modpack banners
        for modpack in nova_hub_json["packs"]:
            path_to_modpack_folder = create_folder(cache_folder + f"\\{modpack}")

            #Download modpack banner.
            name_of_banner = nova_hub_json["packs"][modpack]["nova_hub_banner"]
            destination_path = download_modpack_file(modpack, name_of_banner)

            #Move banner to cache folder.
            move_file(destination_path + f"\\{name_of_banner}", path_to_modpack_folder, file_name=name_of_banner, replace=True)

        #Cache json.
        with open(cache_folder + "\\nova_hub.json", "w") as f: #Write
            json.dump(nova_hub_json, f)

        if silent == False:
            print_and_log("info_2", "[Caching DONE]")
            print_and_log()

    try:
        if not save_the_api == True:

            import urllib.request
            req = urllib.request.Request(
                settings.api + settings.nova_hub_json_location, 
                data=None, 
                headers={
                    'User-Agent': str(settings.app_name)
                }
            )

            with urllib.request.urlopen(req) as url:
                nova_hub_json = json.loads(url.read().decode())

            if silent == False:
                print_and_log("info_2", "Grabbed json successfully!")
                print_and_log(None, "Caching data from API...")

            import threading
            t11=threading.Thread(target=cache_api_stream, args=([nova_hub_json]))
            t11.setDaemon(True)
            t11.start()

            return nova_hub_json

        if save_the_api == True:
            print_and_log("info", ":) Saving bandwidth and just using data from cache. (Click refresh button to connect to the api and refresh modpacks.)")
            with open(".\\nova_api_cache" + "\\nova_hub.json", "r") as f: #Read
                nova_hub_json = json.load(f)

            print_and_log("info_2", "[DONE]")
            print_and_log()

            return nova_hub_json

    except Exception as e:
        print_and_log("error", "Failed to connect to our API, grabbing json from cache instead...")
        print_and_log(None, traceback.print_exc())

        try:
            with open(".\\nova_api_cache" + "\\nova_hub.json", "r") as f: #Read
                nova_hub_json = json.load(f)

            print_and_log("info_2", "[DONE]")
            print_and_log()

            return nova_hub_json

        except FileNotFoundError as e:
            print_and_log("error", "We could not connect to our api and there's no cached files! Please check your internet connection.")
            return False

    del settings

class hub_settings:
    def edit(self, section, object_to_edit, new_value):
        import nova_dir
        from nova_dir import Nova_Dir

        try:
            print_and_log(None, f"Editing the nova hub user_settings.json")
            nova_universe_dir = Nova_Dir.get_nova_universe_directory()

            with open(nova_universe_dir + "\\#.nova_hub\\user_settings.json", "r") as f: #Read
                user_settings_json = json.load(f)

            user_settings_json[section][object_to_edit] = new_value
            print_and_log(None, f"Added {new_value} to {object_to_edit}.")

            with open(nova_universe_dir + "\\#.nova_hub\\user_settings.json", "w") as f: #Write
                json.dump(user_settings_json, f)
                print_and_log("info_2", "[Saved JSON]")
                print_and_log()

        except Exception as e:
            print_and_log("warn", f"An error occurred while editing the nova hub user_settings.json")
            print_and_log("error", traceback.print_exc())
            print_and_log()

        del nova_dir

    def read(self, section, object_to_read):
        import nova_dir
        from nova_dir import Nova_Dir

        try:
            print_and_log(None, f"Reading the nova hub user_settings.json")
            nova_universe_dir = Nova_Dir.get_nova_universe_directory()

            with open(nova_universe_dir + "\\#.nova_hub\\user_settings.json", "r") as f: #Read
                user_settings_json = json.load(f)

            value_to_return = user_settings_json[section][object_to_read]
            print_and_log(None, f"Read {value_to_return} from {object_to_read}.")

            return value_to_return

        except Exception as e:
            print_and_log("warn", f"An error occurred while reading the nova hub user_settings.json")
            print_and_log("error", traceback.print_exc())
            print_and_log()

        del nova_dir

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
        try:
            if modpack_code_name in check_dir(path):
                return True
            else:
                return False

        except FileNotFoundError as e:
            create_folder(".\\installers")
            return False

    def is_optifine_downloaded(self, modpack_code_name, nova_hub_json):
        import nova_dir
        from nova_dir import Nova_Dir

        optifine_ver = nova_hub_json["packs"][modpack_code_name]["files"]["optifine"]
        folder_name = nova_hub_json["packs"][modpack_code_name]["names"]["folder_name"]
        nova_universe_dir = Nova_Dir.get_nova_universe_directory()

        try:
            if optifine_ver in check_dir(nova_universe_dir + f"\\{folder_name}\\mods"):
                return True
            else:
                return False

        except FileNotFoundError as e:
            return False

    def need_update(self, modpack_code_name, nova_hub_json):
        import nova_dir
        from nova_dir import Nova_Dir

        #Grab nova_hub.json from web server.
        data_json = nova_hub_json

        display_name = data_json["packs"][modpack_code_name]["names"]["display_name"]

        #Check for updates.
        print_and_log(None, f"Checking if {display_name} needs an update...")

        #Grab mod_packs.json...
        path = Nova_Dir.get_nova_universe_directory()
        with open(path + "\\#.nova_hub\\mod_packs.json", "r") as f: #Read
            modpacks_json = json.load(f)
        
        #Look for modpack's current version on webserver.
        ver = data_json['packs'][modpack_code_name]['ver']

        #Decide if it needs an update or not.
        try:
            if ver > modpacks_json[modpack_code_name]['ver']:
                print_and_log("info_2", f"Found an update for {display_name}")
                print_and_log()
                return True

            else:
                print_and_log(None, f"{display_name} is update to date.")
                print_and_log()
                return False
        except KeyError as e:
            return None #This mod pack is not installed.
            print_and_log()

        del nova_dir

    class preload_shaders:
        def is_toggled(self):
            pass

        def what_setting(self):
            #Auto, Extreme, High, Medium, Lite.
            pass

        def auto_apply(self):
            #Applys best shaders based on computer specs.
            pass

class mc_launcher:
    def create_profile(self, code_name, profile_name, folder_name, todays_date, block_icon=None, base_64_icon_string=None, mc_version_name=None, java_args=None):
        import nova_dir
        from nova_dir import Nova_Dir

        try:
            print_and_log(None, f"Creating mc launcher profile for {profile_name}...")
            mc_path = Nova_Dir.get_mc_game_directory()
            print(mc_path)
            with open(mc_path + "\\launcher_profiles.json", "r") as f: #Read
                launcher_profiles_json = json.load(f)

            launcher_profiles_json["profiles"][code_name] = {}

            if not block_icon == None:
                launcher_profiles_json["profiles"][code_name]["icon"] = str(block_icon)
                print_and_log(None, "Added " + str(block_icon))

            if not base_64_icon_string == None:
                launcher_profiles_json["profiles"][code_name]["icon"] = f"data:image/png;base64,{base_64_icon_string}"
                print_and_log(None, "Added " + str(base_64_icon_string))

            if not mc_version_name == None:
                launcher_profiles_json["profiles"][code_name]["lastVersionId"] = mc_version_name
                print_and_log(None, "Added " + str(mc_version_name))

            launcher_profiles_json["profiles"][code_name]["name"] = profile_name
            print_and_log(None, "Added " + str(profile_name))

            path = Nova_Dir.get_nova_universe_directory()
            launcher_profiles_json["profiles"][code_name]["gameDir"] = (path + f"\\{folder_name}")
            print_and_log(None, "Added " + path + f"\\{folder_name}")

            launcher_profiles_json["profiles"][code_name]["javaArgs"] = java_args
            print_and_log(None, "Added " + str(java_args))

            launcher_profiles_json["profiles"][code_name]["lastUsed"] = todays_date
            print_and_log(None, "Added " + str(todays_date))

            launcher_profiles_json["profiles"][code_name]["type"] = ""

            with open(mc_path + "\\launcher_profiles.json", "w") as f: #Write
                json.dump(launcher_profiles_json, f)
                print_and_log("info_2", "Saved JSON")

        except Exception as e:
            print_and_log("warn", f"An error occurred while creating a MC launcher profile for {profile_name}")
            print_and_log("error", e)

        del nova_dir

    def edit_profile(self, code_name, display_name, value_to_edit, new_value):
        import nova_dir
        from nova_dir import Nova_Dir

        try:
            print_and_log(None, f"Editing mc launcher profile for {display_name}...")
            mc_path = Nova_Dir.get_mc_game_directory()
            print(mc_path)
            with open(mc_path + "\\launcher_profiles.json", "r") as f: #Read
                launcher_profiles_json = json.load(f)

            if value_to_edit.lower() == "block_icon":
                launcher_profiles_json["profiles"][code_name]["icon"] = str(new_value)
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit.lower() == "base64_icon":
                launcher_profiles_json["profiles"][code_name]["icon"] = f"data:image/png;base64,{new_value}"
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit == "lastVersionId":
                launcher_profiles_json["profiles"][code_name]["lastVersionId"] = new_value
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit.lower() == "name":
                launcher_profiles_json["profiles"][code_name]["name"] = new_value
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit == "gameDir":
                path = Nova_Dir.get_nova_universe_directory()
                launcher_profiles_json["profiles"][code_name]["gameDir"] = (path + f"\\{new_value}")
                print_and_log(None, "Added " + path + f"\\{new_value}")

            if value_to_edit == "javaArgs":
                launcher_profiles_json["profiles"][code_name]["javaArgs"] = new_value
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit == "lastUsed":
                launcher_profiles_json["profiles"][code_name]["lastUsed"] = new_value
                print_and_log(None, "Added " + str(new_value))

            if value_to_edit.lower() == "type":
                launcher_profiles_json["profiles"][code_name]["type"] = new_value

            with open(mc_path + "\\launcher_profiles.json", "w") as f: #Write
                json.dump(launcher_profiles_json, f)
                print_and_log("info_2", "Saved JSON")
                print_and_log()

        except Exception as e:
            print_and_log("warn", f"An error occurred while editing the MC launcher profile for {display_name}")
            print_and_log("error", e)
            print_and_log()

        del nova_dir

    def read_profile(self, code_name, display_name, value_to_read):
        import nova_dir
        from nova_dir import Nova_Dir

        try:
            print_and_log(None, f"Reading mc launcher profile for {display_name}...")
            mc_path = Nova_Dir.get_mc_game_directory()
            with open(mc_path + "\\launcher_profiles.json", "r") as f: #Read
                launcher_profiles_json = json.load(f)

            if value_to_read.lower() == "block_icon":
                value_to_return = launcher_profiles_json["profiles"][code_name]["icon"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read.lower() == "base64_icon":
                value_to_return = launcher_profiles_json["profiles"][code_name]["icon"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read == "lastVersionId":
                value_to_return = launcher_profiles_json["profiles"][code_name]["lastVersionId"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read.lower() == "name":
                value_to_return = launcher_profiles_json["profiles"][code_name]["name"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read == "gameDir":
                path = Nova_Dir.get_nova_universe_directory()
                value_to_return = launcher_profiles_json["profiles"][code_name]["gameDir"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read == "javaArgs":
                value_to_return = launcher_profiles_json["profiles"][code_name]["javaArgs"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read == "lastUsed":
                value_to_return = launcher_profiles_json["profiles"][code_name]["lastUsed"]
                print_and_log(None, f"Read {value_to_return}")

            if value_to_read.lower() == "type":
                value_to_return = launcher_profiles_json["profiles"][code_name]["type"]

            return value_to_return

        except Exception as e:
            print_and_log("warn", f"An error occurred while reading the MC launcher profile for {display_name}")
            print_and_log("error", e)
            print_and_log()

        del nova_dir