from tkinter import *
from tkinter import ttk

from objects.app import *
#from objects.settings import *
from modules.menubar import *
from modules.notification import notification
from modules.panel_side import SidePanel
from modules.panel_details import DetailsPanel
from modules.panel_plotting import PlottingPanel

root = Tk()
root.title("O2 Pathway Tool")
root.geometry("1000x750")

app.strVars = []

# Mainframe
mainframe = ttk.Frame(root)
mainframe.pack(expand=TRUE, fill=BOTH)

# Menubar
menu = createMenu(root)

# Panels
sidePanel = SidePanel(mainframe)
notification.setParent(mainframe)
detailsPanel = DetailsPanel(mainframe)
plottingPanel = PlottingPanel(mainframe)

root.config(menu=menu)

if __name__ == '__main__':
    root.mainloop()