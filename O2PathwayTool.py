from tkinter import *
from tkinter.messagebox import askokcancel
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
app.plottingPanel = plottingPanel

root.config(menu=menu)

def on_closing():
    if askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == '__main__':
    root.mainloop()