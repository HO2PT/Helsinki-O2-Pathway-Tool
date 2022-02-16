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

        ttk.Button(self.detailsPanel, text='Plot', command=lambda: self.debugPrint()).pack(side=RIGHT)

    def debugPrint(self):
        """ workLoads = app.activeTest.getWorkLoads()
        for w in workLoads:
            print(w.getWorkLoadDetails())
            print(app.getActiveTest().getEnvDetails().getDetails()) """
        app.getPlottingPanel().plot()
        #print(len(app.strVars))
        #print( app.getActiveTest().getEnvDetails().getDetails() )
        """ print( f'n-of-TESTS: {len(app.getActiveSubject().getTests())}' )
        i = 1
        for t in app.getActiveSubject().getTests():
            print( f'LOADS OF TEST-{i}: {t.nWorkLoads()}' )
            for w in t.getWorkLoads():
                print(w.getWorkLoadDetails())
            i = i+1 """

        #print(app.getActiveProject(), app.getActiveSubject(), app.getActiveTest())
        """ workLoads = app.activeTest.getWorkLoads()
        print( f'N OF WORKLOADS: {len(workLoads)}' )
        print( f'N OF STRVARS: {len(app.strVars)}' )
        for w in workLoads:
            print(w.getWorkLoadDetails()) """