import tkinter
import os
import sys
from nova_dir import Nova_Dir
from nova_func import *
import settings
import threading
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image, ImageFilter
import tkinter.font as font
from colour import Color
import pythoncom

import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 ) #Hides console

popup_noti_return_value = None

def popup_notification(noti_type, title=None, message=None):
    noti_font_title = font.Font(family='Arial Rounded MT Bold', size=20, weight='bold', underline=False)
    message_label_font = font.Font(family='Arial Rounded MT Bold', size=13, weight='bold', underline=False)

    popup_noti_json = {}
    popup_noti_json["return_value"] = None
    popup_noti_json["tutorial"] = False

    with open(".\\popup_noti_cache.json", 'w') as f:
        json.dump(popup_noti_json, f)

    def wait_for_response_thread():
        #Thread that is ran to pause application after message is displayed.

        def wait_for_response():
            global popup_noti_return_value

            while True:
                with open(".\\popup_noti_cache.json", "r") as f:
                    popup_noti_json = json.load(f)

                return_value = popup_noti_json["return_value"]

                time.sleep(0.001)

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
        ok_button = Button(noti_window, text="Ok!", font=ok_button_font, padx=5, pady=5, fg="#D46757", bg="#171717", activebackground="#D46757", borderwidth=0, 
        cursor="hand2", command=lambda: noti_exit(True))
        ok_button.pack()

    t11=threading.Thread(target=wait_for_response_thread)
    t11.setDaemon(True)
    t11.start()

    return t11

def run(option=None):
    
    if option == None:
        option = "INSTALL"

    if option.upper() == "INSTALL":
        try:
            appdata_path = Nova_Dir.get_appdata_directory()

            #Check if Nova Hub exist first.
            if os.path.isdir(appdata_path + "\\NovaHub") == True:
                #Delete NovaHub app folder in programs folder.
                delete_file(appdata_path + "\\NovaHub")
                
            create_folder(appdata_path + "\\NovaHub")

            #Create temp folder
            create_temp_folder()

            #Download app.zip
            download_file(settings.api + settings.nova_hub_update_package_location, appdata_path + "\\NovaHub\\app.zip") #Download update package.

            extract_zip(appdata_path + "\\NovaHub\\app.zip") #Extracts app package.

            move_files(".\\temp\\update", appdata_path + "\\NovaHub", replace=True) #Move files from temp to root dir to replace old files.

            clear_temp_folder()

            #Delete app.zip
            delete_file(appdata_path + "\\NovaHub\\app.zip")

            #Run app
            import subprocess
            #os.open(appdata_path + "\\NovaHub\\nova_hub.exe")
            #subprocess.Popen(appdata_path + "\\NovaHub\\nova_hub.exe")

            time.sleep(0.2)
            delete_file(".\\assets")
            delete_file(".\\installers")
            delete_file(".\\logs")
            delete_file(".\\popup_noti_cache.json")
            delete_file(".\\temp")
            delete_file(".\\update.exe")

            #Create shortcut.
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            path = os.path.join(desktop, "Nova Hub.lnk")
            target = appdata_path + "\\NovaHub\\nova_hub.exe"
            wDir = appdata_path + "\\NovaHub"
            icon = appdata_path + "\\NovaHub\\nova_hub.exe"
            pythoncom.CoInitialize()
            shell = Dispatch('WScript.Shell')
            pythoncom.CoInitialize()

            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()

            delete_file(".\\assets")
            delete_file(".\\installers")
            delete_file(".\\logs")
            delete_file(".\\popup_noti_cache.json")
            delete_file(".\\temp")
            delete_file(".\\update.exe")

            thread = popup_notification("ok", "Nova Hub Installed", "Nova Hub has been successfully installed. RUN the Nova Hub shortcut on your desktop to start the app. \n:)")
            thread.join()

            window.destroy()
            sys.exit()

        except Exception as e:
            thread = popup_notification("ok", "Installer Unexpected Error", f"In the installer has errored but don't worry they should be a logs folder somewhere so you can report the issue with a log. \n \n {e}")
            thread.join()

            print_and_log("error", e)

            window.destroy()
            sys.exit()

def install_run():
    t1=threading.Thread(target=run, args=[("INSTALL")])
    t1.setDaemon(True)
    t1.start()

    install_button.config(state="disabled")

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

def color_glow_effect(e, hex_list):

    for color in hex_list:
        time.sleep(0.01)
        e.widget['background'] = '{}'.format(color)

window = Tk()

main_canvas = Canvas(window)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
main_frame.pack(fill=BOTH, expand=1)

nova_hub_font = font.Font(family='Arial Rounded MT Bold', size=40, weight='bold', underline=False)
nova_hub_text = Label(main_frame, text="Nova Hub", font=nova_hub_font, fg="#F04E3A", bg="#171717")
#nova_hub_text.pack()

install_button_font = font.Font(family='Arial Rounded MT Bold', size=30, weight='bold', underline=False)
install_button = Button(main_frame, text="Install!", font=install_button_font, padx=10, pady=5, fg="white", bg="#EA0808", activebackground="#F05A17", borderwidth=0, 
cursor="hand2", command=install_run)
install_button.pack(pady=(70, 70))
install_button.bind("<Enter>", lambda event, start_colour="#EA0808", end_colour="#F05A17": button_hover_enter(event, start_colour="#EA0808", end_colour="#F05A17"))
install_button.bind("<Leave>", lambda event, end_colour="#EA0808", start_colour="#F05A17": button_hover_leave(event, end_colour="#EA0808", start_colour="#F05A17"))

#Live Status
live_status_text = Label(main_frame, text="", font=("Arial Rounded MT Bold", 18), fg="#E1D8D8", 
pady=12, bg="#171717", wraplength=780)

#Version Text
version_text_font = font.Font(family='Arial Rounded MT Bold', size=18, weight='bold', underline=False)
version_text = Label(main_frame, text="test", font=version_text_font, fg="#C52612", bg="#171717")
version_text.place(x=628, y=166)

window.title("NOVA HUB INSTALLER")
window.geometry('350x200')
window.resizable(False, False) #Makes window not resizeable

if __name__ == '__main__':

    option = None
    try:
        option = sys.argv[1]
        print_and_log("info_2", f":) We got your command line argument. >>> {option}")

    except IndexError as e:
        print_and_log("WARN", "Couldn't grab command line argument, if you didn't pass an argument ignore this.")
        print_and_log()

    #run(option)

window.mainloop()