from tkinter import *
from tkinter import ttk
from modules.details_env import *
from modules.details_project import *
from modules.details_test import *
from objects.app import app

class DetailsPanel(object):
    def __init__(self, mainFrame):
        s = ttk.Style()
        s.configure('detailsPanel.TFrame')

        self.detailsPanel = ttk.Frame(mainFrame, style='detailsPanel.TFrame')
        if app.settings.visDefaults['allDetails']:
            self.detailsPanel.pack(side=TOP, fill=X)

        self.projectDetails = ProjectDetailsModule(self.detailsPanel)
        app.projectDetailModule = self.projectDetails

        self.testDetails = TestDetailModule(self.detailsPanel)
        app.testDetailModule = self.testDetails
        
        self.envDetails = EnvDetailModule(self.detailsPanel)
        app.envDetailModule = self.envDetails

        ttk.Button(self.detailsPanel, text='Plot', command=lambda: self.plotData()).pack(side=RIGHT, fill=Y)

    def plotData(self):
        app.getPlottingPanel().plot()
        tabCount = app.getPlottingPanel().plotNotebook.index('end')
        app.getPlottingPanel().plotNotebook.select(tabCount-1)