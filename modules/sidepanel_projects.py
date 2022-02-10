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
        self.projectList.insert('end', id)
        self.projectList.selection_clear(0, 'end')
        self.projectList.selection_set('end')

    def createProject(self):
        #print(f'BEFORE: {self.projectList.curselection()}')
        project = Project()
        self.projectList.insert('end', project.id)
        self.projectList.selection_clear(0, 'end')
        self.projectList.selection_set('end')
        #print(f'AFTER: {self.projectList.curselection()}')

        # Update app state
        app.addProject(project)
        app.setActiveProject(project)
        app.setActiveSubject(None)
        app.setActiveTest(None)

        # Refresh views
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

    def handleListboxSelect(self):
        # Set selected project as active project by clicked index
        index = self.projectList.curselection()[0]
        project = app.projects[index]
        app.setActiveProject(project)

        # Refresh app state
        app.setActiveSubject(None)
        app.setActiveTest(None)

        # Refresh views
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()