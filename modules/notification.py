from tkinter import *
from tkinter import ttk

class Notification(object):
    def __init__(self):
        print("Notification instance created")
        pass

    def create(self, type, text, timeout):
        style = ttk.Style()
        
        if type == 'info':
            style.configure('notif.TLabel', background="green", foreground="white", anchor="CENTER")
        if type == 'error':
            style.configure('notif.TLabel', background="red", foreground="white", anchor="CENTER")

        notif = ttk.Label(self.parent, style='notif.TLabel', text=text)
        notif.pack(fill=X)
        notif.after(timeout, lambda: notif.destroy())

    def setParent(self, parent):
        self.parent = parent

notification = Notification()