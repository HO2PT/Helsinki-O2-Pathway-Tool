from tkinter import *
from tkinter import ttk

class NotificationPanel(object):
    def __init__(self):
        self.parent = None
        self.notifications = []

    def create(self, type, text, timeout):
        style = ttk.Style()
        style.configure('notif.TLabel')
        
        if type == 'info':
            style.configure('notif.TLabel', background="green", foreground="white", anchor="CENTER")
        if type == 'error':
            style.configure('notif.TLabel', background="red", foreground='white', anchor="CENTER")

        self.notif = ttk.Label(self.notifPanel, style='notif.TLabel', text=text, font='Arial 12')

        if len(self.notifications) == 0:
            self.notifications.append(self.notif)
            self.notif.pack(fill=X)
            self.notif.after(timeout, lambda: self.destroyNotif())

    def destroyNotif(self):
        self.notifications[0].destroy()
        self.notifications = []

    def setParent(self, parent):
        self.parent = parent
        self.notifPanel = ttk.Frame(self.parent, height=22)
        self.notifPanel.pack(fill=X)

notification = NotificationPanel()