from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter import ttk

from objects.app import app
from objects.settings import Settings
from modules.menubar import MenuBar
from modules.notification import notification
from modules.panel_side import SidePanel
from modules.panel_details import DetailsPanel
from modules.panel_plotting import PlottingPanel

root = Tk()
root.title("O2 Pathway Tool")
root.geometry("1000x750")
root.pack_propagate(1)

app.root = root
# app.strVars = []
# app.intVars = []

# Load settings
settings = Settings()
app.settings = settings

# Mainframe
mainframe = ttk.Frame(root)
mainframe.pack(expand=TRUE, fill=BOTH)

# Panels
sidePanel = SidePanel(mainframe)
app.sidePanel = sidePanel

notification.setParent(mainframe)

detailsPanel = DetailsPanel(mainframe)
app.detailsPanel = detailsPanel

plottingPanel = PlottingPanel(mainframe)
app.plottingPanel = plottingPanel

""" def showAdvLayout():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container

    projectContainer.pack_forget()
    testContainer.pack_forget()
    envContainer.pack_forget()

    projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
    testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
    envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

def showBasicLayout():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container

    projectContainer.pack_forget()
    testContainer.pack_forget()
    envContainer.pack_forget()

    testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

if app.getActiveMode() == 0:
    showBasicLayout()
else:
    showAdvLayout() """

# Menubar
menuObj = MenuBar(root)
menu = menuObj.getMenubar()
app.menu = menuObj

root.config(menu=menu)

def debug():
    for d in app.getActiveTest().getWorkLoads():
        print(d.getDetails().getWorkLoadDetails())

root.bind('<Tab>', lambda e: debug())

def on_closing():
    if askokcancel("Quit", "Do you want to quit?"):
        side = False
        details = False
        project = False
        test = False
        env = False

        try:
            sidePanel.sidePanel.pack_info()
            side = True
        except:
            pass
        try:
            detailsPanel.detailsPanel.pack_info()
            details = True
        except:
            pass
        try:
            detailsPanel.projectDetails.container.pack_info()
            project = True
        except:
            pass
        try:
            detailsPanel.testDetails.container.pack_info()
            test = True
        except:
            pass
        try:
            detailsPanel.envDetails.frame.pack_info()
            env = True
        except:
            pass

        settings.saveLayout(side, details, project, test, env)
        root.destroy()
        root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == '__main__':
    root.mainloop()