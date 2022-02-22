from tkinter import *
from tkinter import ttk
from objects.app import app

class ProjectDetailsModule(object):
    def __init__(self, detailsPanel):
        self.container = ttk.Labelframe(detailsPanel, text="Project details")
        self.container.pack(side = LEFT, fill=Y)
        #print(self.container.pack_info())

        self.subjectCount = ttk.Label(self.container, text=None)
        self.subjectCount.pack(expand=False)
        #print(self.subjectCount.pack_info())

        #ttk.Button(self.container, text="Calculate").pack(side=BOTTOM)

    def refreshDetails(self):
        activeProject = app.getActiveProject()
        self.subjectCount.config(text=f'Subjects: {len(activeProject.subjects)}')
