from tkinter import *
from tkinter import ttk
from modules.sidepanel_projects import ProjectList
from modules.sidepanel_subjectList import SubjectList
from modules.sidepanel_testList import TestList
from objects.app import app

class SidePanel(object):
    def __init__(self, mainFrame):

        self.sidePanel = ttk.Frame(mainFrame, width=200)
        self.sidePanel.pack(side=LEFT, fill=Y)

        projects = ProjectList(self.sidePanel)
        app.sidepanel_projectList = projects

        subjects = SubjectList(self.sidePanel)
        app.sidepanel_subjectList = subjects
        
        tests = TestList(self.sidePanel)
        app.sidepanel_testList = tests