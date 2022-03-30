from ctypes import resize
from tkinter import *
from tkinter import ttk
from turtle import width
from modules.details_env import *
from modules.details_project import *
from modules.details_test import *
from objects.app import app

class DetailsPanel(object):
    def __init__(self, mainFrame):
        sty = ttk.Style()
        sty.configure(
            'details.TFrame', 
            relief='raised'
        )

        self.frame_thickness = 10
        self.defHeight = 50

        self.detailsPanel = ttk.Frame(mainFrame, height=self.defHeight, style="details.TFrame", borderwidth=self.frame_thickness)
        if app.settings.visDefaults['allDetails']:
            self.detailsPanel.pack(side=TOP, fill=X)
            # self.detailsPanel.pack_propagate(False)

        
        sty.layout('details.TFrame', [
            ('Frame.border', {'sticky': 'swe'})
            ])

        self.detailsPanel.bind('<Motion>', self.changeCursor)
        self.detailsPanel.bind('<B1-Motion>', self.resize)
        self.detailsPanel.bind('<Double-Button-1>', self.defSize)

        self.projectDetails = ProjectDetailsModule(self.detailsPanel)
        app.projectDetailModule = self.projectDetails

        self.testDetails = TestDetailModule(self.detailsPanel)
        app.testDetailModule = self.testDetails
        
        self.envDetails = EnvDetailModule(self.detailsPanel)
        app.envDetailModule = self.envDetails

        ttk.Button(self.detailsPanel, text='Plot', command=lambda: self.plotData()).pack(side=RIGHT)#, fill=Y)

    def plotData(self):
        app.getPlottingPanel().plot()
        tabCount = app.getPlottingPanel().plotNotebook.index('end')
        app.getPlottingPanel().plotNotebook.select(tabCount-1)

    def resize(self, event):
        self.detailsPanel.pack_propagate(False)
        if event.y > 10:
            self.detailsPanel.configure(height=event.y, width=self.detailsPanel.winfo_reqwidth())

    def changeCursor(self, e):
        if self.detailsPanel.identify(e.x, e.y) == 'border':
            self.detailsPanel.configure(cursor='sb_v_double_arrow')
        else:
            self.detailsPanel.configure(cursor='arrow')

    def defSize(self, event):
        self.detailsPanel.pack_propagate(True) 