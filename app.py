import os
from tkinter import *
from tkinter import ttk
#from ttkthemes import themed_tk as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image, ImageFilter
#import tkinter.font as font
from tkinter import font
import threading
import time
import subprocess
from colour import Color
import webbrowser
import json
import importlib
import urllib.request
import requests
from tkhtmlview import HTMLLabel
import emoji
import psutil
import math
import pygame

import settings
from nova_func import *
from nova_dir import *

if not settings.option == None:
    if not (settings.option).lower() == "dev":
        import ctypes
        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 ) #Hides console

os.system('color FF')

app_name = settings.app_name

ver_v = "V" + str(settings.version)

lrs = False #Turns Live Status Thread off.
live_installer_status = "Starting Live Install Status Thread..."

downloaded_modpacks = {}
downloaded_modpacks['modpacks'] = {}

installs_button = None #Installs button needs to be global so I can choose not disble it when I'm looping through all of them in mod pack settings menu.
popup_noti_return_value = None

no_connection = False
current_frame = None
already_ran_api = None
installations_frame = None

t12 = None

def live_run_status(run, frame): #Updates
    global live_installer_status
    global lrs
    global progress
    global live_status_text

    lrs = True

    live_status_text = Label(main_frame, text=live_installer_status, font=("Arial Rounded MT Bold", 20), fg="#E1D8D8", 
    pady=12, bg="#171717", wraplength=780)
    live_status_text.config(anchor=CENTER)
    live_status_text.pack()

    s = ttk.Style() #Apply Theme
    s.theme_use('clam')
    s.configure("terra.Horizontal.TProgressbar", foreground='#C06565', background='#9F1F0F')

    progress = Progressbar(main_frame, style="terra.Horizontal.TProgressbar", orient=HORIZONTAL, length=600, mode='determinate')
    progress['value'] = run.live_installer_progress_bar
    progress.pack(pady=(0, 10))
    
    while lrs == True:
        live_installer_status = run.live_installer_status

        live_status_text.config(text=live_installer_status)

        progress['value'] = run.live_installer_progress_bar

        time.sleep(0.06)

def nav_bar():
    global installations_menu
    global home_frame
    global installs_button

    nav_bar = Frame(main_frame, width=window.winfo_width(), height=window.winfo_height() / 18, bg="#3D0000") #NavBar
    nav_bar.pack(side="top", fill=BOTH)

    Nova_Logo = Image.open(settings.path_to_images + "Nova-Universe.png")
    width, height = Nova_Logo.size
    
    actual_width = round(int(width)/11)
    actual_height = round(int(height)/11)

    #Nova_Logo = add_image_shadow(Nova_Logo, 50, 0, [10, 10], "#3D0000", "black")

    Nova_Logo_0 = Nova_Logo.resize((actual_width, actual_height))
    tkimage = ImageTk.PhotoImage(Nova_Logo_0)
    nova_logo_label = Label(nav_bar, image=tkimage, bg="#3D0000", cursor="hand2")
    nova_logo_label.photo = tkimage
    nova_logo_label.pack()
    nova_logo_label.bind("<Button-1>", open_url)

    t6=threading.Thread(target=logo_brething_effect, args=([Nova_Logo, Nova_Logo_0, nova_logo_label, actual_width, actual_height]))
    t6.setDaemon(True)
    #t6.start()

    buttons_bar = Frame(nav_bar, width=10, height=30, bg="#9F1F0F") #NavBar
    buttons_bar.pack(side="top", fill=BOTH)

    #Home Button
    home_button = Button(buttons_bar, text="Home", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: home_menu(home_button, current_frame)) 
    home_button.grid(row=0, column=1, padx=(15, 0))
    home_button.bind("<Enter>", button_hover_enter)
    home_button.bind("<Leave>", button_hover_leave)

    home_menu(home_button, None)
    
    #Installations Button
    installs_button = Button(buttons_bar, text="Installations", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: installations_menu(installs_button, current_frame))
    installs_button.grid(row=0, column=2, padx=(15, 0))
    installs_button.bind("<Enter>", button_hover_enter)
    installs_button.bind("<Leave>", button_hover_leave)
    
    #Settings Button
    settings_button = Button(buttons_bar, text="Settings", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: app_settings_menu(settings_button, current_frame))
    settings_button.grid(row=0, column=3, padx=(15, 0))
    settings_button.bind("<Enter>", button_hover_enter)
    settings_button.bind("<Leave>", button_hover_leave)

    settings.button_list = [home_button, installs_button, settings_button]

def installations_menu(button_used, previous_frame):
    global installations_frame
    global progress
    global live_status_text
    global current_frame
    global already_ran_api

    amount_of_installers = 0

    if not button_used == None: #Don't reset buttons if no button was used to get here.
        reset_clickable(settings.button_list)
    
    if not button_used == None:
        make_unclickable(button_used)
        button_used.bind("<Enter>", button_hover_enter)
        button_used.bind("<Leave>", button_hover_leave)

    if not previous_frame == None:
        previous_frame.pack_forget()

    installations_frame = Frame(main_frame, width=1280, height=720, bg="#171717")
    installations_frame.pack(fill=BOTH, expand=1)

    current_frame = installations_frame

    #API Refresh Button
    refresh_image = Image.open(settings.path_to_images + "refresh.png")

    width, height = refresh_image.size
    
    actual_width = round(int(width)/14)
    actual_height = round(int(height)/14)

    refresh_image = refresh_image.resize((actual_width, actual_height))
    tkimage = ImageTk.PhotoImage(refresh_image)
    refresh_button = Button(installations_frame, image=tkimage, bg="#171717", borderwidth=0, activebackground="#171717", 
    cursor="hand2")
    refresh_button.config(command=refresh_modpacks)
    refresh_button.grid(row=0, column=1 + amount_of_installers, padx=(15, 0), pady=15)
    refresh_button.bind("<Enter>", lambda event, sound="hover_1.wav", volume=0.1 : play_sound(sound=sound, volume=volume))
    refresh_button.photo = tkimage

    amount_of_installers +=1

    def modpack_glow_effect(modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, hex_list, hex_list_text):

        for colour in hex_list:
            time.sleep(0.01)
            modpack_frame.config(bg="{}".format(colour)) #Frame
            try:
                e.widget['background'] = '{}'.format(colour) #Button
                e.widget['activebackground'] = '{}'.format(colour)
            except AttributeError as error:
                e.config(bg="{}".format(colour))
                e.config(activebackground="{}".format(colour))
            
            modpack_title.config(bg="{}".format(colour)) #Title
            pack_image_frame.config(bg="{}".format(colour)) #Image
            version_label.config(bg="{}".format(colour)) #Version Label
            settings_button.config(bg="{}".format(colour), activebackground="{}".format(colour)) #Settings Button
        
        for colour in hex_list_text:
            modpack_title.config(fg="{}".format(colour)) #Title
            version_label.config(fg="{}".format(colour)) #Version Label

    def zoom_in_effect(modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button):

        pass

    def install_button_hover_enter(e, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button):
        hex_colour = Color("#282727")
        colours = list(hex_colour.range_to(Color("#C06565"), 12))

        hex_colour = Color("#C52612") #Text
        colours_text = list(hex_colour.range_to(Color("black"), 12))
        
        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

        play_sound("hover_1.wav", volume=0.1)

    def install_button_hover_leave(e, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button):
        hex_colour = Color("#C06565")
        colours = list(hex_colour.range_to(Color("#282727"), 20))

        hex_colour = Color("black") #Text
        colours_text = list(hex_colour.range_to(Color("#C52612"), 20))
        
        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

    def update_button_hover_enter(e, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button):
        hex_colour = Color("#282727")
        colours = list(hex_colour.range_to(Color("#ff8142"), 12)) #Dark Orange

        hex_colour = Color("#C52612") #Text
        colours_text = list(hex_colour.range_to(Color("black"), 12))
        
        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

        play_sound("hover_1.wav", volume=0.1)

    def update_button_hover_leave(e, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button):
        hex_colour = Color("#ff8142")
        colours = list(hex_colour.range_to(Color("#282727"), 20))

        hex_colour = Color("black") #Text
        colours_text = list(hex_colour.range_to(Color("#C52612"), 20))
        
        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

    def install_modpack(modpack_frame, installs_button, pack_image_frame, version_label, modpack_title, settings_button, code_name, run, nova_hub_json):
        def finish_effect():
            time.sleep(2)
            
            progress.pack_forget()
            live_status_text.pack_forget()

            hex_colour = Color("#C06565")
            colours = list(hex_colour.range_to(Color("#00B6C0"), 40))

            hex_colour = Color("#C52612") #Text
            colours_text = list(hex_colour.range_to(Color("black"), 12))
            
            t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
            t8.setDaemon(True)
            t8.start()

            launch_image = Image.open(settings.path_to_images + "nova_hub_launch_button.png")

            width, height = launch_image.size
            
            actual_width = round(int(width)/14)
            actual_height = round(int(height)/14)

            launch_image = launch_image.resize((actual_width, actual_height))
            tkimage = ImageTk.PhotoImage(launch_image)
            launch_button = Button(modpack_frame, text="Launch", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#00B6C0", activebackground="#00B6C0", borderwidth=0, 
            cursor="hand2")
            launch_button.config()
            launch_button.photo = tkimage

            t8.join()
            launch_button.place(x=64, y=210)

        #Install Effect
        hex_colour = Color("#C06565")
        colours = list(hex_colour.range_to(Color("#00C03E"), 20))

        hex_colour = Color("#C52612") #Text
        colours_text = list(hex_colour.range_to(Color("black"), 12))

        def install_thread():
            #Install Effect
            hex_colour = Color("#C06565")
            colours = list(hex_colour.range_to(Color("#00C03E"), 20))

            hex_colour = Color("#C52612") #Text
            colours_text = list(hex_colour.range_to(Color("black"), 12))

            if nova_hub_json["packs"][code_name]["GAC"] == True:
                terms_and_conditions = nova_hub_json["GAC_terms"]
                thread = popup_notification("agree_cancel", "Goose Anticheat", terms_and_conditions)
                thread.join()

            if popup_noti_return_value == True: #Install
                #Threads needed for install.
                t3=threading.Thread(target=run.run, args=(["NORMAL"])) #Run Installer thread.
                t3.setDaemon(True)
                t3.start()

                t2=threading.Thread(target=live_run_status, args=([run, modpack_frame])) #Live Run Stats
                t2.setDaemon(True)
                t2.start()

                time.sleep(0.1)

                t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
                t8.setDaemon(True)
                t8.start()

                #Check if this is terra smp and if old terra smp is already installed.
                if code_name == "terra_smp":
                    for folder in check_dir(Nova_Dir.get_mc_game_directory()):
                        folder = folder.lower()
                        if folder == "terrasmp":
                            thread = popup_notification("yes_no", f"Transfer Controls and Settings from old {display_name}?", f"We have detected that you have the old {display_name}, would you like to transfer all the controls and settings from it over to the NEW {display_name}. Notice: Make sure to launch the new {display_name} from now on.")
                            thread.join()
                    
                    if popup_noti_return_value == True:
                        pass

                #Create mc launcher profile for mod pack.
                from datetime import datetime
                todays_date = datetime.now().isoformat() #Getting current date.

                profile_name = nova_hub_json["packs"][code_name]["names"]["profile_name"]
                ver = nova_hub_json["packs"][code_name]["ver"]
                folder_name = nova_hub_json["packs"][code_name]["names"]["folder_name"]
                block_icon = nova_hub_json["packs"][code_name]["profile_block_icon"]
                mc_version = nova_hub_json["packs"][code_name]["mc_version"]
                default_java_args = nova_hub_json["packs"][code_name]["java_args"]

                mc_launcher.create_profile(None, code_name, profile_name + f" - v{ver}", folder_name, todays_date, block_icon=block_icon, mc_version_name=mc_version, java_args=default_java_args) #Creating profile

                t5=threading.Thread(target=finish, args=([t3])) #Finish Install thread
                t5.setDaemon(True)
                t5.start()

                t5.join()

                #Add installed mod pack to modpacks.json
                path = Nova_Dir.get_nova_universe_directory()
                with open(path + "\\#.nova_hub\\mod_packs.json", "r") as f: #Read
                    modpacks_json = json.load(f)

                modpacks_json[code_name] = {}
                modpacks_json[code_name]["ver"] = nova_hub_json["packs"][code_name]["ver"]

                with open(path + "\\#.nova_hub\\mod_packs.json", "w") as f: #Write
                    json.dump(modpacks_json, f)

                t9=threading.Thread(target=finish_effect)
                t9.setDaemon(True)
                t9.start()

            if popup_noti_return_value == False:
                popup_notification("ok", "Goose Anticheat", "You did not agree with our terms and conditions so you can not install the modpack.")

            thread = popup_notification("yes_no", "OptiFine", "Would you like to also install optifine for this modpack?")
            thread.join()

            if popup_noti_return_value == True: #Install Optifine
                download_optifine(code_name, nova_hub_json)

        t13=threading.Thread(target=install_thread)
        t13.setDaemon(True)
        t13.start()

    def update_modpack(modpack_frame, update_button, pack_image_frame, version_label, modpack_title, settings_button, code_name, run, nova_hub_json):
        global t12
        def finish_effect():
            time.sleep(2)
            
            progress.pack_forget()
            live_status_text.pack_forget()

            hex_colour = Color("#C06565")
            colours = list(hex_colour.range_to(Color("#00B6C0"), 40))

            hex_colour = Color("#C52612") #Text
            colours_text = list(hex_colour.range_to(Color("black"), 12))
            
            t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
            t8.setDaemon(True)
            t8.start()

            launch_image = Image.open(settings.path_to_images + "nova_hub_launch_button.png")

            width, height = launch_image.size
            
            actual_width = round(int(width)/14)
            actual_height = round(int(height)/14)

            launch_image = launch_image.resize((actual_width, actual_height))
            tkimage = ImageTk.PhotoImage(launch_image)
            launch_button = Button(modpack_frame, text="Launch", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#00B6C0", activebackground="#00B6C0", borderwidth=0, 
            cursor="hand2")
            launch_button.config()
            launch_button.photo = tkimage

            t8.join()
            launch_button.place(x=64, y=210)

        def update_thread():
            #Update Effect
            hex_colour = Color("#C06565")
            colours = list(hex_colour.range_to(Color("#00C03E"), 20))

            hex_colour = Color("#C52612") #Text
            colours_text = list(hex_colour.range_to(Color("black"), 12))

            #Delete old install script and download new one.
            delete_file(settings.path_to_installers + f"\\{code_name}")

            path_to_script = nova_hub_json["packs"][code_name]["files"]["script"]
            destination_path = download_modpack_file(code_name, path_to_script)

            extract_zip(destination_path + "\\script.zip")

            create_folder(settings.path_to_installers + f"\\{code_name}")

            move_files(destination_path + "\\script", settings.path_to_installers + f"\\{code_name}")

            clear_temp_folder()

            #Reinporting script.
            try:
                print_and_log(None, f"Importing {display_name} Script...")
                run = importlib.import_module(f"installers.{mod_pack}.run")

            except Exception as e:
                print_and_log("error", e)

            #Threads needed for update.
            try:
                t3=threading.Thread(target=run.run, args=(["UPDATE"])) #Run Installer thread.
                t3.setDaemon(True)
                t3.start()

                update_comfirmation = None

            except Exception as e:
                popup_notification("ok", "SCRIPT ERROR!", f"An error occured in the {display_name} script while updating, so we rolled back this update.")
                update_comfirmation = False

            t2=threading.Thread(target=live_run_status, args=([run, modpack_frame])) #Live Run Stats
            t2.setDaemon(True)
            t2.start()

            time.sleep(0.1)

            t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, update_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
            t8.setDaemon(True)
            t8.start()

            #Update mc launcher profile for mod pack.
            from datetime import datetime
            todays_date = datetime.now().isoformat() #Getting current date.

            profile_name = nova_hub_json["packs"][code_name]["names"]["profile_name"]
            ver = nova_hub_json["packs"][code_name]["ver"]
            folder_name = nova_hub_json["packs"][code_name]["names"]["folder_name"]
            block_icon = nova_hub_json["packs"][code_name]["profile_block_icon"]
            mc_version = nova_hub_json["packs"][code_name]["mc_version"]
            default_java_args = nova_hub_json["packs"][code_name]["java_args"]

            mc_launcher.create_profile(None, code_name, profile_name + f" - v{ver}", folder_name, todays_date, block_icon=block_icon, mc_version_name=mc_version, java_args=default_java_args) #Creating profile
            
            t5=threading.Thread(target=finish, args=([t3])) #Finish Install thread
            t5.setDaemon(True)
            t5.start()

            t5.join()
            
            if not update_comfirmation == False:
                #Update mod pack version in modpacks.json
                path = Nova_Dir.get_nova_universe_directory()
                with open(path + "\\#.nova_hub\\mod_packs.json", "r") as f: #Read
                    modpacks_json = json.load(f)

                modpacks_json[code_name] = {}
                modpacks_json[code_name]["ver"] = nova_hub_json["packs"][code_name]["ver"]

                with open(path + "\\#.nova_hub\\mod_packs.json", "w") as f: #Write
                    json.dump(modpacks_json, f)

                t9=threading.Thread(target=finish_effect)
                t9.setDaemon(True)
                t9.start()

        t14=threading.Thread(target=update_thread)
        t14.setDaemon(True)
        t14.start()

    def download_modpack_script(code_name, nova_hub_json):
        global t12
        def download_modpack_script_thread(code_name, nova_hub_json):
            display_name = nova_hub_json["packs"][code_name]["names"]["display_name"]
            thread = popup_notification("yes_no", f"Would you like to download the script for {display_name}?", "The script will allow you to install and manage the modpack.")
            thread.join()

            if popup_noti_return_value == True: #Download script.
                try:
                    path_to_script = nova_hub_json["packs"][code_name]["files"]["script"]
                    destination_path = download_modpack_file(code_name, path_to_script)

                    extract_zip(destination_path + "\\script.zip")

                    create_folder(settings.path_to_installers + f"\\{code_name}")

                    move_files(destination_path + "\\script", settings.path_to_installers + f"\\{code_name}")

                    clear_temp_folder()

                    installations_frame.pack_forget()

                    installations_menu(None, None)

                except KeyError as e:
                    print_and_log("error", e)
                    popup_notification("ok", "Script Download Unavailable", """The script for this modpack is currently unavailable. It could be unavailable becasuse of the following: the modpack is coming soon or something is wrong on our web servers. (There may be more indepth infomation in the logs.)""")
                    return False

                except ConnectionError as e:
                    print_and_log("error", e)
                    popup_notification("ok", "Script Download Failed", """The download failed. It could have failed becasuse of the following: you have no internet connect or our web servers are down. (There may be more indepth infomation in the logs.)""")
                    return False

                except Exception as e:
                    print_and_log("error", e)
                    thread = popup_notification("ok", "Script Download Failed", """The download failed but we are unsure what caused it. (There may be more indepth infomation in the logs.)""")
                    thread.join()

                    popup_notification("ok", "Reporting Bugs", "To report a bug, join our discord server and open a ticket and help will come right away. The Golden Pro: Sorry about there not being a quicker way to report these bugs, I'm currently working on making this process quicker.")

                    return False

        t12=threading.Thread(target=download_modpack_script_thread, args=([code_name, nova_hub_json]))
        t12.setDaemon(True)
        t12.start()

    #Drawing modpacks from web server. ---------------------------------

    if already_ran_api == True:
        nova_hub_json = get_nova_hub_json(save_the_api=True)

    if not already_ran_api == True:
        nova_hub_json = get_nova_hub_json()
        already_ran_api = True

    if nova_hub_json == False:
        popup_notification("ok", "API ERROR", "We could not connect to the Nova Hub API and we could not find any cached files.")

    modpack_list = nova_hub_json["packs"]

    for mod_pack in modpack_list:
        is_modpack_installed = False

        pack_version = nova_hub_json["packs"][mod_pack]["ver"]

        display_name = nova_hub_json["packs"][mod_pack]["names"]["display_name"]
        code_name = nova_hub_json["packs"][mod_pack]["names"]["code_name"]
        folder_name = nova_hub_json["packs"][mod_pack]["names"]["folder_name"]

        modpack_frame = Frame(installations_frame, width=264, height=280, bg="#282727")
        modpack_frame.grid(row=0, column=1 + amount_of_installers, padx=15, pady=15)

        #Mod Pack Banner
        try:
            Pack_Image = Image.open(requests.get(settings.api + settings.nova_hub_modpack_location + "/" + code_name + "/" + "banner.png", stream=True).raw)
        except Exception as e:
            try:
                global no_connection
                no_connection = True #Assume there is no internet.
                name_of_banner = nova_hub_json["packs"][mod_pack]["nova_hub_banner"]
                Pack_Image = Image.open(f".\\nova_api_cache\\{code_name}\\{name_of_banner}")
            except Exception as e:
                no_connection = False
                try:
                    Pack_Image = Image.open(requests.get(settings.api + settings.nova_hub_modpack_location + "/" + code_name + "/" + "banner.jpeg", stream=True).raw)
                except Exception as e:
                    Pack_Image = Image.open(settings.path_to_images + "no_banner.png")

        width, height = Pack_Image.size
        
        actual_width = round(int(width)/7.39)
        actual_height = round(int(height)/7.39)

        Pack_Image = Pack_Image.resize((actual_width, actual_height))
        tkimage = ImageTk.PhotoImage(Pack_Image)
        pack_image_frame = Label(modpack_frame, image=tkimage, bg="#282727", cursor="hand2")
        pack_image_frame.photo = tkimage
        pack_image_frame.place(x=0, y=0)

        #Title Label
        modpack_title_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
        modpack_title = Label(modpack_frame, text=display_name.upper().replace("_", " "), font=modpack_title_font, fg="#C52612", bg="#282727") #Where I left off
        modpack_title.place(x=0, y=150)

        #Version Label
        version_font = font.Font(family='Arial Rounded MT Bold', size=8, weight='bold', underline=False)
        version_label = Label(modpack_frame, text="V" + str(pack_version), font=version_font, fg="#C52612", bg="#282727") #Where I left off
        version_label.place(x=0, y=263)

        #Settings Button
        settings_image = Image.open(settings.path_to_images + "modpack_settings.png")

        width, height = settings_image.size
        
        actual_width = round(int(width)/28)
        actual_height = round(int(height)/28)

        settings_image = settings_image.resize((actual_width, actual_height))
        tkimage = ImageTk.PhotoImage(settings_image)
        settings_button = Button(modpack_frame, image=tkimage, bg="#282727", activebackground="#282727", borderwidth=0, cursor="hand2")
        settings_button.config(command=lambda installations_frame=installations_frame, display_name=display_name, folder_name=folder_name, code_name=code_name : 
        modpack_settings_menu(installations_frame, display_name, folder_name, code_name))
        settings_button.photo = tkimage
        settings_button.place(x=213, y=230) #Notice for later: Maybe add a rotaion effect to the settings icon.

        #Grey Install Button
        grey_install_image = Image.open(settings.path_to_images + "greyed_install_button.png")

        width, height = grey_install_image.size
        
        actual_width = round(int(width)/14)
        actual_height = round(int(height)/14)

        grey_install_image = grey_install_image.resize((actual_width, actual_height))
        tkimage = ImageTk.PhotoImage(grey_install_image)
        install_button = Button(modpack_frame, text="Install", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#282727", activebackground="#282727", borderwidth=0, 
        cursor="hand2")
        install_button.config(command=lambda code_name=code_name, nova_hub_json=nova_hub_json : download_modpack_script(code_name, nova_hub_json))
        install_button.photo = tkimage
        install_button.place(x=64, y=210)

        is_script_downloaded = check_modpack.is_script_downloaded(None, code_name)

        if is_script_downloaded == True:
            #Import run.py from script.
            print_and_log("info_2", f"Install script for {display_name} has been found.")

            try:
                print_and_log(None, f"Importing {display_name} Script...")
                run = importlib.import_module(f"installers.{mod_pack}.run")

            except Exception as e:
                print_and_log("error", e)
                delete_file(settings.path_to_installers + f"\\{mod_pack}")
                download_modpack_script(code_name, nova_hub_json)

                is_script_downloaded = check_modpack.is_script_downloaded(None, code_name)

            #Install Button
            install_image = Image.open(settings.path_to_images + "nova_hub_install_button.png")

            width, height = install_image.size
            
            actual_width = round(int(width)/14)
            actual_height = round(int(height)/14)

            install_image = install_image.resize((actual_width, actual_height))
            tkimage = ImageTk.PhotoImage(install_image)
            installs_button = Button(modpack_frame, text="Install", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#282727", activebackground="#C06565", borderwidth=0, 
            cursor="hand2")
            installs_button.config(command=lambda modpack_frame=modpack_frame, installs_button=installs_button, pack_image_frame=pack_image_frame, version_label=version_label, modpack_title=modpack_title, 
            settings_button=settings_button, mod_pack=mod_pack, run=run, nova_hub_json=nova_hub_json : install_modpack(modpack_frame, installs_button, pack_image_frame, version_label, modpack_title, 
            settings_button, mod_pack, run, nova_hub_json))
            installs_button.photo = tkimage
            installs_button.place(x=64, y=210)
            installs_button.bind("<Enter>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: install_button_hover_enter(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))
            installs_button.bind("<Leave>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: install_button_hover_leave(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))

        is_modpack_installed = check_modpack.is_installed(None, folder_name)
        does_modpack_need_update = check_modpack.need_update(None, code_name, nova_hub_json)

        if is_modpack_installed == True:
            hex_colour = Color("#171717")
            colours = list(hex_colour.range_to(Color("#00B6C0"), 40))

            hex_colour = Color("#C52612") #Text
            colours_text = list(hex_colour.range_to(Color("black"), 12))

            launch_image = Image.open(settings.path_to_images + "nova_hub_launch_button.png")

            width, height = launch_image.size
            
            actual_width = round(int(width)/14)
            actual_height = round(int(height)/14)

            launch_image = launch_image.resize((actual_width, actual_height))
            tkimage = ImageTk.PhotoImage(launch_image)
            installs_button = Button(modpack_frame, text="Launch", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#00B6C0", activebackground="#00B6C0", borderwidth=0, 
            cursor="hand2")
            installs_button.config(command=launch)
            installs_button.photo = tkimage
            installs_button.place(x=64, y=210)

            if not does_modpack_need_update == True:
                t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
                t8.setDaemon(True)
                t8.start()

            is_script_downloaded = check_modpack.is_script_downloaded(None, code_name)
            if is_script_downloaded == False:
                download_modpack_script(code_name, nova_hub_json)

        #Update checking
        if does_modpack_need_update == True:

            #Set update button.
            update_image = Image.open(settings.path_to_images + "nova_hub_update_button.png")

            width, height = update_image.size
            
            actual_width = round(int(width)/14)
            actual_height = round(int(height)/14)

            update_image = update_image.resize((actual_width, actual_height))
            tkimage = ImageTk.PhotoImage(update_image)
            update_button = Button(modpack_frame, text="Install", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#282727", activebackground="#C06565", borderwidth=0, 
            cursor="hand2")
            update_button.config(command=lambda modpack_frame=modpack_frame, update_button=update_button, pack_image_frame=pack_image_frame, version_label=version_label, modpack_title=modpack_title, 
            settings_button=settings_button, mod_pack=mod_pack, run=run, nova_hub_json=nova_hub_json : update_modpack(modpack_frame, update_button, pack_image_frame, version_label, modpack_title, 
            settings_button, mod_pack, run, nova_hub_json))
            update_button.photo = tkimage
            update_button.place(x=64, y=210)
            update_button.bind("<Enter>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: update_button_hover_enter(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))
            update_button.bind("<Leave>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: update_button_hover_leave(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))

        amount_of_installers +=1

    print_and_log()

def home_menu(button_used, previous_frame):
    global home_frame
    global current_frame

    reset_clickable(settings.button_list)

    make_unclickable(button_used)
    button_used.bind("<Enter>", button_hover_enter)
    button_used.bind("<Leave>", button_hover_leave)

    if not previous_frame == None:
        previous_frame.pack_forget()

    home_frame = Frame(main_frame, width=1280, height=720, bg="#171717") #Main App Frame
    home_frame.pack(fill=BOTH, expand=1)

    current_frame = home_frame

    news_feed_drawer(home_frame, "NOVA HUB NEWS FEED COMING SOON...", ("IMPORTANT"), "Goldy", (18, "May", "??? Seconds ago"), 
    emoji.emojize("News feed is currently being worked on..."))

    #webview_v2(home_frame, "https://novauniverse.net/api/private/hub/news_letter/")
    message = """
Nova Hub is an app that players can use to rapidly install Mod Packs for game modes on nova universe like Terra Smp. It allows for players to not worry about installing forge, optifine and all the mods required for play.

Furthermore it allows for modpacks to be automatically updated, viewing the latest news from the Nova Universe news feed, managing the minecraft clients/modpacks and even more features that will be added in the future.

NOTICE: Nova Hub is only compatible with Minecraft Launcher, if you do not have MC Launcher installed Nova Hub will fail to function properly.
    """

    #Welcome popup.
    with open(".\\popup_noti_cache.json", "r") as f:
        popup_noti_json = json.load(f)

    try:
        tutorial = popup_noti_json["tutorial"]
    except KeyError as e:
        tutorial = None

    if tutorial == None:
        thread = popup_notification("ok", "Welcome to Nova Hub!", message)
        thread.join()

    popup_noti_json["tutorial"] = False

    with open(".\\popup_noti_cache.json", 'w') as f:
        json.dump(popup_noti_json, f)
    
amount_of_news = 0

def app_settings_menu(button_used, previous_frame):
    global current_frame

    if not button_used == None: #Don't reset buttons if no button was used to get here.
        reset_clickable(settings.button_list)
    
    if not button_used == None:
        make_unclickable(button_used)
        button_used.bind("<Enter>", button_hover_enter)
        button_used.bind("<Leave>", button_hover_leave)

    if not previous_frame == None:
        previous_frame.pack_forget()

    app_settings_frame = Frame(main_frame, width=1280, height=720, bg="#1F1E1E")
    app_settings_frame.pack(fill=BOTH, expand=1)
    current_frame = app_settings_frame #Tells nav bar that this is the current frame being viewed.

    settings_title_font = font.Font(family='Arial Rounded MT Bold', size=30, weight='bold', underline=True)
    settings_title_label = Label(app_settings_frame, text="Nova Hub Settings", font=settings_title_font, fg="#C52612", bg="#1F1E1E", cursor="hand2")
    settings_title_label.pack(fill=X, pady=(10, 0))


    #Change .minecraft dirctory ------------------------------------------------
    dot_minecraft_dir_frame = Frame(app_settings_frame, width=400, height=80, bg="#171717")
    dot_minecraft_dir_frame.pack(fill=X, padx=20, pady=(30, 0))

    dmd_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    dmd_text_label = Label(dot_minecraft_dir_frame, text="1) Change '.minecraft' Directory", font=dmd_text_font, fg="#19F200", bg="#171717")
    dmd_text_label.pack(pady=(5, 0))

    def apply(e): #Edit user settings.json.
        value_in_box = e.get()

        if value_in_box == "":
            hub_settings.edit(None, "paths", ".mc_path", None)

        else:
            hub_settings.edit(None, "paths", ".mc_path", value_in_box)

    #Entry Box
    dmd_entry_box_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
    dmd_entry_box = Entry(dot_minecraft_dir_frame, font=dmd_entry_box_font, bg="#1F1E1E", fg="#8CE781")
    dmd_entry_box.pack(fill=X, padx=20, pady=5)

    if not hub_settings.read(None, "paths", ".mc_path") == None: #Fill up string with function that returns json objects from user_settings.json
        path = hub_settings.read(None, "paths", ".mc_path")
        dmd_entry_box.insert(0, path) #Insert path into entry box.

    dmd_apply_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    dmd_apply_button = Button(dot_minecraft_dir_frame, text="Apply", font=dmd_apply_button_font, bg="#171717", fg="#12AC00", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    dmd_apply_button.pack(side="right", padx=(5, 250), pady=5)
    dmd_apply_button.config(command=lambda e=dmd_entry_box : apply(e=dmd_entry_box))
    dmd_apply_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#4aff36": button_hover_enter(event, start_colour="#171717", end_colour="#4aff36"))
    dmd_apply_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#4aff36": button_hover_leave(event, end_colour="#171717", start_colour="#4aff36"))

    dmd_clear_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    dmd_clear_button = Button(dot_minecraft_dir_frame, text="Clear", font=dmd_clear_button_font, bg="#171717", fg="#12AC00", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    dmd_clear_button.config(command=lambda first=0, last=END : dmd_entry_box.delete(first=0, last=END))
    dmd_clear_button.pack(side="left", padx=(250, 5), pady=5)
    dmd_clear_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#ffffff": button_hover_enter(event, start_colour="#171717", end_colour="#ffffff"))
    dmd_clear_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#ffffff": button_hover_leave(event, end_colour="#171717", start_colour="#ffffff"))



    #Change mc launcher exe dirctory ------------------------------------------------
    mc_launcher_exe_frame = Frame(app_settings_frame, width=400, height=80, bg="#171717")
    mc_launcher_exe_frame.pack(fill=X, padx=20, pady=(30, 0))

    mcl_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    mcl_text_label = Label(mc_launcher_exe_frame, text="2) Change minecraft launcher executable\n location.", font=mcl_text_font, fg="#DE7931", bg="#171717")
    mcl_text_label.pack(pady=(5, 0))

    def mcl_apply(e): #Edit user settings.json.
        value_in_box = e.get()

        if value_in_box == "":
            hub_settings.edit(None, "paths", "mc_launcher_exe_path", None)

        else:
            hub_settings.edit(None, "paths", "mc_launcher_exe_path", value_in_box)

    #Entry Box
    mcl_entry_box_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
    mcl_entry_box = Entry(mc_launcher_exe_frame, font=mcl_entry_box_font, bg="#1F1E1E", fg="#AC5D26")
    mcl_entry_box.pack(fill=X, padx=20, pady=5)

    if not hub_settings.read(None, "paths", ".mc_path") == None: #Fill up string with function that returns json objects from user_settings.json
        path = hub_settings.read(None, "paths", ".mc_path")
        dmd_entry_box.insert(0, path) #Insert path into entry box.

    mcl_apply_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    mcl_apply_button = Button(mc_launcher_exe_frame, text="Apply", font=mcl_apply_button_font, bg="#171717", fg="#AC5D26", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    mcl_apply_button.pack(side="right", padx=(5, 250), pady=5)
    mcl_apply_button.config(command=lambda e=dmd_entry_box : mcl_apply(e=dmd_entry_box))
    mcl_apply_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#4aff36": button_hover_enter(event, start_colour="#171717", end_colour="#4aff36"))
    mcl_apply_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#4aff36": button_hover_leave(event, end_colour="#171717", start_colour="#4aff36"))

    mcl_clear_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    mcl_clear_button = Button(mc_launcher_exe_frame, text="Clear", font=mcl_clear_button_font, bg="#171717", fg="#AC5D26", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    mcl_clear_button.config(command=lambda first=0, last=END : dmd_entry_box.delete(first=0, last=END))
    mcl_clear_button.pack(side="left", padx=(250, 5), pady=5)
    mcl_clear_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#ffffff": button_hover_enter(event, start_colour="#171717", end_colour="#ffffff"))
    mcl_clear_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#ffffff": button_hover_leave(event, end_colour="#171717", start_colour="#ffffff"))


    coming_soon_font = font.Font(family='Arial Rounded MT Bold', size=25, weight='bold', underline=False)
    coming_soon_label = Label(app_settings_frame, text="Coming Soon", font=coming_soon_font, fg="white", bg="#171717")
    #coming_soon_label.pack(pady=10)



    #Open Log ------------------------------------------------
    open_logs_frame = Frame(app_settings_frame, width=400, height=80, bg="#171717")
    open_logs_frame.pack(fill=X, padx=20, pady=(30, 0))

    ol_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    ol_text_label = Label(open_logs_frame, text="3) Open Logs.", font=ol_text_font, fg="#F1F1F1", bg="#171717")
    ol_text_label.pack(pady=(5, 10))

    def open_log(txt_name): #Edit user settings.json.
        os.startfile(txt_name)

    ol_open_current_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    open_current_button = Button(open_logs_frame, text="Open Current Log", font=ol_open_current_button_font, bg="#85ff78", fg="grey", padx=10, pady=3, activebackground="#ffffff", borderwidth=0, 
    cursor="hand2")
    open_current_button.pack(side="right", padx=(5, 250), pady=(5, 12))
    log_file_name = print_and_log()
    open_current_button.config(command=lambda txt_name=log_file_name : open_log(txt_name=log_file_name))
    open_current_button.bind("<Enter>", lambda event, start_colour="#85ff78", end_colour="#ffffff": button_hover_enter(event, start_colour="#85ff78", end_colour="#ffffff"))
    open_current_button.bind("<Leave>", lambda event, end_colour="#85ff78", start_colour="#ffffff": button_hover_leave(event, end_colour="#85ff78", start_colour="#ffffff"))

    ol_all_logs_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    ol_all_logs_button = Button(open_logs_frame, text="All Logs", font=ol_all_logs_button_font, bg="#F04E3A", fg="grey", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    ol_all_logs_button.config(command=lambda txt_name=settings.path_to_logs : open_log(txt_name=settings.path_to_logs))
    ol_all_logs_button.pack(side="left", padx=(250, 5), pady=(5, 12))
    ol_all_logs_button.bind("<Enter>", lambda event, start_colour="#F04E3A", end_colour="#F0AF39": button_hover_enter(event, start_colour="#F04E3A", end_colour="#F0AF39"))
    ol_all_logs_button.bind("<Leave>", lambda event, end_colour="#F04E3A", start_colour="#F0AF39": button_hover_leave(event, end_colour="#F04E3A", start_colour="#F0AF39"))

def modpack_settings_menu(previous_frame, pack_name, pack_folder_name, code_name):
    if not previous_frame == None:
        previous_frame.pack_forget()

    for button in settings.button_list:
        if not button == installs_button:
            make_unclickable(button) #Disables all buttons.

    #Global Varibles
    stop_at_common_values = 0
    ma_checkbox_value = 0

    #Scrollbar ------------------------------------------------------------------------------------------
    outer_frame = Frame(main_frame, bg="#1F1E1E") #Main App Frame
    outer_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(outer_frame, bg="#1F1E1E", highlightthickness=0, relief='ridge')
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    #Adds mouse scrollwheel functionality...
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    scrollable_frame = Frame(canvas, bg="#1F1E1E")

    canvas.create_window((50, 0), window=scrollable_frame, anchor="nw")
    #---------------------------------------------------------------------------------------------------

    modpack_settings_frame = Frame(scrollable_frame, width=200, height=200, bg="#1F1E1E") #Main App Frame
    modpack_settings_frame.pack(fill=BOTH, padx=20, pady=15)

    def uninstall_modpack(modpack_frame, run, code_name):
        def finish_effect():
            time.sleep(2)
            
            #Destroy Live Run Status
            progress.pack_forget()
            live_status_text.pack_forget()

        def uninstall_modpack_thread():
            thread = popup_notification("yes_no", "Uninstall Modpack", f"Are you sure you want to uninstall {pack_name}?")
            thread.join()

            if popup_noti_return_value == True:
                uninstall_button.pack_forget()

                #Threads needed for uninstall.
                t3=threading.Thread(target=run.run, args=(["uninstall"])) #Run Installer thread.
                t3.setDaemon(True)
                t3.start()

                t2=threading.Thread(target=live_run_status, args=([run, modpack_settings_frame])) #Live Run Stats
                t2.setDaemon(True)
                t2.start()

                #Remove mod pack from modpacks.json
                path = Nova_Dir.get_nova_universe_directory()
                with open(path + "\\#.nova_hub\\mod_packs.json", "r") as f: #Read
                    modpacks_json = json.load(f)

                modpacks_json.pop(str(code_name), None)

                with open(path + "\\#.nova_hub\\mod_packs.json", "w") as f: #Write
                    json.dump(modpacks_json, f)

                t5=threading.Thread(target=finish, args=([t3, False])) #Finish Uninstall thread
                t5.setDaemon(True)
                t5.start()

                t9=threading.Thread(target=finish_effect)
                t9.setDaemon(True)
                t9.start()

                time.sleep(0.5)
                installations_menu(installs_button, outer_frame)

        t14=threading.Thread(target=uninstall_modpack_thread)
        t14.start()

    #Mod Pack Name
    pack_name_font = font.Font(family='Arial Rounded MT Bold', size=25, weight='bold', underline=False)
    pack_name_label = Label(modpack_settings_frame, text=pack_name.upper() + " SETTINGS", font=pack_name_font, fg="#D46757", bg="#282727", cursor="hand2")
    pack_name_label.pack(fill=X)

    #Back Button
    back_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
    back_button = Button(modpack_settings_frame, text="Back", font=back_button_font, padx=10, pady=5, fg="#D46757", bg="#171717", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: installations_menu(installs_button, outer_frame))
    back_button.pack(pady=10)
    back_button.bind("<Enter>", lambda event, start_colour="#171717": button_hover_enter(event, start_colour="#171717"))
    back_button.bind("<Leave>", lambda event, end_colour="#171717": button_hover_leave(event, end_colour="#171717"))



    #Memory Allocation Bar
    memory_allocation_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    memory_allocation_frame.pack(fill=X, padx=20, pady=0)

    ma_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    ma_text_label = Label(memory_allocation_frame, text="1) Memory Allocation (RAM)", font=ma_text_font, fg="#C52612", bg="#171717")
    ma_text_label.pack()

    def set_slider(value_to_set):
        ma_slider.set(int(value_to_set))

    def edit_ram_text(e):
        amount_of_ram = get_size(int(e))
        ma_ram_text_label.config(text=f"RAM USAGE: {str(amount_of_ram)}" + f"/{str(max_amount_of_ram)} (MAX)")

        #2GB, 3GB, 4GB, 6GB, 8GB, 10GB, 12GB, 16GB
        values_to_stop_at = [2147483648, 3221225472, 4294967296, 6442450944, 8589934592, 10737418240, 12884901888, 17179869184]

        stop_at_common_values = ma_checkbox_var.get()

        if int(stop_at_common_values) == 1: #1=True, 0=False
            for ram_value in values_to_stop_at:

                if math.isclose(ram_value, int(e), abs_tol=40000000) == True:
                    t11=threading.Thread(target=set_slider, args=([ram_value]))
                    t11.start()

                    time.sleep(0.1)

    #Slider
    ma_slider_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    ma_slider = Scale(memory_allocation_frame, font=ma_slider_font, fg="white", from_=1073741824, to=psutil.virtual_memory().total, length=500, sliderlength=40, orient=HORIZONTAL, 
    bg="#171717", troughcolor="#171717", cursor="hand2", activebackground="#C52612", highlightthickness=0, bd=3, showvalue=False, resolution=10000, command=edit_ram_text)
    ma_slider.pack(fill=X, padx=20, pady=5)

    #Stick to values check box
    ma_checkbox_var = IntVar()
    ma_checkbox_font = font.Font(family='Arial Rounded MT Bold', size=8, weight='bold', underline=False)
    ma_checkbox = Checkbutton(memory_allocation_frame, text="Stick to Common Values (ALPHA)", font=ma_checkbox_font, variable=ma_checkbox_var, bg="#171717", fg="#D46757", cursor="hand2", 
    activebackground="#171717")
    ma_checkbox.pack(padx=(570, 0), pady=(0, 0))
    #ma_checkbox.place(x=680, y=0)

    max_amount_of_ram = get_size(psutil.virtual_memory().total)
    
    #Replace these three lines with code that reads from mc launcher versions txt.
    amount_of_ram = get_size(2147483648) #2GB
    ma_slider.set(2147483648)
    stop_at_common_values = False

    ma_ram_text_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    ma_ram_text_label = Label(memory_allocation_frame, text=f"RAM USAGE: {str(amount_of_ram)}" + f"/{str(max_amount_of_ram)} (MAX)", font=ma_ram_text_font, fg="white", bg="#171717")
    ma_ram_text_label.pack()

    is_modpack_installed = check_modpack.is_installed(None, pack_folder_name)
    is_script_downloaded = check_modpack.is_script_downloaded(None, code_name)

    #Disable Ram Allocation (coming soon) (REMOVE THIS WHEN FEATURE IS DONE!)
    ma_slider.config(state="disabled") #Disable Slider.
    ma_text_label.config(text="Coming Soon!", fg="grey")
    ma_checkbox.config(text="Coming Soon...", fg="grey")
    ma_ram_text_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', overstrike=False)
    ma_ram_text_label.config(text="Coming Soon!", font=ma_ram_text_font, fg="grey")
    # ---------------------------------------------------------------------------------------------------------



    #Preload Shaders Settings -------------------------------------
    preload_shaders_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    preload_shaders_frame.pack(fill=X, padx=20, pady=(30, 0))

    ps_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    ps_text_label = Label(preload_shaders_frame, text="2) Preload Shaders (BETA)", font=ps_text_font, fg="#F4A236", bg="#171717")
    ps_text_label.pack()

    ps_description_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    ps_description_label = Label(preload_shaders_frame, text=f"Click the on/off switch to toggle shader preloading for {pack_name}.", font=ps_description_font, fg="#FFCF92", bg="#171717")
    ps_description_label.pack()

    #Toggle Feature
    on_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False) #Change to 15 size after feature done.
    on_button = Button(preload_shaders_frame, text="ON", font=on_button_font, bg="#6CD860", activebackground="#19FF00", borderwidth=0, pady=8, padx=12, 
    cursor="hand2")
    on_button.config(command=None)
    on_button.pack(side="left", padx=(20, 0), pady=(10, 20))
    on_button.bind("<Enter>", lambda event, start_colour="#6CD860", end_colour="#19FF00": button_hover_enter(event, start_colour="#6CD860", end_colour="#19FF00"))
    on_button.bind("<Leave>", lambda event, end_colour="#6CD860", start_colour="#19FF00": button_hover_leave(event, end_colour="#6CD860", start_colour="#19FF00"))

    #Disable Preload Shaders (coming soon) (REMOVE THIS WHEN FEATURE IS DONE!)
    on_button.config(state="disabled", text="Soon...") #Disable Button.



    #Migrate controls -------------------------
    migrate_controls_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    migrate_controls_frame.pack(fill=X, padx=20, pady=(30, 0))

    mc_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    mc_text_label = Label(migrate_controls_frame, text="3) Migrate Controls", font=mc_text_font, fg="#5CCFF4", bg="#171717")
    mc_text_label.pack()

    mc_description_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    mc_description_label = Label(migrate_controls_frame, text=f"This setting allows you to migrate your controls over to {pack_name}. \n(Will overwrite current {pack_name} controls)", font=mc_description_font, fg="#9FDFF3", bg="#171717")
    mc_description_label.pack()

    mc_migrate_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    mc_migrate_button = Button(migrate_controls_frame, text="Migrate", font=mc_migrate_button_font, bg="#9FDFF3", fg="white", padx=10, pady=3, activebackground="#5CCFF4", borderwidth=0, 
    cursor="hand2")
    mc_migrate_button.pack(pady=10)
    mc_migrate_button.config(command=None)
    mc_migrate_button.bind("<Enter>", lambda event, start_colour="#9FDFF3", end_colour="#5CCFF4": button_hover_enter(event, start_colour="#9FDFF3", end_colour="#5CCFF4"))
    mc_migrate_button.bind("<Leave>", lambda event, end_colour="#9FDFF3", start_colour="#5CCFF4": button_hover_leave(event, end_colour="#9FDFF3", start_colour="#5CCFF4"))

    #Disable Migrate controls (coming soon) (REMOVE THIS WHEN FEATURE IS DONE!)
    mc_migrate_button.config(state="disabled", text="Coming Soon") #Disable Button.


    #Download Optifine
    download_optifine_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    download_optifine_frame.pack(fill=X, padx=20, pady=(30, 0))

    op_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    op_text_label = Label(download_optifine_frame, text="4) Download OptiFine", font=op_text_font, fg="#C55812", bg="#171717")
    op_text_label.pack()

    op_description_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    op_description_label = Label(download_optifine_frame, text=f"Install OptiFine for {pack_name} here!", font=op_description_font, fg="#C57A4A", bg="#171717")
    op_description_label.pack()

    nova_hub_json = get_nova_hub_json(silent=True)

    op_download_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    op_download_button = Button(download_optifine_frame, text="Download", font=op_download_button_font, bg="#C57A4A", fg="white", padx=10, pady=3, activebackground="#C55812", borderwidth=0, 
    cursor="hand2")
    op_download_button.pack(pady=10)
    op_download_button.config(command=lambda code_name=code_name, nova_hub_json=nova_hub_json: download_optifine(code_name, nova_hub_json))
    op_download_button.bind("<Enter>", lambda event, start_colour="#C57A4A", end_colour="#C55812": button_hover_enter(event, start_colour="#C57A4A", end_colour="#C55812"))
    op_download_button.bind("<Leave>", lambda event, end_colour="#C57A4A", start_colour="#C55812": button_hover_leave(event, end_colour="#C57A4A", start_colour="#C55812"))

    is_optifine_installed = check_modpack.is_optifine_downloaded(None, code_name, nova_hub_json)
    if is_optifine_installed == True:
        op_download_button.config(state="disabled", text="Already Installed")

    #Java Args Bar
    java_args_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    java_args_frame.pack(fill=X, padx=20, pady=(30, 0))

    ja_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    ja_text_label = Label(java_args_frame, text="5) Java Arguments (For Advanced Users)", font=ja_text_font, fg="#C52612", bg="#171717")
    ja_text_label.pack()

    def apply(e):
        string_from_box = e.get()

        mc_launcher.edit_profile(None, code_name, display_name, "javaArgs", string_from_box)
    
    #Entry Box
    ja_entry_box_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
    ja_entry_box = Entry(java_args_frame, font=ja_entry_box_font, bg="#1F1E1E", fg="white")
    ja_entry_box.pack(fill=X, padx=20, pady=5)

    if is_modpack_installed == True:
        #Getting java arg from versions.json
        nova_hub_json = get_nova_hub_json(silent=True)
        display_name = nova_hub_json["packs"][code_name]["names"]["display_name"]

        javaArgs = mc_launcher.read_profile(None, code_name, display_name, "javaArgs")
        ja_entry_box.insert(0, javaArgs) #Insert java arg into entry box.

    ja_apply_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    ja_apply_button = Button(java_args_frame, text="Apply", font=ja_apply_button_font, bg="#171717", fg="#D46757", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    ja_apply_button.pack(side="right", padx=(5, 250), pady=5)
    ja_apply_button.config(command=lambda e=ja_entry_box : apply(e=ja_entry_box))
    ja_apply_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#4aff36": button_hover_enter(event, start_colour="#171717", end_colour="#4aff36"))
    ja_apply_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#4aff36": button_hover_leave(event, end_colour="#171717", start_colour="#4aff36"))

    ja_clear_button_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    ja_clear_button = Button(java_args_frame, text="Clear", font=ja_apply_button_font, bg="#171717", fg="#D46757", padx=10, pady=3, activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2")
    ja_clear_button.config(command=lambda first=0, last=END : ja_entry_box.delete(first=0, last=END))
    ja_clear_button.pack(side="left", padx=(250, 5), pady=5)
    ja_clear_button.bind("<Enter>", lambda event, start_colour="#171717", end_colour="#ffffff": button_hover_enter(event, start_colour="#171717", end_colour="#ffffff"))
    ja_clear_button.bind("<Leave>", lambda event, end_colour="#171717", start_colour="#ffffff": button_hover_leave(event, end_colour="#171717", start_colour="#ffffff"))



    #Uninstall Button
    if is_modpack_installed == True:

        #Import run.py from script.
        try:
            print_and_log(None, f"Importing {pack_name} Script...\n")
            run = importlib.import_module(f"installers.{code_name}.run")

        except Exception as e:
            print_and_log("error", e)
            pass

        if is_script_downloaded == True:
            uninstall_button_font = font.Font(family='Arial Rounded MT Bold', size=16, weight='bold', underline=False)
            uninstall_button = Button(modpack_settings_frame, text="Uninstall Modpack", font=uninstall_button_font, padx=15, pady=5, fg="#D46757", bg="#171717", activebackground="#FEBCBC", borderwidth=0, 
            cursor="hand2")
            uninstall_button.config(command=lambda modpack_settings_frame=modpack_settings_frame, run=run, code_name=code_name : uninstall_modpack(modpack_settings_frame, run, code_name))
            uninstall_button.pack(side="bottom", pady=(40, 5))
            uninstall_button.bind("<Enter>", lambda event, start_colour="#171717": button_hover_enter(event, start_colour="#171717"))
            uninstall_button.bind("<Leave>", lambda event, end_colour="#171717": button_hover_leave(event, end_colour="#171717"))

    #Stuff to disable if mod pack is not installed.
    if not is_modpack_installed == True:
        #Memory Allocation Bar
        ma_slider.config(state="disabled") #Disable Slider if mod pack is not installed.
        ma_text_label.config(fg="grey")
        ma_ram_text_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', overstrike=True)
        ma_ram_text_label.config(text="MOD PACK NOT INSTALLED", font=ma_ram_text_font, fg="grey")

        #Java Args
        ja_entry_box.config(state="disabled") #Disable Java Args entry box if mod pack is not installed.

        ja_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', overstrike=True)
        ja_text_label.config(fg="grey", font=ja_text_font)

        ja_clear_button.config(state="disabled")
        ja_apply_button.config(state="disabled")

        #Migrate controls
        mc_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', overstrike=True)
        mc_text_label.config(fg="grey", font=mc_text_font)

        mc_description_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', overstrike=True)
        mc_description_label.config(fg="grey", font=mc_description_font)

        mc_migrate_button.config(state="disabled")

        #Download Optifine
        op_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', overstrike=True)
        op_text_label.config(fg="grey", font=op_text_font)

        op_description_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', overstrike=True)
        op_description_label.config(fg="grey", font=op_description_font)

        op_download_button.config(state="disabled")

def webview(frame=None, url=None): #Wait untill module dev fixes issue.
    html_frame = HtmlFrame(frame)
    html_frame.load_website(url) #load a website
    html_frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window

def webview_v2(frame=None, url=None):
    headers = {'User-Agent': str(settings.app_name)}

    request = urllib.request.Request(
        url, 
        data=None, 
        headers=headers
    )

    website = urllib.request.urlopen(request)
    mybytes = website.read()
    html = mybytes.decode("utf8")
    website.close()

    web_label = HTMLLabel(frame, html=html)
    web_label.pack(fill="both")
    
def news_feed_drawer(frame, heading, news_tag, author_name, date_time, embeded_des):
    #frame = Tkinter frame to draw to.
    #heading = The title for the news. (Takes string)
    #news_tag = The tag at the top righy (Takes string)

    news_frame = Frame(frame, width=800, height=400, bg="#282727")
    news_frame.pack(pady=20)

    #Top Red Border
    red_bar = Frame(news_frame, width=800, height=40, bg="#9F1F0F", cursor="hand2")
    red_bar.place(x=0, y=0)

    #Heading
    heading_text_font = font.Font(family='Arial Rounded MT Bold', size=12, underline=False)
    heading_text = Label(red_bar, text=heading, font=heading_text_font, fg="white", bg="#9F1F0F")
    heading_text.place(x=10, y=6)

    #News Tag

    news_tag_colour = "grey"

    if news_tag.upper() == 'IMPORTANT':
        news_tag_colour = "#971B1B" #Red

    if news_tag.upper() == 'NEWS':
        news_tag_colour = "#4ACE4E" #Green

    if news_tag.upper() == 'UPDATE':
        news_tag_colour = "#F4A236" #Orange

    news_tag_font = font.Font(family='Arial Rounded MT Bold', size=10, underline=False)
    news_tag_text = Label(red_bar, text=news_tag.upper(), font=news_tag_font, fg="white", bg=news_tag_colour)
    news_tag_text.place(x=700, y=10)

    #Details Bar Border
    details_bar = Frame(news_frame, width=800, height=50, bg="#282727")
    details_bar.place(x=0, y=40)

    details_bar_line = Label(details_bar, text="???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????", fg="#424242", bg="#282727")
    details_bar_line.place(x=7, y=30)

    #Author Head
    head_image = Image.open(settings.path_to_images + "goldens_head.png") #Defult Head

    width, height = head_image.size
    
    actual_width = round(int(width)/8)
    actual_height = round(int(height)/9)

    head_image = head_image.resize((actual_width, actual_height))
    tkimage = ImageTk.PhotoImage(head_image)
    head_label = Label(details_bar, image=tkimage, bg="#282727")
    head_label.photo = tkimage
    head_label.place(x=3, y=9)

    #Author Label
    author_label_font = font.Font(family='Arial Rounded MT Bold', size=10, underline=False)
    author_label = Label(details_bar, text=author_name + " ??? ", font=author_label_font, fg="grey", bg="#282727")
    author_label.place(x=30, y=10)

    #Time ago Label
    time_label_font = font.Font(family='Arial Rounded MT Bold', size=10, underline=False)
    time_label = Label(details_bar, text=date_time[2], font=time_label_font, fg="grey", bg="#282727")
    time_label.place(x=81, y=10)

    #Date Box
    date_box = Frame(news_frame, width=40, height=60, bg="#9F1F0F")
    date_box.place(x=10, y=100)

    if len(str(date_time[0])) == 1:
        date_label_font = font.Font(family='Arial Rounded MT Bold', size=18, underline=False)
        date_label = Label(date_box, text=date_time[0], font=date_label_font, fg="white", bg="#9F1F0F")
        date_label.place(x=10, y=0)

    if len(str(date_time[0])) == 2:
        date_label_font = font.Font(family='Arial Rounded MT Bold', size=18, underline=False)
        date_label = Label(date_box, text=date_time[0], font=date_label_font, fg="white", bg="#9F1F0F")
        date_label.place(x=2.5, y=0)

    month_box = Frame(date_box, width=40, height=25, bg="#171717")
    month_box.place(x=0, y=35)

    month_label_font = font.Font(family='Arial Rounded MT Bold', size=12, underline=False)
    month_label = Label(month_box, text=date_time[1].upper(), font=month_label_font, fg="grey", bg="#171717")
    month_label.place(x=0, y=0)

    #News Embed Description
    embeded_description_frame = Frame(news_frame, width=730, height=300, bg="#282727")
    embeded_description_frame.place(x=60, y=90)

    embeded_des_font = font.Font(family='Arial Rounded MT Bold', size=13, underline=False)
    embeded_des_label = Label(embeded_description_frame, text=embeded_des, font=embeded_des_font, fg="#BDBDBD", bg="#282727", wraplength=740)
    embeded_des_label.pack()

def popup_notification(noti_type, title=None, message=None):
    noti_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    noti_font_title = font.Font(family='Arial Rounded MT Bold', size=20, weight='bold', underline=False)
    message_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)

    popup_noti_json = {}
    popup_noti_json["return_value"] = None
    popup_noti_json["tutorial"] = False

    with open(".\\popup_noti_cache.json", 'w') as f:
        json.dump(popup_noti_json, f)

    play_sound("popup_1.mp3", volume=0.5)

    def wait_for_response_thread():
        #Thread that is ran to pause application after message is displayed.

        def wait_for_response():
            global popup_noti_return_value

            while True:
                with open(".\\popup_noti_cache.json", "r") as f:
                    popup_noti_json = json.load(f)

                return_value = popup_noti_json["return_value"]

                time.sleep(0.00000000000001)

                if return_value is True:
                    noti_window.withdraw()
                    popup_noti_return_value = True
                    return True

                if return_value is False:
                    noti_window.withdraw()
                    popup_noti_return_value = False
                    return False

        wait_for_response()

    def noti_exit(return_val):
        popup_noti_json["return_value"] = return_val

        with open(".\\popup_noti_cache.json", 'w') as f:
            json.dump(popup_noti_json, f)

        return return_val

    if noti_type.lower() == "ok": #Okay prompt
        noti_window = Toplevel(bg="#171717", height=200, width=600)
        noti_window.resizable(False, False)
        noti_window.title(title)

        #Big Title
        title_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        title_label = Label(noti_window, text=title, font=noti_font_title, fg="#BDBDBD", bg="#171717", wraplength=600)
        title_label.pack(pady=0)

        #Message
        message_frame = Frame(noti_window, width=730, height=300, bg="#171717")
        message_frame.pack(padx=5)

        message_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        message_label = Label(message_frame, text=message, font=message_label_font, fg="#BDBDBD", bg="#171717", wraplength=700)
        message_label.pack()

        #Ok Button
        ok_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
        ok_button = Button(noti_window, text="Ok!", font=ok_button_font, padx=5, pady=5, fg="#D46757", bg="#171717", activebackground="#FEBCBC", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(True))
        ok_button.pack()
        ok_button.bind("<Enter>", lambda event, start_colour="#171717": button_hover_enter(event, start_colour="#171717"))
        ok_button.bind("<Leave>", lambda event, end_colour="#171717": button_hover_leave(event, end_colour="#171717"))

    if noti_type.lower() == "yes_no": #Yes and No Prompt
        noti_window = Toplevel(bg="#171717", height=200, width=600)
        noti_window.resizable(False, False)
        noti_window.title(title)

        #Big Title
        title_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        title_label = Label(noti_window, text=title, font=noti_font_title, fg="#BDBDBD", bg="#171717", wraplength=600)
        title_label.pack(pady=0)

        #Message
        message_frame = Frame(noti_window, width=730, height=300, bg="#171717")
        message_frame.pack(padx=5)

        message_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        message_label = Label(message_frame, text=message, font=message_label_font, fg="#BDBDBD", bg="#171717", wraplength=700)
        message_label.pack(pady=(10, 0))

        #Yes Button
        yes_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
        yes_button = Button(noti_window, text="Yes!", font=yes_button_font, padx=5, pady=5, fg="#D46757", bg="#00FF7F", activebackground="#FEBCBC", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(True))
        yes_button.pack(side="left", padx=(250, 5), pady=20)
        yes_button.bind("<Enter>", lambda event, start_colour="#00FF7F": button_hover_enter(event, start_colour="#00FF7F"))
        yes_button.bind("<Leave>", lambda event, end_colour="#00FF7F": button_hover_leave(event, end_colour="#00FF7F"))

        #No Button
        no_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
        no_button = Button(noti_window, text="No", font=no_button_font, padx=10, pady=5, fg="#D46757", bg="#971B1B", activebackground="#FEBCBC", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(False))
        no_button.pack(side="right", padx=(5, 250), pady=20)
        no_button.bind("<Enter>", lambda event, start_colour="#971B1B": button_hover_enter(event, start_colour="#971B1B"))
        no_button.bind("<Leave>", lambda event, end_colour="#971B1B": button_hover_leave(event, end_colour="#971B1B"))

    if noti_type.lower() == "agree_cancel": #Yes and No Prompt
        noti_window = Toplevel(bg="#171717", height=200, width=600)
        noti_window.resizable(False, False)
        noti_window.title(title)

        #Big Title
        title_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        title_label = Label(noti_window, text=title, font=noti_font_title, fg="#BDBDBD", bg="#171717", wraplength=600)
        title_label.pack(pady=0)

        #Message
        message_frame = Frame(noti_window, width=730, height=300, bg="#171717")
        message_frame.pack(padx=5)

        message_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)
        message_label = Label(message_frame, text=message, font=message_label_font, fg="#BDBDBD", bg="#171717", wraplength=700)
        message_label.pack(pady=(10, 0))

        #Yes Button
        yes_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
        yes_button = Button(noti_window, text="I Agree", font=yes_button_font, padx=5, pady=5, fg="#D46757", bg="#00FF7F", activebackground="#FEBCBC", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(True))
        yes_button.pack(side="left", padx=(250, 5), pady=20)
        yes_button.bind("<Enter>", lambda event, start_colour="#00FF7F": button_hover_enter(event, start_colour="#00FF7F"))
        yes_button.bind("<Leave>", lambda event, end_colour="#00FF7F": button_hover_leave(event, end_colour="#00FF7F"))

        #No Button
        no_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
        no_button = Button(noti_window, text="Cancel", font=no_button_font, padx=10, pady=5, fg="#D46757", bg="#971B1B", activebackground="#FEBCBC", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(False))
        no_button.pack(side="right", padx=(5, 250), pady=20)
        no_button.bind("<Enter>", lambda event, start_colour="#971B1B": button_hover_enter(event, start_colour="#971B1B"))
        no_button.bind("<Leave>", lambda event, end_colour="#971B1B": button_hover_leave(event, end_colour="#971B1B"))

    t11=threading.Thread(target=wait_for_response_thread)
    t11.setDaemon(True)
    t11.start()

    return t11

def finish(thread_to_wait_for, open_mc_launcher=True):

    thread_to_wait_for.join()

    if not open_mc_launcher == False:
        subprocess.Popen(settings.path_to_mc_launcher_exe, stdout=subprocess.PIPE, creationflags=0x08000000)

def refresh_modpacks():
    global already_ran_api
    already_ran_api = False

    installations_menu(None, installations_frame)

def button_hover_enter(e, start_colour=None, end_colour=None):

    if start_colour == None:
        hex_colour = Color("#1F1E1E")
    else:
        hex_colour = Color(start_colour)
    
    if end_colour == None:
        colours = list(hex_colour.range_to(Color("#C06565"),10))
    else:
        colours = list(hex_colour.range_to(Color(end_colour),10))
    
    t7=threading.Thread(target=color_glow_effect, args=([e, colours]))
    t7.setDaemon(True)
    t7.start()

    play_sound("hover_1.wav", volume=0.1)

def button_hover_leave(e, start_colour=None, end_colour=None):
    if start_colour == None:
        hex_colour = Color("#C06565")
    else:
        hex_colour = Color(start_colour)
    
    if end_colour == None:
        colours = list(hex_colour.range_to(Color("#1F1E1E"),10))
    else:
        colours = list(hex_colour.range_to(Color(end_colour),10))

    t7=threading.Thread(target=color_glow_effect, args=([e, colours]))
    t7.setDaemon(True)
    t7.start()

def make_unclickable(button):
    if button["state"] == "normal":
        button["state"] = "disabled"
    else:
        button["state"] = "normal"

def reset_clickable(button_list):
    for button in button_list:
        button["state"] = "normal"

def color_glow_effect(e, hex_list):

    for color in hex_list:
        time.sleep(0.01)
        e.widget['background'] = '{}'.format(color)

def play_sound(sound, volume=1.0):

    def play_sound_thread():
        pygame.init()
        pygame.mixer.init()
        sound_ = pygame.mixer.Sound(settings.path_to_assets + sound)
        sound_.set_volume(volume) #Set's volume
        sound_.play()

        #from playsound import playsound
        #playsound(settings.path_to_assets + sound)

    t8=threading.Thread(target=play_sound_thread)
    t8.start()

def add_image_shadow(image, iterations, border, offset, backgroundColour, shadowColour):
    # image: base image to give a drop shadow
    # iterations: number of times to apply the blur filter to the shadow
    # border: border to give the image to leave space for the shadow
    # offset: offset of the shadow as [x,y]
    # backgroundCOlour: colour of the background
    # shadowColour: colour of the drop shadow
    
    #Calculate the size of the shadow's image
    fullWidth  = image.size[0] + abs(offset[0]) + 2*border
    fullHeight = image.size[1] + abs(offset[1]) + 2*border
    
    #Create the shadow's image. Match the parent image's mode.
    shadow = Image.new(image.mode, (fullWidth, fullHeight), backgroundColour)
    
    # Place the shadow, with the required offset
    shadowLeft = border + max(offset[0], 0) #if <0, push the rest of the image right
    shadowTop  = border + max(offset[1], 0) #if <0, push the rest of the image down
    #Paste in the constant colour
    shadow.paste(shadowColour, 
                [shadowLeft, shadowTop,
                 shadowLeft + image.size[0],
                 shadowTop  + image.size[1] ])
    
    # Apply the BLUR filter repeatedly
    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    # Paste the original image on top of the shadow 
    imgLeft = border - min(offset[0], 0) #if the shadow offset was <0, push right
    imgTop  = border - min(offset[1], 0) #if the shadow offset was <0, push down
    shadow.paste(image, (imgLeft, imgTop))

    return shadow

def logo_brething_effect(Nova_Logo, Nova_Logo_0, logo_label, actual_width, actual_height):
    logo_size_1 = Nova_Logo.resize((actual_width, actual_height))
    size = 1.001
    logo_size_2 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.002
    logo_size_3 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.003
    logo_size_4 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.004
    logo_size_5 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.005
    logo_size_6 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.006
    logo_size_7 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.007
    logo_size_8 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.008
    logo_size_9 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.009
    logo_size_10 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.010
    logo_size_11 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.011
    logo_size_12 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.012
    logo_size_13 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.013
    logo_size_14 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.014
    logo_size_15 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.015
    logo_size_16 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.016
    logo_size_17 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.017
    logo_size_18 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.018
    logo_size_19 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.019
    logo_size_20 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.020
    logo_size_21 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.021
    logo_size_22 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.022
    logo_size_23 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.023
    logo_size_24 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.024
    logo_size_25 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))

    sizes_list_2 = [Nova_Logo_0, logo_size_1, logo_size_2, logo_size_3, logo_size_4, logo_size_5, logo_size_6, logo_size_7, logo_size_8, logo_size_9,
    logo_size_10, logo_size_11, logo_size_12, logo_size_13, logo_size_14, logo_size_15, logo_size_16, logo_size_17, logo_size_18, logo_size_19, logo_size_20, logo_size_21,
    logo_size_22, logo_size_23, logo_size_24, logo_size_25] + [logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, 
    logo_size_25, logo_size_25, logo_size_25]

    sizes_list_2.reverse()

    sizes_list = [Nova_Logo_0, logo_size_1, logo_size_2, logo_size_3, logo_size_4, logo_size_5, logo_size_6, logo_size_7, logo_size_8, logo_size_9,
    logo_size_10, logo_size_11, logo_size_12, logo_size_13, logo_size_14, logo_size_15, logo_size_16, logo_size_17, logo_size_18, logo_size_19, logo_size_20, logo_size_21,
    logo_size_22, logo_size_23, logo_size_24, logo_size_25] + [logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, logo_size_25, 
    logo_size_25, logo_size_25, logo_size_25] + sizes_list_2

    while True:

        for logo in sizes_list:
            time.sleep(0.03)
            tkimage = ImageTk.PhotoImage(logo)
            logo_label.config(image=tkimage)
            logo_label.photo = tkimage

def logo_brething_effect_v2(Nova_Logo, Nova_Logo_0, logo_label, actual_width, actual_height):

    first_logo_size = Nova_Logo.resize((actual_width, actual_height))

    size_list_norm = []
    sizes_list_normal = [Nova_Logo_0]

    for x in range(1000):
        if not x == 0:
            size = 1.000 + float(f'0.0{x}')
            print (size) #Debug
            size_list_norm.append(size)
            logo_size = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
            sizes_list_normal.append(logo_size)

    size_list_rev = size_list_norm
    size_list_rev.reverse()

    sizes_list_reverse = sizes_list_normal
    sizes_list_reverse.reverse()

    sizes_list = sizes_list_normal + sizes_list_reverse

    size_list = size_list_norm + size_list_rev
    print (size_list)

    while True:

        '''
        for logo in sizes_list:
            time.sleep(0.0001)
            print (logo)
            tkimage = ImageTk.PhotoImage(logo)
            logo_label.config(image=tkimage)
            logo_label.photo = tkimage

        '''

    '''
    logo_size_1 = Nova_Logo.resize((actual_width, actual_height))
    size = 1.001
    logo_size_2 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.002
    logo_size_3 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.003
    logo_size_4 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.004
    logo_size_5 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.005
    logo_size_6 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.006
    logo_size_7 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.007
    logo_size_8 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.008
    logo_size_9 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.009
    logo_size_10 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.010
    logo_size_11 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.011
    logo_size_12 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.012
    logo_size_13 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.013
    logo_size_14 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.014
    logo_size_15 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.015
    logo_size_16 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.016
    logo_size_17 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.017
    logo_size_18 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.018
    logo_size_19 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.019
    logo_size_20 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.020
    logo_size_21 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.021
    logo_size_22 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.022
    logo_size_23 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.023
    logo_size_24 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    size = 1.024
    logo_size_25 = Nova_Logo.resize((round(actual_width*size), round(actual_height*size)))
    '''

def open_url(url=None):
    if not type(url) == type(""):
        url = settings.nova_universe_url

    webbrowser.open_new_tab(url)

def launch(option=None):
    def open_mc_launcher():
        open_mc_launcher = True

        if not open_mc_launcher == False:
            subprocess.Popen(settings.path_to_mc_launcher_exe, stdout=subprocess.PIPE, creationflags=0x08000000)
    
    if option == None:
        option = "mcl"

    if option.lower() == "mcl":
        t10=threading.Thread(target=open_mc_launcher)
        t10.setDaemon(True)
        t10.start()

def app_close():
    global lrs
    print ("\u001b[36m[Protocal Close App]")
    print ("Stoping App Processes...")
    print ("")

    lrs = False
    print ("[Thread 2: Live Installer Status Feed] Stopped")

    #This thread is killed automatically.
    print ("[Thread 5: Finish Thread] Stopped")

    print ("[DONE]\u001b[0m")

    try:
        window.destroy()
        sys.exit()
        time.sleep(1)
        sys.exit()
        sys.exit()
        raise SystemExit

    except RuntimeError as e:
        pass

def start_up():
    nav_bar() #Loads everything

t1=threading.Thread(target=start_up)
t1.setDaemon(True)

window = Tk()

main_canvas = Canvas(window)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
main_frame.pack(fill=BOTH, expand=1)

window.title(app_name)
window.iconbitmap(settings.path_to_images + "icon.ico")

window.geometry('900x600')
#window.resizable(False, False) #Makes window not resizeable

window.protocol("WM_DELETE_WINDOW", app_close)

t1.start() #App startup runs within this function!

if __name__ == '__main__':
    #Run nova__hub warning.
    warning_font = font.Font(family='Arial Rounded MT Bold', size=11, weight='bold', underline=False)
    warning_label = Label(main_frame, text=":( Please run Nova_Hub.exe/py when launching Nova Hub instead of just attempting to run the app.py.", font=warning_font, fg="#C52612", bg="#282727")
    warning_label.pack(fill=BOTH)

#window.withdraw() #Removes console
window.mainloop()

'''
Nova Hub Color Pallet

1st Color: #0D1C30
2nd Color: #354C51
3rd Color: #13472D
4rd Color: #67E6B0

'''
#Black: \u001b[30m
#Red: \u001b[31m
#Green: \u001b[32m
#Yellow: \u001b[33m
#Blue: \u001b[34m
#Magenta: \u001b[35m
#Cyan: \u001b[36m
#White: \u001b[37m
#Reset: \u001b[0m

news_list = {
    "news_1":{
        "title": "hello, this a test title",
        "text_string_1": "Hi, Nova Universe community! This is me testing out the nova hub news description.",
        "image_url": "https://media.discordapp.net/attachments/759051040389201935/826132923882668052/Goldy_Colours_Banner.png"

    }
}

#Discord car drip - https://youtu.be/6U6EPxchhSU
#(Yes here's some more drip for you...)