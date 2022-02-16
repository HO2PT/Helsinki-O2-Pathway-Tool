class App(object):
    sidePanel = None
    sidepanel_projectList = None
    sidepanel_subjectList = None
    sidepanel_testList = None

    detailsPanel = None
    projectDetailModule = None
    testDetailModule = None
    envDetailModule = None
    plottingPanel = None
   
    strVars = None
    intVars = None

    def __init__(self):
        self.activeProject = None
        self.activeSubject = None
        self.activeTest = None
        self.activeMode = None
        self.projects = []
        self.settings = None

    def setActiveTest(self, test):
        self.activeTest = test

    def getActiveTest(self):
        return self.activeTest

    def setActiveSubject(self, subject):
        self.activeSubject = subject

    def getActiveSubject(self):
        return self.activeSubject

    def setActiveProject(self, project):
        self.activeProject = project

    def getActiveProject(self):
        return self.activeProject
    
    def addProject(self, project):
        self.projects.append(project)

    def getPlottingPanel(self):
        return self.plottingPanel

app = App()