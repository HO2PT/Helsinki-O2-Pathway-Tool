from tkinter import *
from tkinter import ttk
from modules.sidepanel_projects import ProjectList
from modules.sidepanel_subjectList import SubjectList
from modules.sidepanel_testList import TestList
from objects.app import app

class SidePanel(object):
    def __init__(self, mainFrame):
        print("SidePanel instance created")

        s = ttk.Style()
        s.configure('sidePanel.TFrame', background="green")

        sidePanel = ttk.Frame(mainFrame, style='sidePanel.TFrame', width=200)
        sidePanel.pack(side=LEFT, fill=Y)

        projects = ProjectList(sidePanel)
        app.sidepanel_projectList = projects

        subjects = SubjectList(sidePanel)
        app.sidepanel_subjectList = subjects
        
        tests = TestList(sidePanel)
        app.sidepanel_testList = tests