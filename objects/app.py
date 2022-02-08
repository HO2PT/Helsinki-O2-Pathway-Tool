from objects.test import Test

class App(object):
    sidepanel_projectList = None
    sidepanel_subjectList = None
    sidepanel_testList = None
    projectDetailModule = None
    testDetailModule = None

    def __init__(self):
        print("App instance created") 
        self.activeProject = None
        self.activeSubject = None
        self.activeTest = None
        self.activeMode = None
        self.projects = []
        self.settings = None

    def setActiveTest(self, test):
        self.activeTest = test

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

app = App()