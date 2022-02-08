from tkinter import *
from tkinter import ttk
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
            index = app.sidepanel_subjectList.subjectList.size()
            subject = Subject(index)

            test = Test()
            subject.addTest(test)
            #print(subject.tests)

            # Update app state
            app.setActiveSubject(subject)
            app.setActiveTest(test)

            #Refresh view
            subjectList = app.sidepanel_subjectList
            subjectList.addToList(subject.id)
            #print(subjectList.subjectList)
            subjectList.updateSelection()
            self.addToTestList(test.id)
            app.testDetailModule.refreshTestDetails()

            # Make current selection
            self.testList.selection_set('end')

        else:
            subject = app.getActiveSubject()
            test = Test()
            subject.addTest(test)

            # Update app state
            app.setActiveTest(test)

            #Refresh view
            self.testList.insert('end', test.id)
            app.testDetailModule.refreshTestDetails()

            # Make current selection
            self.testList.selection_set('end')
            app.sidepanel_projectList.projectList.selection_set(0)

    def addToTestList(self, id):
        self.testList.insert('end', id)

    def refreshList(self):
        activeSubject = app.getActiveSubject()
        tests = activeSubject.getTests()
        print(tests)
        self.testList.delete(0, 'end')
        for t in tests:
            self.testList.insert('end', t.id)

    def handleListboxSelect(self):
        #app.setActiveTest(self.testList.curselection())
        testId = self.testList.curselection()[0]
        app.setActiveTest(app.getActiveSubject().tests[testId])
        app.testDetailModule.refreshTestDetails()