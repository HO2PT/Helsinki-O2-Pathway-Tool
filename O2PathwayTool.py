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
root.geometry('750x500')
# print(f' init: {initWidth, initHeight}')
# root.pack_propagate(False)

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

# Menubar
menuObj = MenuBar(root)
menu = menuObj.getMenubar()
app.menu = menuObj

root.config(menu=menu)

root.update_idletasks()
initX = int(root.winfo_screenwidth()) * 0.5 - int(root.winfo_width()) * 0.5
initY = int(root.winfo_screenheight()) * 0.5 - int(root.winfo_height()) * 0.5
root.geometry("+%d+%d" % ( initX, initY ))

loaded = False

def resize(e):
    print(e)
    width = root.winfo_width()
    height = root.winfo_height()
    print(width, height)
    # if e.width != root.winfo_reqwidth() or e.height != root.winfo_reqheight():
    #     print('resize')
    sidePanelMinWidth = app.sidePanel.sidePanel.winfo_reqwidth()
    detailsPanelMinWidth = app.detailsPanel.detailsPanel.winfo_reqwidth()
    print( sidePanelMinWidth )
    print( detailsPanelMinWidth )
    if width < sidePanelMinWidth + detailsPanelMinWidth:
        print('HOOLLD UP')
        # root.resizable(False, True)
    # else:
    #     root.resizable(True, True)
    # app.sidepanel_projectList.container.configure(height=100)

# root.bind('<Configure>', lambda e: resize(e))

def debug():
    # for d in app.getActiveTest().getWorkLoads():
        # print(d.getDetails().getWorkLoadDetails())
    print( app.plottingPanel.plots[0].loadNotebookFrame.winfo_width())

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