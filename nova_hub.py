import os
import threading
import time
import ctypes

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image, ImageFilter
import tkinter.font as font

def launch_app():
    import app

def focus_on_app():
    import settings

    time.sleep(2) #Add 2 secound delay on production version
    user32 = ctypes.windll.user32

    # get handle for Notepad window
    # non-zero value for handle should mean it found a window that matches
    handle = user32.FindWindowW(u'{}'.format(settings.app_name), None)

    print(handle)

    user32.ShowWindow(handle, 5)


def updating_screen():
    global window

    window = Tk()

    main_canvas = Canvas(window)
    main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    main_frame = Frame(main_canvas, width=1280, height=720, bg="#171717") #Main App Frame
    main_frame.pack(fill=BOTH, expand=1)

    update_text_font = font.Font(family='Arial Rounded MT Bold', size=20, weight='bold', underline=False)
    update_text = Label(main_frame, text="Updating Nova Hub...", font=update_text_font, fg="#05FFFF", bg="#171717")
    update_text.pack()

    update_image = Image.open("images\\update.png")

    width, height = update_image.size
    
    actual_width = round(int(width)/8)
    actual_height = round(int(height)/8)

    update_image = update_image.resize((actual_width, actual_height))
    tkimage = ImageTk.PhotoImage(update_image)
    update_image_label = Label(main_frame, image=tkimage, bg="#171717")
    update_image_label.photo = tkimage
    update_image_label.pack(side="left", padx=20)

    window.title("NOVA HUB UPDATER")
    window.iconbitmap("images\\update_icon.ico")
    window.geometry('800x200')
    window.resizable(False, False) #Makes window not resizeable

def update_app():
    updating_screen()

    window.destroy() #End of update

def run_update_service():
    pass

if __name__ == '__main__':
    update_app()

    t1 = threading.Thread(target=launch_app)
    t1.start()

    t2 = threading.Thread(target=focus_on_app)
    t2.start()



    # meaning of 2nd parameter defined here.
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx

window.mainloop()