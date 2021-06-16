import os
import threading
import time
import ctypes
import json
import urllib.request
import requests

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image, ImageFilter
import tkinter.font as font

import settings
import nova_func
import nova_var_cache

live_installer_status = "Starting..."
live_installer_progress_bar = 0

t3 = None
live_status_string = ""

def launch_app(thread_to_wait_for=None):
    if not thread_to_wait_for == None: #Waits for update thread to finish.
        thread_to_wait_for.join()
        
    import app #Launchs Nova Hub

def focus_on_app():

    time.sleep(1) #Add 2 secound delay on production version
    user32 = ctypes.windll.user32

    # get handle for Notepad window
    # non-zero value for handle should mean it found a window that matches
    handle = user32.FindWindowW(u'{}'.format(settings.app_name), None)

    print(handle)

    user32.ShowWindow(handle, 5)

    #Meaning of 2nd parameter defined here.
    #https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx

def create_status_bar(frame):
    global live_installer_status
    global live_installer_progress_bar

    global progress
    global live_status_text

    #Progress Bar
    #live_status_text.config(anchor=CENTER)
    #live_status_text.place(x=418, y=75)

    s = ttk.Style() #Applys Theme
    s.theme_use('clam')
    s.configure("terra.Horizontal.TProgressbar", foreground='#C06565', background='#9F1F0F')

    progress = Progressbar(frame, style="terra.Horizontal.TProgressbar", orient=HORIZONTAL, length=600, mode='determinate')
    progress['value'] = 0
    progress.place(x=180, y=120)

def status_bar_thread():
    global live_status_string

    staus_bar = True

    while staus_bar == True:
        #live_status_text.config(text=live_status_string)

        time.sleep(0.006)

def check_for_update():
    global live_installer_progress_bar
    global window
    import settings

    data_json = nova_func.get_nova_hub_json()
    ver = data_json["current_version"]

    if ver > settings.version: #Work in progress
        #I disabled the live status thread because of main loop error.

        #version_text.config(text="V" + str(settings.version) + " --> V" + str(ver))
        
        '''
        t12 = threading.Thread(target=live_run_status, args=([main_frame]))
        t12.setDaemon(True)
        t12.start()
        '''

        #create_status_bar(main_frame)

        del settings #Unload settings.

        #Update...
        live_status_string = "Starting Update..."
        update_comfirmation = update_app("whole_app")

        #End of update
        
        if update_comfirmation == True:
            nova_func.print_and_log("INFO_2", "Nova Hub done updating to version {}".format(str(ver)))

    import settings

    if ver <= settings.version: #Up to date
        nova_func.print_and_log("INFO", "Nova Hub is up to date. Your on version {}".format(str(settings.version)))
        live_status_string = "Up to Date"
        
def update_app(mode):
    import nova_func
    
    if mode.lower() == "whole_app":

        #Run Updater
        try:
            import subprocess
            subprocess.call(".\\update.exe")
            exit
            sys.exit()

        except Exception as e:
            nova_func.print_and_log("warn", "Nova Hub failed to run update.exe, so it's going to skip this update. (Ignore this if you are running nova hub as source code.)")
            nova_func.print_and_log("error", e)

            return False

def check_nova_hub_appdata_folder():
    #Find the nova_universe directory.
    import nova_dir
    from nova_dir import Nova_Dir
    path = Nova_Dir.get_nova_universe_directory()
    del nova_dir

    if not "#.nova_hub" in nova_func.check_dir(path):
        #Create #.nova_hub folder.
        nova_func.create_nova_hub_appdata_folder()

        #Download user_settings.json template from webserver.
        with urllib.request.urlopen(settings.api + settings.user_settings_json_template_location) as url:
            template_json = json.loads(url.read().decode())

        #Create user_settings.json
        with open(path + "\\#.nova_hub\\user_settings.json", 'w') as f:
            json.dump(template_json, f)

    if not "mod_packs.json" in nova_func.check_dir(f"{path}\\#.nova_hub"):
        #Create modpacks.json
        modpacks_json = {}
        with open(path + "\\#.nova_hub\\mod_packs.json", 'w') as f:
            json.dump(modpacks_json, f)

    #Download assets folder if not avalible.
    if not "assets" in nova_func.check_dir("."):
        #Download assets
        nova_func.download_file(settings.api + "/assets.zip", ".\\assets.zip") #Test if it's possible to download a folder that's not a zip.
        nova_func.extract_zip(".\\assets.zip")
        nova_func.move_files(".\\temp", ".")

        nova_func.delete_file(".\\assets.zip")
        
        nova_func.clear_temp_folder()

    #Download updater script if not avalible
    if not "update.exe" in nova_func.check_dir("."):
        if not "update.py" in nova_func.check_dir("."): #This is here to prevent the app from downloading the exacutable version of the script if the .py version already exists.
            #Download assets
            nova_func.download_file(settings.api + settings.updater_script_location, ".\\updater_script.zip") #Test if it's possible to download a folder that's not a zip.
            nova_func.extract_zip(".\\updater_script.zip")
            nova_func.move_files(".\\temp\\updater_script", ".")

            nova_func.delete_file(".\\updater_script.zip")
            nova_func.delete_file(".\\updater_script")
            
            nova_func.clear_temp_folder()

    #Create installers folder if not avalible.
    if not "installers" in nova_func.check_dir("."):
        #Create installers folder.
        nova_func.create_folder(".\\installers")

    #Create popup_noti_cache.json if not avalible.
    if not "popup_noti_cache.json" in nova_func.check_dir("."):
        #Create json.
        popup_noti_cache_json = {}

        with open(".\\popup_noti_cache.json", "w") as f: #Write
            json.dump(popup_noti_cache_json, f)
        
def check_assets_folder():
    pass
    
def run_update_service():
    pass

check_nova_hub_appdata_folder() #This stays here, don't you dear move it OR THINGS WILL BREAK! I'm warning you!

window = Tk()

main_canvas = Canvas(window)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
main_frame.pack(fill=BOTH, expand=1)

update_text_font = font.Font(family='Arial Rounded MT Bold', size=20, weight='bold', underline=False)
update_text = Label(main_frame, text="Checking for Updates...", font=update_text_font, fg="#05FFFF", bg="#171717")
update_text.pack()

#Live Status
live_status_text = Label(main_frame, text="", font=("Arial Rounded MT Bold", 18), fg="#E1D8D8", 
pady=12, bg="#171717", wraplength=780)

#Version Text
version_text_font = font.Font(family='Arial Rounded MT Bold', size=18, weight='bold', underline=False)
version_text = Label(main_frame, text="", font=version_text_font, fg="#C52612", bg="#171717")
version_text.place(x=628, y=166)

#Image
update_image = Image.open(settings.path_to_assets + "update.png")

width, height = update_image.size

actual_width = round(int(width)/8)
actual_height = round(int(height)/8)

update_image = update_image.resize((actual_width, actual_height))
tkimage = ImageTk.PhotoImage(update_image)
update_image_label = Label(main_frame, image=tkimage, bg="#171717")
update_image_label.photo = tkimage
update_image_label.pack(side="left", padx=20)

window.title("NOVA HUB UPDATER")
window.iconbitmap(settings.path_to_assets + "update_icon.ico")
window.geometry('800x200')
window.resizable(False, False) #Makes window not resizeable

t12=threading.Thread(target=status_bar_thread) #Live Status Bar
t12.setDaemon(True)
t12.start()

def start_up_thread():
    global t3

    t3=threading.Thread(target=check_for_update)
    t3.setDaemon(True)
    t3.start()

if __name__ == '__main__':
    option = None
    try:
        option = sys.argv[1]
        nova_func.print_and_log("info_2", f":) We got your command line argument. >>> {option}")

    except IndexError as e:
        nova_func.print_and_log("WARN", "Couldn't grab command line argument, if you didn't pass an argument ignore this.")
        nova_func.print_and_log()
    
    t2 = threading.Thread(target=start_up_thread)
    t2.start()

    import nova_dir
    from nova_func import print_and_log

    if nova_dir.Nova_Dir.is_supported() == None: #If app is supported by OS.
        update_image_label.pack_forget()
        update_text.config(text="Sorry for the inconvenience but Nova Hub does not\n support your OS. We only support Windows atm\n but we'll be supporting Linix next.", 
        fg="red", pady=45)
        print_and_log("ERROR", "Sorry for the inconvenience but Nova Hub does not support your OS. We only support Windows atm but we'll be supporting Linix next. \n")

    else:
        window.destroy() #Kills Update Window

        t1 = threading.Thread(target=launch_app, args=([t3]))
        t1.start()

        t11 = threading.Thread(target=focus_on_app)
        t11.start()

window.mainloop()

#bad piggies drip - https://youtu.be/dkM9GxaCow4