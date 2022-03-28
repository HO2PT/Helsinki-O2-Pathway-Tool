from tkinter import *
from tkinter import ttk
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from objects.app import app
from modules.notification import notification
from modules.DataImporter import DataImporter

class TestList(object):
    def __init__(self, sidePanel):
        self.container = LabelFrame(sidePanel, text="Tests")
        self.container.pack(fill = BOTH, expand=TRUE)
        self.startSel = None

        self.testList = Listbox(self.container, exportselection=FALSE)
        self.testList.pack(fill = BOTH, expand=TRUE)
        self.testList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.testList.bind('<Control-Button-1>', lambda e: self.handleMultiSelect(e))
        self.testList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add', command=lambda: self.createTest()).grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit', command=lambda: self.editTest())
        self.editButton.grid(column=1, row=0)
        ttk.Button(buttonContainer, text='Del', command=lambda: self.deleteTest()).grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=lambda: DataImporter()).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare', command=lambda: self.compareTests()).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Plot mean', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def handleShiftSelect(self,e):
        endSel = f'@{e.x},{e.y}'
        self.testList.selection_set(self.startSel, endSel)

    def showMeanOptions(self):
        if len(self.testList.curselection()) > 0:
            # Create popup
            editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*3, height=self.editButton.winfo_reqheight()*4)
            editscreen.title('Plot options')
            editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth() - 7
            ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
            editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
            editscreen.grid_propagate(False)
                
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(editscreen, text='Mean/SD', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(editscreen, text='Mean/IQR', variable=self.var, value=1)
            opt2.grid(column=1, row=1, sticky='w')
            ttk.Button(editscreen, text='Plot', command=lambda: plot()).grid(column=3, row=3, sticky='se')

            def plot():
                if self.var.get() == 0:
                    self.plotMeanSd()
                else:
                    self.plotMeanIqr()
                editscreen.destroy()
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

    def handleMultiSelect(self, e):
        index = f'@{e.x},{e.y}'
            
        if self.testList.selection_includes(index):
            self.testList.selection_clear(index)
        else:
            self.testList.selection_set(index)

    def compareTests(self):
        if len(self.testList.curselection()) > 1:
            comparisonTest = Test()
            comparisonTest.setId('Test comparison')
            comparisonTest.workLoads = []

            for j,i in enumerate(self.testList.curselection()):
                test = app.getActiveSubject().getTests()[i]
                # print( f'index: {i} - {test.id}' )
                lastWorkLoad = test.getWorkLoads()[-1]
                lastWorkLoad.name = f'Test{j+1}'
                comparisonTest.addWorkLoad(lastWorkLoad)

            # print(comparisonTest.getWorkLoads())
            # print(self.testList.curselection())
            app.setActiveTest(comparisonTest)
            # Refresh views
            app.testDetailModule.refreshTestDetails()
            app.envDetailModule.refresh()
        else:
            notification.create('error', 'Select at least 2 tests for comparison', '5000')

    def editTest(self):
        index = self.testList.curselection()[0]

        # Create edit popup
        editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*3, height=self.editButton.winfo_reqheight()*3)
        editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth() - 7
        ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
        editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
        editscreen.pack_propagate(False)
        
        ttk.Label(editscreen, text='Test name').pack()
        nameEntry = ttk.Entry(editscreen)
        nameEntry.pack(expand=TRUE)
        ttk.Button(editscreen, text='Save', command=lambda: edit()).pack(side=BOTTOM,anchor='e')

        def edit():
            test = app.getActiveTest()
            test.setId(nameEntry.get())
            self.refreshList()
            editscreen.destroy()

    def deleteTest(self):
        subject = app.getActiveSubject()
        tests = subject.getTests()
        toBeDeleted = []

        for i in self.testList.curselection():
            toBeDeleted.append(i)
            
        sortedToBeDeleted = sorted(toBeDeleted, reverse=True)
        for i in sortedToBeDeleted:
            del tests[i]
        
        app.setActiveTest(None)
        # app.testDetailModule.refreshTestDetails()
        self.refreshList()

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
            testId = f'{subject.id}-Test-{len(subject.getTests())+1}'
            test = Test(id=testId)
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
            test = Test(testId)
            subject.addTest(test)

            # Make current selection
            self.testList.insert('end', test.id)
            self.testList.selection_clear(0, 'end')
            self.testList.selection_set('end')

            # Update app state
            app.setActiveTest(test)

        # Add test to app
        #app.plottedTests.append(test)

        # Create load tab
        app.projectDetailModule.refreshDetails()
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def addToList(self, id):
        self.testList.insert('end', id)
        self.testList.selection_clear(0, 'end')
        self.testList.selection_set('end')

    def refreshList(self):
        self.testList.delete(0, 'end')
        activeSubject = app.getActiveSubject()
        try:
            tests = activeSubject.getTests()
        except AttributeError:
            tests = []
        #print(tests)
        #self.testList.delete(0, 'end')
        for t in tests:
            self.testList.insert('end', t.id)

    def handleListboxSelect(self):
        # Set selected subject as active subject by index
        index = self.testList.curselection()[0]
        self.startSel = index
        test = app.getActiveSubject().tests[index]

        # Prevent updating test details when multiple tests selected
        if len(self.testList.curselection()) < 2:
            # Refresh app state
            app.setActiveTest(test)

            # Refresh views
            app.testDetailModule.refreshTestDetails()
            app.envDetailModule.refresh()