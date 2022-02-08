from tkinter import *
from tkinter import ttk
from modules.details_env import *
from modules.details_project import *
from modules.details_test import *
from objects.app import app

class DetailsPanel(object):
    def __init__(self, mainFrame):
        print("DetailsPanel instance created")
        
        s = ttk.Style()
        s.configure('detailsPanel.TFrame')

        detailsPanel = ttk.Frame(mainFrame, style='detailsPanel.TFrame')
        detailsPanel.pack(side=TOP, fill=X)

        projectDetails = ProjectDetailsModule(detailsPanel)
        app.projectDetailModule = projectDetails

        testDetails = TestDetailModule(detailsPanel)
        app.testDetailModule = testDetails
        
        envDetails = EnvDetailModule(detailsPanel)

        ttk.Button(detailsPanel, text='Plot', command=lambda: print(app.activeProject, app.activeSubject, app.activeTest) ).pack(side=RIGHT)