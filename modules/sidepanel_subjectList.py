from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.project import Project
from objects.subject import Subject
from modules.notification import notification
from modules.DataImporter import DataImporter
from objects.test import Test

class SubjectList(object):
    def __init__(self, sidePanel):
        self.container = LabelFrame(sidePanel, text="Subjects")
        self.container.pack(fill = BOTH, expand=TRUE)
        self.startSel = None

        self.subjectList = Listbox(self.container, exportselection=FALSE)
        self.subjectList.pack(fill = BOTH, expand=TRUE)
        self.subjectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.subjectList.bind('<Control-Button-1>', lambda e: self.handleCtrlSelect(e))
        self.subjectList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add', command=lambda: self.createSubject()).grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit', command=lambda: self.editSubject())
        self.editButton.grid(column=1, row=0)
        ttk.Button(buttonContainer, text='Del', command=lambda: self.deleteSubject()).grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=lambda: DataImporter()).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare', command=lambda: self.showComparisonOptions()).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Plot mean', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def showMeanOptions(self):
        if len(self.subjectList.curselection()) > 0:
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
            notification.create('error', 'Not a single project selected', '5000')

    def plotMeanSd(self):
        subjects = []
        for i in self.subjectList.curselection():
            subjects.append(app.getActiveProject().getSubjects()[i])
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects)
    
    def plotMeanIqr(self):
        subjects = []
        for i in self.subjectList.curselection():
            subjects.append(app.getActiveProject().getSubjects()[i])
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects, iqr=True)

    def handleShiftSelect(self,e):
        endSel = f'@{e.x},{e.y}'
        self.subjectList.selection_set(self.startSel, endSel)

    def handleCtrlSelect(self, e):
        index = f'@{e.x},{e.y}'
            
        if self.subjectList.selection_includes(index):
            self.subjectList.selection_clear(index)
        else:
            self.subjectList.selection_set(index)

    def compareSubjects(self, n):
        #print(n)
        comparisonTest = Test()
        comparisonTest.setId('Subject comparison')
        comparisonTest.workLoads = []

        for j,i in enumerate(self.subjectList.curselection()):
            subject = app.getActiveProject().getSubjects()[i]
            test = subject.getTests()[n]
            # print( f'index: {i} - {test.id}' )
            lastWorkLoad = test.getWorkLoads()[-1]
            lastWorkLoad.name = f'{subject.id}-Test{n+1}'
            comparisonTest.addWorkLoad(lastWorkLoad)

        # print(comparisonTest.getWorkLoads())
        # print(self.testList.curselection())
        app.setActiveTest(comparisonTest)
        # Refresh views
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def showComparisonOptions(self):
        if len(self.subjectList.curselection()) > 1:
            # Create edit popup
            editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*3, height=self.editButton.winfo_reqheight()*4)
            editscreen.title('Compare')
            editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth() - 7
            ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
            editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
            editscreen.grid_propagate(False)
            
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(editscreen, text='First tests', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(editscreen, text='Last tests', variable=self.var, value=-1)
            opt2.grid(column=1, row=1, sticky='w')
            opt32 = ttk.Entry(editscreen, width=3)
            opt3 = ttk.Radiobutton(editscreen, text='Test number', variable=self.var, value=-999)
            opt3.grid(column=1, row=2, sticky='w')
            opt32.grid(column=2, row=2, sticky='w')
            ttk.Button(editscreen, text='Save', command=lambda: close()).grid(column=3, row=3, sticky='se')

            def close():
                if self.var.get() == -999:
                    self.compareSubjects(int(opt32.get())-1)
                else:
                    self.compareSubjects(self.var.get())
                editscreen.destroy()
        else:
            notification.create('error', 'Select at least 2 subjects for comparison', '5000')

    def editSubject(self):
        index = self.subjectList.curselection()[0]

        # Create edit popup
        editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*3, height=self.editButton.winfo_reqheight()*3)
        editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth() - 7
        ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
        editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
        editscreen.pack_propagate(False)
        
        ttk.Label(editscreen, text='Subject name').pack()
        nameEntry = ttk.Entry(editscreen)
        nameEntry.pack(expand=TRUE)
        ttk.Button(editscreen, text='Save', command=lambda: edit()).pack(side=BOTTOM,anchor='e')

        def edit():
            subject = app.getActiveSubject()
            subject.setId(nameEntry.get())
            self.refreshList()
            editscreen.destroy()

    def deleteSubject(self):
        project = app.getActiveProject()
        subjects = project.getSubjects()
        toBeDeleted = []

        for i in self.subjectList.curselection():
            toBeDeleted.append(i)

        sortedToBeDeleted = sorted(toBeDeleted, reverse=True)
        for i in sortedToBeDeleted:
            del subjects[i]

        app.setActiveSubject(None)
        self.refreshList()
        app.sidepanel_testList.refreshList()

    def createSubject(self):
        if app.getActiveProject() == None:
            # Create project and make it active
            project = Project()
            app.setActiveProject(project)
            app.addProject(project)

            # Create subject with index based on the size of project subject list
            index = self.subjectList.size()
            subject = Subject(index)

            # Append subject to list
            self.addToList(subject)
            
            # Update app state
            app.setActiveSubject(subject)

            project.addSubject(subject)
            app.sidepanel_projectList.addToList(project.id)
        else:
            # Create subject with index based on the size of project subject list
            activeProject = app.getActiveProject()
            index = len(activeProject.getSubjects())
            subject = Subject(index)

            # Append subject to list
            self.addToList(subject)

            # Update app state
            app.setActiveSubject(subject)
            app.setActiveTest(None)

            activeProject.addSubject(subject)
        
        # Refresh project details (=subject count)
        app.projectDetailModule.refreshDetails()
        app.sidepanel_testList.refreshList()

    def addToList(self, subject):
        id = subject.id
        i = 0
        while True:
            if id in self.subjectList.get(0, 'end'):
                subject.setId(f'Subject{i}')
                id = subject.id
                i += 1
            else:
                break
        self.subjectList.insert('end', id)
        self.subjectList.selection_clear(0, 'end')
        self.subjectList.selection_set('end')

    def updateSelection(self):
        self.subjectList.selection_set('end')

    def refreshList(self):
        activeProject = app.getActiveProject()
        try:
            subjects = activeProject.getSubjects()
        except AttributeError:
            subjects = []
        #print(subjects)
        self.subjectList.delete(0, 'end')
        for s in subjects:
            self.subjectList.insert('end', s.id)

    def handleListboxSelect(self):
        # Set selected subject as active subject by index
        index = self.subjectList.curselection()[0]
        self.startSel = index
        subject = app.getActiveProject().getSubjects()[index]
        
        # Refresh app state
        app.setActiveSubject(subject)
        app.setActiveTest(None)

        # Refresh views
        app.sidepanel_testList.refreshList()