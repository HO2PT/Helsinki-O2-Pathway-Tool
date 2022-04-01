from ctypes import resize
from tkinter import *
from tkinter import ttk
from turtle import width
from modules.details_env import *
from modules.details_project import *
from modules.details_test import *
from objects.app import app

class DetailsPanel(ttk.Frame):
    def __init__(self, mainFrame, *args, **kwargs):
        ttk.Frame.__init__(self, mainFrame, *args, **kwargs)
        self.pack(side=TOP, fill=X)

        sty = ttk.Style()
        sty.configure(
            'details.TFrame', 
            relief='raised'
        )

        self.frame_thickness = 10
        self.defHeight = 50

        self.upPart = ttk.Frame(self)
        self.upPart.pack(fill=X)

        self.detailsPanel = ttk.Frame(self.upPart, height=self.defHeight, style="details.TFrame", borderwidth=self.frame_thickness)
        if app.settings.visDefaults['allDetails']:
            self.detailsPanel.pack(side=LEFT, fill=X, expand=True)
            # self.detailsPanel.pack_propagate(False)

        
        sty.layout('details.TFrame', [
            ('Frame.border', {'sticky': 'swe'})
            ])

        self.projectDetails = ProjectDetailsModule(self.detailsPanel)
        app.projectDetailModule = self.projectDetails

        self.testDetails = TestDetailModule(self.detailsPanel)
        app.testDetailModule = self.testDetails
        
        self.envDetails = EnvDetailModule(self.detailsPanel)
        app.envDetailModule = self.envDetails

        self.plotButton = ttk.Button(self.upPart, text='Plot', command=lambda: self.plotData())
        self.plotButton.pack(side=RIGHT, fill=Y)

        self.indicator = ttk.Label(self, text='', anchor='center')
        self.indicator.pack(side=BOTTOM, fill=X)

        self.detailsPanel.bind('<Motion>', self.changeCursor)
        self.detailsPanel.bind('<B1-Motion>', self.resize)
        self.indicator.bind('<Double-Button-1>', self.defSize)

        # print(self.testDetails.winfo_width(), self.projectDetails.winfo_width(), self.envDetails.winfo_width())

    def plotData(self):
        app.getPlottingPanel().plot()
        tabCount = app.getPlottingPanel().plotNotebook.index('end')
        app.getPlottingPanel().plotNotebook.select(tabCount-1)

    def resize(self, event):
        self.detailsPanel.pack_propagate(False)
        minHeight = self.testDetails.winfo_reqheight()
        containerHeight = self.detailsPanel.winfo_height()
        if event.y > 20:
            self.detailsPanel.configure(height=event.y, width=self.detailsPanel.winfo_reqwidth())
        
        if containerHeight < minHeight:
            self.indicator.configure(text='\u25BC', foreground='white', background='#4eb1ff')
        else:
            self.indicator.configure(text='', background=app.root.cget('bg'))

    def changeCursor(self, e):
        if self.detailsPanel.identify(e.x, e.y) == 'border':
            self.detailsPanel.configure(cursor='sb_v_double_arrow')
        else:
            self.detailsPanel.configure(cursor='arrow')

    def defSize(self, event):
        self.indicator.configure(text='', background=app.root.cget('bg'))
        self.detailsPanel.pack_propagate(True)
