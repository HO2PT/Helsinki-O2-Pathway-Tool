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
        self.detailsPanel.pack(side=TOP, fill=X)

        projectDetails = ProjectDetailsModule(self.detailsPanel)
        app.projectDetailModule = projectDetails

        testDetails = TestDetailModule(self.detailsPanel)
        app.testDetailModule = testDetails
        
        envDetails = EnvDetailModule(self.detailsPanel)
        app.envDetailModule = envDetails

        ttk.Button(self.detailsPanel, text='Plot', command=lambda: self.plotData()).pack(side=RIGHT)

    def plotData(self):
        app.getPlottingPanel().plot()
        tabCount = app.getPlottingPanel().plotNotebook.index('end')
        app.getPlottingPanel().plotNotebook.select(tabCount-1)