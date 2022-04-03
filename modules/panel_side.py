from tkinter import *
from tkinter import ttk
from modules.sidepanel_projects import ProjectList
from modules.sidepanel_subjectList import SubjectList
from modules.sidepanel_testList import TestList
from objects.app import app

class SidePanel(ttk.Frame):
    def __init__(self, mainFrame, *args, **kwargs):
        ttk.Frame.__init__(self, mainFrame, *args, **kwargs)
        self.pack(side=LEFT, fill=Y)

        sty = ttk.Style()
        sty.configure(
            'sidePanel.TFrame', 
            relief='raised'
        )
        
        self.frame_thickness = 10

        self.sidePanel = ttk.Frame(self, style="sidePanel.TFrame", borderwidth=self.frame_thickness)
        if app.settings.visDefaults['sideMenu']:
            self.sidePanel.pack(side=LEFT, fill=Y)

        sty.layout('sidePanel.TFrame', [
            ('Frame.border', {'sticky': 'nse'})
        ])

        projects = ProjectList(self.sidePanel)
        app.sidepanel_projectList = projects

        subjects = SubjectList(self.sidePanel)
        app.sidepanel_subjectList = subjects
        
        tests = TestList(self.sidePanel)
        app.sidepanel_testList = tests

        self.indicator = ttk.Label(self, text='', anchor='center')
        self.indicator.pack(side=RIGHT, fill=Y)

        self.sidePanel.bind('<Motion>', self.changeCursor)
        self.sidePanel.bind('<B1-Motion>', self.resize)
        self.indicator.bind('<Double-Button-1>', self.defSize)

    def changeCursor(self, e):
        if self.sidePanel.identify(e.x, e.y) == 'border':
            self.sidePanel.configure(cursor='sb_h_double_arrow')
        else:
            self.sidePanel.configure(cursor='arrow')

    def resize(self, event):
        self.sidePanel.pack_propagate(False)
        minWidth = app.sidepanel_projectList.container.winfo_reqwidth()
        containerWidth = self.sidePanel.winfo_width()
        if event.x > 10:
            self.sidePanel.configure(height=self.sidePanel.winfo_height(), width=event.x)
        
        if containerWidth < minWidth:
            self.indicator.configure(text='\u2B80', foreground='white', background='#4eb1ff')
        else:
            self.indicator.configure(text='', background=app.root.cget('bg'))

    def defSize(self, event):
        self.indicator.configure(text='', background=app.root.cget('bg'))
        self.sidePanel.pack_propagate(True)