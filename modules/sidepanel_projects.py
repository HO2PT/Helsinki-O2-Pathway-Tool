from tkinter import *
from tkinter import ttk

from objects.app import app
from objects.project import Project

class ProjectList(object):
    def __init__(self, sidePanel):
        self.container = LabelFrame(sidePanel, text="Projects")
        self.container.pack(fill = BOTH, expand=TRUE)

        self.projectList = Listbox(self.container, exportselection=FALSE)
        self.projectList.pack(fill = BOTH, expand=TRUE)

        self.projectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        self.createButton = ttk.Button(buttonContainer, text='Add', command=lambda: self.createProject())
        self.createButton.pack(side=LEFT)
        self.editButton = ttk.Button(buttonContainer, text='Edit', command=lambda: self.editProject())
        self.editButton.pack(side=LEFT)
        self.deleteButton = ttk.Button(buttonContainer, text='Del', command=lambda: self.deleteProject())
        self.deleteButton.pack(side=LEFT)
        
        ttk.Button(self.container, text='Import...').pack()

    def editProject(self):
        index = self.projectList.curselection()[0]

        # Create edit popup
        editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*3, height=self.editButton.winfo_reqheight()*3)
        editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth() - 7
        ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
        editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
        editscreen.pack_propagate(False)
        
        ttk.Label(editscreen, text='Project name').pack()
        nameEntry = ttk.Entry(editscreen)
        nameEntry.pack(expand=TRUE)
        ttk.Button(editscreen, text='Save', command=lambda: edit()).pack(side=BOTTOM,anchor='e')

        def edit():
            project = app.getProjects()[index]
            project.setId(nameEntry.get())
            self.refreshList()
            editscreen.destroy()

    def deleteProject(self):
        index = self.projectList.curselection()[0]
        p = app.getProjects()
        del p[index]
        self.refreshList()
        app.setActiveProject(None)

    def refreshList(self):
        projects = app.getProjects()
        self.projectList.delete(0, 'end')
        for p in projects:
            self.projectList.insert('end', p.id)

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