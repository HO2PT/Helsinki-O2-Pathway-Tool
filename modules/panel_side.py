from tkinter import *
from tkinter import ttk
from modules.sidepanel_projects import ProjectList
from modules.sidepanel_subjectList import SubjectList
from modules.sidepanel_testList import TestList
from objects.app import app

class SidePanel(object):
    def __init__(self, mainFrame):

        sty = ttk.Style()
        sty.configure(
            'sidePanel.TFrame', 
            relief='raised'
        )
        
        self.frame_thickness = 10

        self.sidePanel = ttk.Frame(mainFrame, style="sidePanel.TFrame", borderwidth=self.frame_thickness)
        if app.settings.visDefaults['sideMenu']:
            self.sidePanel.pack(side=LEFT, fill=Y)

        sty.layout('sidePanel.TFrame', [
            ('Frame.border', {'sticky': 'nse'})
        ])

        self.sidePanel.bind('<Motion>', self.changeCursor)
        self.sidePanel.bind('<B1-Motion>', self.resize)
        self.sidePanel.bind('<Double-Button-1>', self.defSize)

        projects = ProjectList(self.sidePanel)
        app.sidepanel_projectList = projects

        subjects = SubjectList(self.sidePanel)
        app.sidepanel_subjectList = subjects
        
        tests = TestList(self.sidePanel)
        app.sidepanel_testList = tests

    def changeCursor(self, e):
        if self.sidePanel.identify(e.x, e.y) == 'border':
            self.sidePanel.configure(cursor='sb_h_double_arrow')
        else:
            self.sidePanel.configure(cursor='arrow')

    def resize(self, event):
        self.sidePanel.pack_propagate(False)
        if event.x > 10:
            self.sidePanel.configure(height=self.sidePanel.winfo_height(), width=event.x)

    def defSize(self, event):
        self.sidePanel.pack_propagate(True)