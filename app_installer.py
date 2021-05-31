import tkinter
import os
import sys
from nova_dir import Nova_Dir
from nova_func import *
import settings

def run(option=None):
    
    if option == None:
        option = "INSTALL"

    if option.upper() == "INSTALL":

        appdata_path = Nova_Dir.get_appdata_directory()
        
        #Create NovaHub app folder in programs folder.
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
        os.startfile(appdata_path + "\\NovaHub\\nova_hub.exe")

        time.sleep(0.2)
        delete_file(".\\assets")
        delete_file(".\\installers")
        delete_file(".\\logs")
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
        shell = Dispatch('WScript.Shell')

        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()

        delete_file(".\\assets")
        delete_file(".\\installers")
        delete_file(".\\logs")
        delete_file(".\\temp")
        delete_file(".\\update.exe")

        exit
        sys.exit()

if __name__ == '__main__':

    option = None
    try:
        option = sys.argv[1]

    except IndexError as e:
        print_and_log("WARN", "Couldn't grab command line argument, if you didn't pass an argument ignore this.")
        print_and_log()

    run(option)