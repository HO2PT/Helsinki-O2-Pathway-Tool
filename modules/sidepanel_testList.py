from tkinter import *
from tkinter import ttk
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from objects.app import app

class TestList(object):
    def __init__(self, sidePanel):
        container = LabelFrame(sidePanel, text="Tests")
        container.pack(fill = BOTH, expand=TRUE)

        self.testList = Listbox(container, exportselection=FALSE)
        self.testList.pack(fill = BOTH, expand=TRUE)
        self.testList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        buttonContainer = ttk.Frame(container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add', command=lambda: self.createTest()).pack(side=LEFT)
        ttk.Button(buttonContainer, text='Edit').pack(side=LEFT)
        ttk.Button(buttonContainer, text='Del').pack(side=LEFT)
        
        ttk.Button(container, text='Import...').pack()

    def createTest(self):
        # Check if there is an active subject or should subject be created
        if app.getActiveSubject() == None:

            # Check if there is an active project
            if app.getActiveProject() == None:
                # Create project and set it active
                project = Project()
                app.setActiveProject(project)

                # Update app state
                app.sidepanel_projectList.addToList(project.id)
                app.addProject(project)
            else:
                project = app.getActiveProject()

            # Create subject with index based on the size of subject list
            index = len(project.getSubjects())
            subject = Subject(index)

            # Add subject to project
            project.addSubject(subject)

            # Add test to subject
            test = Test()
            subject.addTest(test)

            # Update app state
            app.setActiveSubject(subject)
            app.setActiveTest(test)

            #Refresh view
            subjectList = app.sidepanel_subjectList
            subjectList.addToList(subject.id)
            subjectList.updateSelection()
            self.addToList(test.id)

            # Make current selection
            self.testList.selection_set(0)

        else:
            subject = app.getActiveSubject()
            
            # Add test to subject
            test = Test()
            subject.addTest(test)

            # Make current selection
            self.testList.insert('end', test.id)
            self.testList.selection_clear(0, 'end')
            self.testList.selection_set('end')

            # Update app state
            app.setActiveTest(test)

        # Create load tab
        #print(test.workLoads)
        app.getActiveTest().initWorkLoad()
        app.projectDetailModule.refreshDetails()
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def addToList(self, id):
        self.testList.insert('end', id)
        self.testList.selection_clear(0, 'end')
        self.testList.selection_set('end')

    def refreshList(self):
        activeSubject = app.getActiveSubject()
        try:
            tests = activeSubject.getTests()
        except AttributeError:
            tests = []
        #print(tests)
        self.testList.delete(0, 'end')
        for t in tests:
            self.testList.insert('end', t.id)

    def handleListboxSelect(self):
        # Set selected subject as active subject by index
        index = self.testList.curselection()[0]
        test = app.getActiveSubject().tests[index]
        
        # Refresh app state
        app.setActiveTest(test)

        # Refresh views
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()