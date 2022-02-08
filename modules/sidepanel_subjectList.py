from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.project import Project
from objects.subject import Subject

class SubjectList(object):
    def __init__(self, sidePanel):
        container = LabelFrame(sidePanel, text="Subjects")
        container.pack(fill = BOTH, expand=TRUE)

        self.subjectList = Listbox(container, exportselection=FALSE)
        self.subjectList.pack(fill = BOTH, expand=TRUE)
        self.subjectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        buttonContainer = ttk.Frame(container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add', command=lambda: self.createSubject()).pack(side=LEFT)
        ttk.Button(buttonContainer, text='Edit').pack(side=LEFT)
        ttk.Button(buttonContainer, text='Del').pack(side=LEFT)
        
        ttk.Button(container, text='Import...').pack()

    def createSubject(self):
        if app.getActiveProject() == None:
            project = Project()
            app.setActiveProject(project)

            index = self.subjectList.size()
            subject = Subject(index)
            self.subjectList.insert('end', subject.id)
            self.subjectList.selection_set(0)
            app.setActiveSubject(subject)

            project.addSubject(subject)
            app.sidepanel_projectList.addToList(project.id)
            # KESKEN?
        else:
            activeProject = app.getActiveProject()
            index = len(activeProject.getSubjects())
            subject = Subject(index)

            self.subjectList.insert('end', subject.id)
            self.subjectList.selection_set(0)

            activeProject.addSubject(subject)

            # Update app state
            app.setActiveSubject(subject)

    def addToList(self, id):
        self.subjectList.insert('end', id)

    def updateSelection(self):
        self.subjectList.selection_set('end')

    def refreshList(self):
        activeProject = app.getActiveProject()
        subjects = activeProject.getSubjects()
        print(subjects)
        self.subjectList.delete(0, 'end')
        for s in subjects:
            self.subjectList.insert('end', s.id)

    def handleListboxSelect(self):
        index = self.subjectList.curselection()[0]
        subject = app.getActiveProject().getSubjects()[index]
        app.setActiveSubject(subject)

        app.sidepanel_testList.refreshList()