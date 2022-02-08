from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.project import Project

class ProjectList(object):
    def __init__(self, sidePanel):
        container = LabelFrame(sidePanel, text="Projects")
        container.pack(fill = BOTH, expand=TRUE)

        self.projectList = Listbox(container, exportselection=FALSE)
        self.projectList.pack(fill = BOTH, expand=TRUE)

        self.projectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        buttonContainer = ttk.Frame(container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add', command=lambda: self.createProject()).pack(side=LEFT)
        ttk.Button(buttonContainer, text='Edit').pack(side=LEFT)
        ttk.Button(buttonContainer, text='Del').pack(side=LEFT)
        
        ttk.Button(container, text='Import...').pack()

    def addToList(self, id):
        self.projectList.insert(0, id)
        self.projectList.selection_set(0)

    def createProject(self):
        project = Project()
        self.projectList.insert(0, project.id)
        self.projectList.selection_set(0)

        # Update app state
        app.addProject(project)
        app.setActiveProject(project)

    def handleListboxSelect(self):
        #app.sidepanel_subjectList
        app.sidepanel_testList.testList.delete(0, 'end')

        index = self.projectList.curselection()[0]
        project = app.projects[index]
        app.setActiveProject(project)

        app.sidepanel_subjectList.refreshList()