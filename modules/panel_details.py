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
        # s = ttk.Style()
        # s.configure('detailsPanel.TFrame', background='red')

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

        self.detailsPanel.bind('<B1-Motion>', self.resize)
        self.detailsPanel.bind('<Double-Button-1>', self.defSize)

        # self.detailsFrame = ttk.Frame(self.detailsPanel)
        # self.detailsFrame.pack(fill=X)

        self.projectDetails = ProjectDetailsModule(self.detailsPanel)
        app.projectDetailModule = self.projectDetails

        self.testDetails = TestDetailModule(self.detailsPanel)
        app.testDetailModule = self.testDetails
        
        self.envDetails = EnvDetailModule(self.detailsPanel)
        app.envDetailModule = self.envDetails

        ttk.Button(self.detailsPanel, text='Plot', command=lambda: self.plotData()).pack(side=RIGHT)#, fill=Y)
        
        # Resize frame
        # resizeFrame = ttk.Label(self.detailsPanel, style='detailsPanel.TFrame')
        # resizeFrame.pack(fill=X)
        # resizeFrame.bind('<1>', lambda e: print('jou'))
        # print(self.detailsPanel.winfo_height())


    def plotData(self):
        app.getPlottingPanel().plot()
        tabCount = app.getPlottingPanel().plotNotebook.index('end')
        app.getPlottingPanel().plotNotebook.select(tabCount-1)

    def resize(self, event):
        self.detailsPanel.pack_propagate(False)
        self.detailsPanel.configure(height=event.y, width=self.detailsPanel.winfo_reqwidth())

    def defSize(self, event):
        self.detailsPanel.pack_propagate(True) 