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

        detailsPanel = ttk.Frame(mainFrame, style='detailsPanel.TFrame')
        detailsPanel.pack(side=TOP, fill=X)

        projectDetails = ProjectDetailsModule(detailsPanel)
        app.projectDetailModule = projectDetails

        testDetails = TestDetailModule(detailsPanel)
        app.testDetailModule = testDetails
        
        envDetails = EnvDetailModule(detailsPanel)

        #ttk.Button(detailsPanel, text='Plot', command=lambda: print(app.activeProject, app.activeSubject, app.activeTest) ).pack(side=RIGHT)
        ttk.Button(detailsPanel, text='Plot', command=lambda: self.debugPrint()).pack(side=RIGHT)

    def debugPrint(self):
        print( f'n-of-TESTS: {len(app.getActiveSubject().getTests())}' )
        i = 1
        for t in app.getActiveSubject().getTests():
            print( f'LOADS OF TEST-{i}: {t.nWorkLoads()}' )
            i = i+1
        #print(app.getActiveProject(), app.getActiveSubject(), app.getActiveTest())
        """ workLoads = app.activeTest.getWorkLoads()
        print( f'N OF WORKLOADS: {len(workLoads)}' )
        print( f'N OF STRVARS: {len(app.strVars)}' )
        for w in workLoads:
            print(w.getWorkLoadDetails()) """