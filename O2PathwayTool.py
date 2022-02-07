from tkinter import *
from tkinter import ttk

from modules.app import *
from modules.settings import *
from modules.menubar import *
from modules.notification import *
from modules.sidePanel import *
from modules.details import *
from modules.plotting import *

root = Tk()
root.title("O2 Pathway Tool")
root.geometry("1000x750")

# Mainframe
mainframe = ttk.Frame(root)
mainframe.pack(expand=True, fill=BOTH)

# Menubar
menu = createMenu(root)

# Notificationframe
infoFrame = ttk.Frame(mainframe, height="20")
infoFrame.pack(side=TOP, fill=X)
notification.setParent(infoFrame)

root.config(menu=menu)

if __name__ == '__main__':
    root.mainloop()