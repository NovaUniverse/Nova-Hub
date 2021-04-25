import os
from tkinter import *
from tkinter import ttk
#from ttkthemes import themed_tk as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import threading
import time
import subprocess
from colour import Color
import webbrowser

import settings

app_name = settings.app_name

ver_v = "V" + str(settings.version)

live_installer_status = "Starting Live Install Status Thread..."

lrs = False #Turns Live Status Thread off.

def live_run_status(): #Updates
    global live_installer_status
    global lrs

    lrs = True
    
    while lrs == True:
        live_installer_status = run.live_installer_status

        live_status_text = Label(main_frame, text=live_installer_status, font=("Arial Bold", 20), fg="#E1D8D8", 
        pady=12, bg="#171717", wraplength=780)
        live_status_text.config(anchor=CENTER)
        live_status_text.pack()

        s = ttk.Style() #Apply Theme
        s.theme_use('clam')
        s.configure("terra.Horizontal.TProgressbar", foreground='#E1D8D8', background='#FF0000')

        progress = Progressbar(main_frame, style="terra.Horizontal.TProgressbar", orient=HORIZONTAL, length=600, mode='determinate')
        progress['value'] = run.live_installer_progress_bar
        progress.pack()

        time.sleep(0.06)
        
        progress.pack_forget()
        live_status_text.pack_forget()

        if lrs == False:
            sys.exit()

t2=threading.Thread(target=live_run_status)
t2.setDaemon(True)

'''
t3=threading.Thread(target=run.run) #Run thread.
t3.setDaemon(True)

t4=threading.Thread(target=run.run, args=(["RESTORE_FORGE"])) #Restore Forge Run thread.
t4.setDaemon(True)
'''

def nav_bar():
    nav_bar = Frame(main_frame, width=window.winfo_width(), height=window.winfo_height() / 18, bg="#3D0000") #NavBar
    nav_bar.pack(side="top", fill=BOTH)

    Nova_Logo = Image.open("images/Nova-Universe.png")
    width, height = Nova_Logo.size
    
    actual_width = round(int(width)/11)
    actual_height = round(int(height)/11)

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

    home_button = Button(buttons_bar, text="Home", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2") 
    home_button.grid(row=0, column=1, padx=15)
    home_button.bind("<Enter>", button_hover_enter)
    home_button.bind("<Leave>", button_hover_leave)

    installs_button = Button(buttons_bar, text="Installations", font=("Arial Bold", 10), padx=5, pady=5, fg="white", bg="#1F1E1E", activebackground="#FEBCBC", borderwidth=0, 
    cursor="hand2", command=installations_menu)
    installs_button.grid(row=0, column=2)
    installs_button.bind("<Enter>", button_hover_enter)
    installs_button.bind("<Leave>", button_hover_leave)

def installations_menu():
    installations_frame = Frame(main_frame, width=1280, height=720, bg="#171717") #Main App Frame
    installations_frame.pack(fill=BOTH, expand=1)

    amount_of_installers = 0
    for installer in os.listdir("installers/"):
        print (installer)
        modpack_frame = Frame(installations_frame, width=200, height=200, bg="#282727") #Main App Frame
        modpack_frame.grid(row=0 + amount_of_installers, column=1 + amount_of_installers, padx=15, pady=15)

        modpack_title = Label(modpack_frame, text=installer, font=("Arial Bold", 10)) #Where I left off
        #modpack_title.pack()

        amount_of_installers =+ 1

def home_menu():
    global ver_label
    global Terra_text
    global Terra_slowgon
    global install_button
    global restore_forge_button
    global border

    home_frame = Frame(main_frame, width=1280, height=720, bg="#171717") #Main App Frame
    home_frame.pack(fill=BOTH, expand=1)

    
    #Bottom Hud Frame
    border = Frame(main_canvas, width=600, height=30, bg="#3D0000")
    border.pack(fill=BOTH)

    restore_forge_button = Button(border, text="Restore Forge", font=("Arial Bold", 12), padx=5, pady=1, fg="#E1D8D8", bg="#110000", 	
    activebackground="#13472D", command=restore_forge)
    restore_forge_button.pack(side=RIGHT)

    ver_label = Label(border, text=ver_v, font=("Arial Bold", 16), padx=6, pady=0, fg="#E1D8D8", bg="#3D0000")
    ver_label.config()
    ver_label.pack(side=LEFT)

def finish():
    global t4

    try:
        t3.join()
        open_mc_launcher = True
    except RuntimeError as e:
        open_mc_launcher = False
        t4.join()

    if not open_mc_launcher == False:
        subprocess.Popen(settings.path_to_mc_launcher_exe, stdout=subprocess.PIPE, creationflags=0x08000000)

    close_button = Button(main_frame, text="Close!", font=("Arial Bold", 12), padx=5, pady=1, fg="#E1D8D8", bg="#8A0004", 	
    activebackground="#13472D", command=app_close)   
    close_button.pack(side=BOTTOM)

    sys.exit()

t5=threading.Thread(target=finish)

def button_hover_enter(e):
    hex_colour = Color("#1F1E1E")
    colours = list(hex_colour.range_to(Color("#C06565"),10))
    
    t7=threading.Thread(target=color_glow_effect, args=([e, colours]))
    t7.setDaemon(True)
    t7.start()

def button_hover_leave(e):
    hex_colour = Color("#C06565")
    colours = list(hex_colour.range_to(Color("#1F1E1E"),10))

    t7=threading.Thread(target=color_glow_effect, args=([e, colours]))
    t7.setDaemon(True)
    t7.start()

def color_glow_effect(e, hex_list):
    for color in hex_list:
        time.sleep(0.01)
        print(color)
        e.widget['background'] = '{}'.format(color)

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

def open_url(url=None):
    if not type(url) == type(""):
        url = settings.nova_universe_url

    webbrowser.open_new_tab(url)

def install():
    Terra_text.pack_forget()
    Terra_slowgon.pack_forget()
    install_button.pack_forget()
    restore_forge_button.pack_forget()
    
    t2.start() #Start live installer status thread.

    t3.start() #Start run thread.

    t5.start() #Finish Thread

def restore_forge():
    global t4

    Terra_text.pack_forget()
    Terra_slowgon.pack_forget()
    install_button.pack_forget()
    restore_forge_button.pack_forget()

    t2.start() #Start live installer status thread.

    t4.start() #Start restore forge run thread.

    t5.start() #Finish Thread

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
    #Normal Start Up
    nav_bar() #Loads Nav Bar
    #home_menu() #Loads Home Page

t1=threading.Thread(target=start_up)

window = Tk()

main_canvas = Canvas(window)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
main_frame.pack(fill=BOTH, expand=1)

window.title(app_name)

window.geometry('900x600')
#window.resizable(False, False) #Makes window not resizeable

window.protocol("WM_DELETE_WINDOW", app_close)

start_up() #App startup runs within this function!

window.mainloop()

'''
Jascord Player Color Pallet

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

if __name__ == '__main__':
    pass