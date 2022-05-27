import time
from tkinter import *
from tkinter import ttk
from copy import deepcopy
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from objects.app import app
from modules.TestDataImporter import TestDataImporter
from modules.notification import notification

class TestList(object):
    def __init__(self, sidePanel):
        self.container = LabelFrame(sidePanel, text="Tests")
        self.container.pack(fill = BOTH, expand=TRUE)
        self.container.configure(cursor='arrow')
        self.startSel = None

        self.testList = Listbox(self.container, exportselection=FALSE, height=1)
        self.testList.pack(fill = BOTH, expand=TRUE)
        self.testList.bind('<Double-1>', self.handleListboxSelect)
        self.testList.bind('<1>', self.setStartSel)
        self.testList.bind('<Control-Button-1>', lambda e: self.handleMultiSelect(e))
        self.testList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add...', command=self.showAddOptions).grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit...', command=lambda: self.editTest())
        self.editButton.grid(column=1, row=0)
        ttk.Button(buttonContainer, text='Delete', command=lambda: self.deleteTest()).grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=self.testImport).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare...', command=self.showComparisonOptions).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Statistics...', command=self.showMeanOptions).grid(column=2, row=1)

    def testImport(self):
        if len(self.testList.curselection()) == 1:
            subject = app.getActiveSubject()
            tindex = self.testList.curselection()[0]
            test = subject.tests[tindex]
            TestDataImporter(test)
        else: 
            TestDataImporter()

    def setStartSel(self, e):
        self.startSel = f'@{e.x},{e.y}'
        self.testList.selection_set(self.startSel)

    def showAddOptions(self):
        Options(self, 'add')
    
    def addToActiveTest(self):
        subject = app.getActiveSubject()

        if app.activeTest == None:
            emptyTest = Test(id='Joined tests')
            emptyTest.workLoads = []

            for tindex in self.testList.curselection():
                lastLoad = subject.tests[tindex].workLoads[-1]
                loadCopy = deepcopy(lastLoad)
                loadCopy.setName(subject.tests[tindex].id)
                emptyTest.addWorkLoad(loadCopy)
            
            app.setActiveTest(emptyTest)

        else:
            newTest = deepcopy(app.activeTest)
            app.activeTest = newTest
            if app.activeTest.id != 'Joined tests':
                app.activeTest.workLoads[0].name = f'{app.activeTest.parentSubject.parentProject.id}-{app.activeTest.workLoads[0].parentTest.id}'
                app.activeTest.id = 'Joined tests'

            for tindex in self.testList.curselection():
                lastLoad = subject.tests[tindex].workLoads[-1]
                loadCopy = deepcopy(lastLoad)
                loadCopy.setName(f'{subject.parentProject.id}-{subject.tests[tindex].id}')
                app.activeTest.addWorkLoad(loadCopy)
            
        app.testDetailModule.refreshTestDetails()

    def handleShiftSelect(self,e):
        endSel = f'@{e.x},{e.y}'
        self.testList.selection_set(self.startSel, endSel)

    def showMeanOptions(self):
        if len(self.testList.curselection()) > 0:
            Options(self, 'mean')
        else:
            notification.create('error', 'Not a single test selected', '5000')

    def plotMeanSd(self):
        subjects = []
        subjects.append(app.getActiveSubject())
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects)
    
    def plotMeanIqr(self):
        subjects = []
        subjects.append(app.getActiveSubject())
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects, iqr=True)

    def plotMean95(self):
        subjects = []
        subjects.append(app.getActiveSubject())
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects, ci95=True)

    def handleMultiSelect(self, e):
        index = f'@{e.x},{e.y}'
            
        if self.testList.selection_includes(index):
            self.testList.selection_clear(index)
        else:
            self.testList.selection_set(index)

    def showComparisonOptions(self):
        if len(self.testList.curselection()) > 1:
            Options(self, 'compare')
        else:
            notification.create('error', 'Select at least 2 tests for comparison', '5000')

    def compareTests(self, mode):
        comparisonTest = Test()
        comparisonTest.setId('Test comparison')
        comparisonTest.workLoads = []

        if mode == 1:
            for j,i in enumerate(self.testList.curselection()):
                test = app.activeSubject.tests[i]
                testCopy = deepcopy(test)
                lastWorkLoad = testCopy.workLoads[-1]
                lastWorkLoad.setName(f'Test{j+1}')
                comparisonTest.addWorkLoad(lastWorkLoad)
        else:
            for j,i in enumerate(self.testList.curselection()):
                test = app.activeSubject.tests[i]
                testCopy = deepcopy(test)

                for li, l in enumerate(testCopy.workLoads):
                    l.setName(f'{testCopy.id}-L{li}')
                    comparisonTest.addWorkLoad(l)

        app.setActiveTest(comparisonTest)
        # Refresh views
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def editTest(self):
        if len(self.testList.curselection()) < 2:
            index = self.testList.curselection()[0]
            Options(self, 'edit', index)
        else:
            notification.create('error', 'Select only 1 test to edit', 5000)

    def deleteTest(self):
        if len(self.testList.curselection()) > 0:
            subject = app.getActiveSubject()
            tests = subject.getTests()
            toBeDeleted = []

            for i in self.testList.curselection():
                toBeDeleted.append(i)

            # If one of the deleted test is set as active test
            # refresh app state and details panel
            for t in toBeDeleted:
                if app.activeTest == tests[t]:
                    app.setActiveTest(None)
                    app.testDetailModule.refreshTestDetails()
                
            sortedToBeDeleted = sorted(toBeDeleted, reverse=True)
            for i in sortedToBeDeleted:
                subject.deleteTest(i)

            self.refreshList()
        else:
            notification.create('error', 'Select test to be deleted', 5000)

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
            subject = Subject(index, parentProject=project)

            # Add subject to project
            project.addSubject(subject)

            # Add test to subject
            testId = f'{subject.id}-Test-{len(subject.getTests())+1}'
            test = Test(id=testId, parentSubject=subject)
            subject.addTest(test)

            # Update app state
            app.setActiveSubject(subject)
            app.setActiveTest(test)

            #Refresh view
            subjectList = app.sidepanel_subjectList
            subjectList.addToList(subject)
            subjectList.updateSelection()
            self.addToList(test.id)

            # Make current selection
            self.testList.selection_set(0)

        else:
            subject = app.getActiveSubject()
            
            # Add test to subject
            testId = f'{subject.id}-Test-{len(subject.getTests())+1}'
            test = Test(testId, parentSubject=subject)
            subject.addTest(test)

            # Make current selection
            self.testList.insert('end', test.id)
            self.testList.selection_clear(0, 'end')
            self.testList.selection_set('end')

            # Update app state
            app.setActiveTest(test)

        # Create load tab
        app.projectDetailModule.refreshDetails()
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def addToList(self, id):
        self.testList.insert('end', id)
        self.testList.selection_clear(0, 'end')
        self.testList.selection_set('end')

    def refreshList(self, index=None):
        self.testList.delete(0, 'end')
        activeSubject = app.getActiveSubject()
        try:
            tests = activeSubject.getTests()
        except AttributeError:
            tests = []

        for t in tests:
            self.testList.insert('end', t.id)

        if index != None:
            self.testList.select_set(index)

    def handleListboxSelect(self, e):
        try:
            self.testList.selection_clear(0, 'end')

            newIndex= f'@{e.x},{e.y}'
            self.testList.selection_set(newIndex)

            test = app.getActiveSubject().tests[self.testList.curselection()[0]]
            try:
                if test.workLoads[0].details.isImported == True:
                    testCopy = deepcopy(test)
                    app.setActiveTest(testCopy)
                else:
                    app.setActiveTest(test)

                time.sleep(0.05)

                # Refresh views
                app.testDetailModule.refreshTestDetails()
                app.envDetailModule.refresh()
            except:
                notification.create('error', 'No workloads found', 5000)
        except AttributeError:
            pass

class Options():
    def __init__(self, parent, mode, index = None):
        self.parent = parent
        self.mode = mode
        if index != None:
            self.index = index
        
        if self.mode == 'mean':
            self.height = 4
        else:
            self.height = 3

        self.win = Toplevel(width=self.parent.editButton.winfo_reqwidth() * 3, height=self.parent.editButton.winfo_reqheight() * self.height, bg='#4eb1ff', borderwidth=3)
        self.win.overrideredirect(True)
        self.win.focus_force()
        winX = self.parent.editButton.winfo_rootx() - self.parent.editButton.winfo_width()
        winY = self.parent.editButton.winfo_rooty() - (self.parent.editButton.winfo_height() * self.height)
        self.win.geometry("+%d+%d" % ( winX, winY ))
        self.win.pack_propagate(False)

        self.bindId = app.root.bind('<Configure>', self.move)

        container = Frame(self.win, bd=0)
        container.pack(fill=BOTH, expand=True)
        
        footer = Frame(self.win, bd=0)
        footer.pack(fill=BOTH, expand=True)
            
        if self.mode == 'compare':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='All loads of tests', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(container, text='Last loads of tests', variable=self.var, value=1)
            opt2.grid(column=1, row=1, sticky='w')
            ttk.Button(footer, text='Compare', command=self.compare).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)

        elif self.mode == 'mean':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='Mean (SD)', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(container, text='Median (IQR)', variable=self.var, value=1)
            opt2.grid(column=1, row=1, sticky='w')
            opt3 = ttk.Radiobutton(container, text='Mean (95% CI)', variable=self.var, value=2)
            opt3.grid(column=1, row=2, sticky='w')
            ttk.Button(footer, text='Plot', command=self.plotMean).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)

        elif self.mode == 'add':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='Create test', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(container, text='Add final load as tab', variable=self.var, value=1)
            opt2.grid(column=1, row=1, sticky='w')
            ttk.Button(footer, text='Next', command=self.add).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)

        elif self.mode == 'edit':
            ttk.Label(container, text='Test name').pack()
            self.nameEntry = ttk.Entry(container)
            self.nameEntry.pack(expand=TRUE)
            self.nameEntry.insert(0, self.parent.testList.get(self.index))
            ttk.Button(footer, text='Save', command=self.edit).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)
            self.win.bind('<KeyPress-Return>', self.edit)

        self.win.bind('<KeyPress-Escape>', self.close)

    def edit(self, *args):
        test = app.activeSubject.tests[self.index]
        test.setId(self.nameEntry.get())
        self.parent.refreshList(self.index)
        self.close()

    def add(self):
        if self.var.get() == 0:
            self.parent.createTest()
        else:
            self.parent.addToActiveTest()
        self.close()

    def plotMean(self):
        if self.var.get() == 0:
            self.parent.plotMeanSd()
        elif self.var.get() == 1:
            self.parent.plotMeanIqr()
        else:
            self.parent.plotMean95()
        self.close()

    def close(self, *args):
        app.root.unbind('<Configure>', self.bindId)
        self.win.destroy()
        
    def compare(self):
        self.parent.compareTests(self.var.get())
        self.close()

    def move(self, e):
        winX = self.parent.editButton.winfo_rootx() - self.parent.editButton.winfo_width()
        winY = self.parent.editButton.winfo_rooty() - (self.parent.editButton.winfo_height() * self.height)
        self.win.geometry("+%d+%d" % ( winX, winY ))
        self.win.lift()