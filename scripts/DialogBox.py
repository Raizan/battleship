__author__ = 'Reisuke'

import Tkinter
import tkMessageBox


def dialog_box(flag, title, message):
    Tkinter.Button().master.withdraw()

    if flag == "err":
        tkMessageBox.showerror(title, message)

    elif flag == "warn":
        tkMessageBox.showwarning(title, message)

    elif flag == "info":
        tkMessageBox.showinfo(title, message)