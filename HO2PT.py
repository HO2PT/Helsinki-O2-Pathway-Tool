from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter import ttk, font
from pathlib import Path
import sys
#from os import path
import syslog
syslog.openlog('Python')

from objects.app import app
from objects.settings import Settings
from modules.menubar import MenuBar
from modules.notification import notification
from modules.panel_side import SidePanel
from modules.panel_details import DetailsPanel
from modules.panel_plotting import PlottingPanel

from ttkthemes import ThemedTk

app.platform = sys.platform
if sys.platform == 'linux':
    root = ThemedTk(theme='clearlooks')
    root.configure(bg='#EFEBE7')
    fontSize = 9
elif sys.platform == 'darwin':
    root = ThemedTk(theme='arc')
    root.configure(bg='#F5F6F7')
    #app.path = path.abspath(path.dirname(__file__))
    if hasattr(sys, '_MEIPASS'):
        app.path = Path(sys._MEIPASS)
    else:
        app.path = Path(__file__).parent
    fontSize = 12
else:
    root = Tk()
    fontSize = 9

syslog.syslog(syslog.LOG_ALERT, f'HO2PT: {app.path}')

app.defaultFont = font.nametofont("TkDefaultFont")
app.defaultFont.configure(family="Arial",size=fontSize)
root.option_add("*Font", f"Arial {fontSize}")

root.title("Helsinki O\u2082 Pathway Tool")
root.geometry('750x500')

app.root = root

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

# def debug():
#     for d in app.getActiveTest().getWorkLoads():
#         print(d.getDetails().getWorkLoadDetails())
#         print(d.envDetails.getDetails())
#     for p in app.plottingPanel.plots:
#         print('TEST')
#         for l in p.activeTest.workLoads:
#             print(l.envDetails.getDetails())
#             print(l.details.getWorkLoadDetails())
# root.bind('<Tab>', lambda e: debug())

# def updateCursor(e):
#     print(mainframe.identify(e.x, e.y))

sepStyle = ttk.Style()
sepStyle.configure('asd.TSeparator', background = 'dark gray')

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
            detailsPanel.projectDetails.pack_info()
            project = True
        except:
            pass
        try:
            detailsPanel.testDetails.pack_info()
            test = True
        except:
            pass
        try:
            detailsPanel.envDetails.pack_info()
            env = True
        except:
            pass

        settings.saveLayout(side, details, project, test, env)
        root.destroy()
        root.quit()

        if app.platform == 'darwin':
            exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
if app.platform == 'darwin':
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=f'{app.path}/Img/ho2pt.png'))
else:
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='Img/ho2pt.png'))

if __name__ == '__main__':
    root.mainloop()