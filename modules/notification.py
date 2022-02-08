from tkinter import *
from tkinter import ttk

class NotificationPanel(object):
    def __init__(self):
        print("Notification instance created")
        self.parent = None

    def create(self, type, text, timeout):
        style = ttk.Style()
        
        if type == 'info':
            style.configure('notif.TLabel', background="green", foreground="white", anchor="CENTER")
        if type == 'error':
            style.configure('notif.TLabel', background="red", foreground="white", anchor="CENTER")

        notif = ttk.Label(self.notifPanel, style='notif.TLabel', text=text)
        notif.pack(fill=X)
        notif.after(timeout, lambda: notif.destroy())

    def setParent(self, parent):
        self.parent = parent
        self.notifPanel = ttk.Frame(self.parent,height=20)
        self.notifPanel.pack(fill=X)

notification = NotificationPanel()