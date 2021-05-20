import os
from tkinter import *
from tkinter import ttk
#from ttkthemes import themed_tk as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image, ImageFilter
import tkinter.font as font
import threading
import time
import subprocess
from colour import Color
import webbrowser
import json
import importlib
from tkinterweb import HtmlFrame
import urllib.request
import requests
from tkhtmlview import HTMLLabel
import emoji
import psutil

import settings
from nova_func import *

import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

app_name = settings.app_name

ver_v = "V" + str(settings.version)

lrs = False #Turns Live Status Thread off.
live_installer_status = "Starting Live Install Status Thread..."

downloaded_modpacks = {}
downloaded_modpacks['modpacks'] = {}

installs_button = None #Installs button needs to be global so I can choose not disble it when I'm looping through all of them in mod pack settings menu.

def live_run_status(run, modpack_frame): #Updates
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
    progress.pack(pady=10)
    
    while lrs == True:
        live_installer_status = run.live_installer_status

        live_status_text.config(text=live_installer_status)

        progress['value'] = run.live_installer_progress_bar

        time.sleep(0.06)

'''
t3=threading.Thread(target=run.run) #Run thread.
t3.setDaemon(True)

t4=threading.Thread(target=run.run, args=(["RESTORE_FORGE"])) #Restore Forge Run thread.
t4.setDaemon(True)
'''

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
    t6.start()

    buttons_bar = Frame(nav_bar, width=10, height=30, bg="#9F1F0F") #NavBar
    buttons_bar.pack(side="top", fill=BOTH)

    #Home Button
    home_button = Button(buttons_bar, text="Home", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: home_menu(home_button, installations_frame)) 
    home_button.grid(row=0, column=1, padx=15)
    home_button.bind("<Enter>", button_hover_enter)
    home_button.bind("<Leave>", button_hover_leave)

    home_menu(home_button, None)
    
    #Installations Button
    installs_button = Button(buttons_bar, text="Installations", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: installations_menu(installs_button, home_frame))
    installs_button.grid(row=0, column=2)
    installs_button.bind("<Enter>", button_hover_enter)
    installs_button.bind("<Leave>", button_hover_leave)

    settings.button_list = [home_button, installs_button]

def installations_menu(button_used, previous_frame):
    global installations_frame
    global progress
    global live_status_text

    reset_clickable(settings.button_list)

    make_unclickable(button_used)
    button_used.bind("<Enter>", button_hover_enter)
    button_used.bind("<Leave>", button_hover_leave)

    if not previous_frame == None:
        previous_frame.pack_forget()

    installations_frame = Frame(main_frame, width=1280, height=720, bg="#171717")
    installations_frame.pack(fill=BOTH, expand=1)

    amount_of_installers = 0

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

    def install_button_hover_leave(e, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button):
        hex_colour = Color("#C06565")
        colours = list(hex_colour.range_to(Color("#282727"), 20))

        hex_colour = Color("black") #Text
        colours_text = list(hex_colour.range_to(Color("#C52612"), 20))
        
        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, e, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

    def install_modpack(modpack_frame, installs_button, pack_image_frame, version_label, modpack_title, settings_button, installer, run, run_option):
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
            launch_button.place(x=53, y=180)

        with open(settings.path_to_installers + installer + "\\#.nova_hub" + "\\" + "data.json", "r") as f:
            data_json = json.load(f)

        #Install Effect
        hex_colour = Color("#C06565")
        colours = list(hex_colour.range_to(Color("#00C03E"), 20))

        hex_colour = Color("#C52612") #Text
        colours_text = list(hex_colour.range_to(Color("black"), 12))

        #Threads needed for install.
        t3=threading.Thread(target=run.run, args=([run_option])) #Run Installer thread.
        t3.setDaemon(True)
        t3.start()

        t2=threading.Thread(target=live_run_status, args=([run, modpack_frame])) #Live Run Stats
        t2.setDaemon(True)
        t2.start()

        time.sleep(0.1)

        t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
        t8.setDaemon(True)
        t8.start()

        t5=threading.Thread(target=finish, args=([t3])) #Finish Install thread
        t5.setDaemon(True)
        t5.start()

        t9=threading.Thread(target=finish_effect)
        t9.setDaemon(True)
        t9.start()

        data_json["installed"] = True

        with open (settings.path_to_installers + installer + "\\#.nova_hub" + "\\" + "data.json", "w") as f:
            json.dump(data_json, f)

    #Drawing modpacks from web server.

    with urllib.request.urlopen(settings.api + settings.nova_hub_json_location) as url:
        nova_hub_json = json.loads(url.read().decode())

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
        settings_button.config(command=lambda installations_frame=installations_frame, display_name=display_name, folder_name=folder_name : 
        modpack_settings_menu(installations_frame, display_name, folder_name))
        settings_button.photo = tkimage
        settings_button.place(x=213, y=230)

        #Grey Install Button
        grey_install_image = Image.open(settings.path_to_images + "greyed_install_button.png")

        width, height = grey_install_image.size
        
        actual_width = round(int(width)/14)
        actual_height = round(int(height)/14)

        grey_install_image = grey_install_image.resize((actual_width, actual_height))
        tkimage = ImageTk.PhotoImage(grey_install_image)
        install_button = Button(modpack_frame, text="Install", image=tkimage, font=("Arial Bold", 16), fg="white", bg="#282727", activebackground="#282727", borderwidth=0, 
        cursor="hand2")
        install_button.config(command=None)
        install_button.photo = tkimage
        install_button.place(x=64, y=210)

        is_script_downloaded = check_modpack.is_script_downloaded(None, code_name)

        if is_script_downloaded == True:
            #Import run.py from script.
            print_and_log("info_2", f"Install script for {display_name} has been found.")

            try:
                print_and_log(None, f"Importing {display_name} Script...\n")
                run = importlib.import_module(f"installers.{mod_pack}.run")

            except Exception as e:
                print_and_log("error", e)
                #Where I left off (20/05/2021)
                pass

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
            settings_button=settings_button, mod_pack=mod_pack, run=run, run_option="NORMAL" : install_modpack(modpack_frame, installs_button, pack_image_frame, version_label, modpack_title, settings_button, mod_pack, run, "NORMAL"))
            installs_button.photo = tkimage
            installs_button.place(x=64, y=210)
            installs_button.bind("<Enter>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: install_button_hover_enter(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))
            installs_button.bind("<Leave>", lambda event, modpack_frame=modpack_frame, pack_image_frame=pack_image_frame, 
            modpack_title=modpack_title, version_label=version_label, settings_button=settings_button: install_button_hover_leave(event, modpack_frame, pack_image_frame, modpack_title, version_label, settings_button))

        #Notice for later: Maybe add a rotaion effect to the settings icon.

        is_modpack_installed = check_modpack.is_installed(None, folder_name)

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

            t8=threading.Thread(target=modpack_glow_effect, args=([modpack_frame, installs_button, pack_image_frame, modpack_title, version_label, settings_button, colours, colours_text]))
            t8.setDaemon(True)
            t8.start()

        amount_of_installers =+ 1
        downloaded_modpacks['modpacks'][mod_pack.lower()] = {} #Adds installer to avalible modpacks list.
        downloaded_modpacks['modpacks'][mod_pack.lower()]['ver'] = pack_version

        t3=threading.Thread(target=modpack_updater, args=(["NORMAL"]))
        t3.start()

def home_menu(button_used, previous_frame):
    global home_frame

    reset_clickable(settings.button_list)

    make_unclickable(button_used)
    button_used.bind("<Enter>", button_hover_enter)
    button_used.bind("<Leave>", button_hover_leave)

    if not previous_frame == None:
        previous_frame.pack_forget()

    home_frame = Frame(main_frame, width=1280, height=720, bg="#171717") #Main App Frame
    home_frame.pack(fill=BOTH, expand=1)

    #news_feed_drawer(home_frame, "Help me, I've been coding for 4 hours.", ("IMPORTANT"), "Goldy", (19, "May", "10 Seconds ago"), 
    #"I honestly think zeeraa should give me all his dogecoin in return of coding this app. I will spend it very wisely :D ")

    news_feed_drawer(home_frame, "NOVA HUB NEWS FEED COMING SOON...", ("IMPORTANT"), "Goldy", (18, "May", "∞ Seconds ago"), 
    emoji.emojize("Zzzz.. Currently waiting for Zeeraa to finish the news letter system."))

    #webview_v2(home_frame, "https://novauniverse.net/api/private/hub/news_letter/")

amount_of_news = 0

def modpack_settings_menu(previous_frame, pack_name, pack_folder_name):
    if not previous_frame == None:
        previous_frame.pack_forget()

    for button in settings.button_list:
        if not button == installs_button:
            make_unclickable(button) #Disables all buttons.

    modpack_settings_frame = Frame(main_frame, width=200, height=200, bg="#1F1E1E") #Main App Frame
    modpack_settings_frame.pack(fill=BOTH, expand=2, padx=20, pady=15)

    #Mod Pack Name
    pack_name_font = font.Font(family='Arial Rounded MT Bold', size=25, weight='bold', underline=False)
    pack_name_label = Label(modpack_settings_frame, text=pack_name.upper() + " SETTINGS", font=pack_name_font, fg="#D46757", bg="#282727")
    pack_name_label.pack(fill=X)

    #Back Button
    back_button_font = font.Font(family='Arial Rounded MT Bold', size=12, weight='bold', underline=False)
    back_button = Button(modpack_settings_frame, text="Back", font=back_button_font, padx=10, pady=5, fg="#D46757", bg="#171717", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=lambda: installations_menu(installs_button, modpack_settings_frame))
    back_button.pack(pady=10)
    back_button.bind("<Enter>", lambda event, start_colour="#171717": button_hover_enter(event, start_colour="#171717"))
    back_button.bind("<Leave>", lambda event, end_colour="#171717": button_hover_leave(event, end_colour="#171717"))

    #Memory Allocation Bar
    memory_allocation_frame = Frame(modpack_settings_frame, width=400, height=80, bg="#171717")
    memory_allocation_frame.pack(fill=X, padx=20, pady=0)

    ma_text_font = font.Font(family='Arial Rounded MT Bold', size=15, weight='bold', underline=False)
    ma_text_label = Label(memory_allocation_frame, text="Memory Allocation (RAM)", font=ma_text_font, fg="#C52612", bg="#171717")
    ma_text_label.pack()

    def edit_ram_text(e):
        amount_of_ram = get_size(int(e))
        ma_ram_text_label.config(text=f"RAM USAGE: {str(amount_of_ram)}" + f"/{str(max_amount_of_ram)} (MAX)")

    ma_slider_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    ma_slider = Scale(memory_allocation_frame, font=ma_slider_font, fg="white", from_=1073741824, to=psutil.virtual_memory().total, length=500, sliderlength=40, orient=HORIZONTAL, 
    bg="#171717", troughcolor="#171717", cursor="hand2", activebackground="#C52612", highlightthickness=0, bd=3, showvalue=False, command=edit_ram_text)
    ma_slider.pack(fill=X, padx=20, pady=5)

    max_amount_of_ram = get_size(psutil.virtual_memory().total)
    
    #2GB #Replace these two lines with code that reads from mc launcher versions txt.
    amount_of_ram = get_size(2147483648) 
    ma_slider.set(2147483648)

    ma_ram_text_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', underline=False)
    ma_ram_text_label = Label(memory_allocation_frame, text=f"RAM USAGE: {str(amount_of_ram)}" + f"/{str(max_amount_of_ram)} (MAX)", font=ma_ram_text_font, fg="white", bg="#171717")
    ma_ram_text_label.pack()

    is_modpack_installed = check_modpack.is_installed(None, pack_folder_name)



    #Stuff to disable if mod pack is not installed.
    if not is_modpack_installed == True:
        #Memory Allocation Bar
        ma_slider.config(state="disabled") #Disable Slider if mod pack is not installed.
        ma_ram_text_font = font.Font(family='Arial Rounded MT Bold', size=10, weight='bold', overstrike=True)
        ma_ram_text_label.config(text="MOD PACK NOT INSTALLED", font=ma_ram_text_font, fg="grey")



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

    details_bar_line = Label(details_bar, text="─────────────────────────────────────────────────────────────────", fg="#424242", bg="#282727")
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
    author_label = Label(details_bar, text=author_name + " • ", font=author_label_font, fg="grey", bg="#282727")
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

def finish(thread_to_wait_for):

    thread_to_wait_for.join()
    open_mc_launcher = True

    if not open_mc_launcher == False:
        subprocess.Popen(settings.path_to_mc_launcher_exe, stdout=subprocess.PIPE, creationflags=0x08000000)

    close_button = Button(main_frame, text="Close!", font=("Arial Bold", 12), padx=5, pady=1, fg="#E1D8D8", bg="#8A0004", 	
    activebackground="#13472D", command=app_close)   
    #close_button.pack(side=BOTTOM)

def modpack_updater(option=None):
    def check_modpacks_for_update():

        #Check for updates.
        for mod_pack in downloaded_modpacks['modpacks']:

            #Look for that modpack's current version on webserver.
            with urllib.request.urlopen(settings.api + settings.nova_hub_json_location) as url:
                data_json = json.loads(url.read().decode())
                ver = data_json['packs'][mod_pack]['ver']

            #Decide if it needs an update or not.
            if int(ver) > int(downloaded_modpacks['modpacks'][mod_pack]['ver']):

                #Update the pack.
                download_update()

    def download_update():
        #Where I left off
        pass

    if option == None:
        option = "NORMAL"

    if option.upper() == "NORMAL":
        #Check all modpacks for updates.
        check_modpacks_for_update()
        pass
        
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

def play_sound(sound):
    pass

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
    nav_bar() #Loads Nav Bar

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