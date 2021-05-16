import os
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter.ttk import Progressbar
import threading
import multiprocessing
import time
import subprocess

import settings
import game_directory_finder
import run

app_name = settings.app_name

ver_v = "V" + str(settings.version)

live_installer_status = "Starting Live Install Status Thread..."

lrs = False

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

t3=threading.Thread(target=run.run) #Run thread.
t3.setDaemon(True)

t4=threading.Thread(target=run.run, args=(["RESTORE_FORGE"])) #Restore Forge Run thread.
t4.setDaemon(True)

def home_menu():
    global ver_label
    global Terra_text
    global Terra_slowgon
    global install_button
    global restore_forge_button
    global border

    Terra_text = Label(main_frame, text="Terra SMP ModPack Installer", font=("Arial Bold", 40), fg="#E1D8D8", bg="#171717")
    Terra_text.config(anchor=CENTER)
    Terra_text.pack()

    Terra_slowgon = Label(main_frame, text="[placeholder for description].", font=("Arial Bold", 15), fg="#E1D8D8", pady=12, bg="#171717")
    Terra_slowgon.config(anchor=CENTER)
    Terra_slowgon.pack()

    install_button = Button(main_frame, text="Install!", font=("Arial Bold", 30), padx=20, pady=2, fg="#E1D8D8", bg="#8A0004", 	
    activebackground="#13472D", command=install)
    install_button.pack(expand=0.1)

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
    home_menu() #Loads Home Page

t1=threading.Thread(target=start_up)

window = Tk()

main_canvas = Canvas(window)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
main_frame.pack(fill=BOTH, expand=1)

window.title(app_name)

window.geometry('800x500')
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