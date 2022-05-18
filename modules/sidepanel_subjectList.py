from cmath import exp
from copy import deepcopy
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
        self.container.configure(cursor='arrow')
        self.startSel = None

        self.subjectList = Listbox(self.container, exportselection=FALSE, height=1)
        self.subjectList.pack(fill = BOTH, expand=TRUE)
        self.subjectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.subjectList.bind('<Control-Button-1>', lambda e: self.handleCtrlSelect(e))
        self.subjectList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        ttk.Button(buttonContainer, text='Add...', command=self.showCreateOptions).grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit...', command=lambda: self.editSubject())
        self.editButton.grid(column=1, row=0)
        ttk.Button(buttonContainer, text='Delete', command=lambda: self.deleteSubject()).grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=lambda: DataImporter()).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare...', command=lambda: self.showComparisonOptions()).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Statistics...', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def showCreateOptions(self):
        Options(self, 'add')
    
    def showComparisonOptions(self):
        if len(self.subjectList.curselection()) > 1:
            Options(self, 'compare')
        else:
            notification.create('error', 'Select at least 2 subjects for comparison', '5000')
    
    def showMeanOptions(self):
        if len(self.subjectList.curselection()) > 0:
            Options(self, 'mean')
            """ # Create popup
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
                editscreen.destroy() """
        else:
            notification.create('error', 'Subject not selected', '5000')

    def addToActiveTest(self):
        project = app.getActiveProject()

        if app.activeTest == None:
            emptyTest = Test(id='Joined subjects')
            emptyTest.workLoads = []

            for sindex in self.subjectList.curselection():
                lastTest = project.getSubjects()[sindex].tests[-1]
                lastLoad = lastTest.workLoads[-1]
                loadCopy = deepcopy(lastLoad)
                loadCopy.setName(lastTest.id)
                emptyTest.addWorkLoad(loadCopy)
            
            app.setActiveTest(emptyTest)

        else:
            newTest = deepcopy(app.activeTest)
            app.activeTest = newTest
            if app.activeTest.id != 'Joined subjects':
                app.activeTest.workLoads[0].setName(f'{app.activeTest.parentSubject.parentProject.id}-{app.activeTest.workLoads[0].parentTest.id}')
                app.activeTest.id = 'Joined subjects'
            # else:
            #     app.activeTest.workLoads[0].name = f'{app.activeTest.parentSubject.parentProject.id}-{app.activeTest.workLoads[0].name}'

            for sindex in self.subjectList.curselection():
                lastTest = project.getSubjects()[sindex].tests[-1]
                lastLoad = lastTest.workLoads[-1]
                loadCopy = deepcopy(lastLoad)
                loadCopy.setName(f'{project.id}-{lastTest.id}')
                app.activeTest.addWorkLoad(loadCopy)

        app.testDetailModule.refreshTestDetails()

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
    
    def plotMean95(self):
        subjects = []
        for i in self.subjectList.curselection():
            subjects.append(app.getActiveProject().getSubjects()[i])
        emptyTest = Test()
        app.plotMean(test=emptyTest, subjects=subjects, ci95=True)

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
            loadCopy = deepcopy(lastWorkLoad)
            loadCopy.setName(f'{subject.id}-Test{n+1}')
            comparisonTest.addWorkLoad(loadCopy)

        # print(comparisonTest.getWorkLoads())
        # print(self.testList.curselection())
        app.setActiveTest(comparisonTest)
        # Refresh views
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def editSubject(self):
        if len(self.subjectList.curselection()) < 2:
            index = self.subjectList.curselection()[0]
            Options(self, 'edit', index)
        else:
            notification.create('error', 'Select only 1 subject to edit', 5000)

    def deleteSubject(self):
        if len(self.subjectList.curselection()) > 0:
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
        else:
            notification.create('error', 'Select subject to be deleted', 5000)

    def createSubject(self):
        if app.getActiveProject() == None:
            # Create project and make it active
            project = Project()
            app.setActiveProject(project)
            app.addProject(project)

            # Create subject with index based on the size of project subject list
            index = self.subjectList.size()
            subject = Subject(index, parentProject=project)

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
            subject = Subject(index, parentProject=activeProject)

            # Append subject to list
            self.addToList(subject)

            # Update app state
            app.setActiveSubject(subject)
            # app.setActiveTest(None)

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

    def combineAndAdd(self):
        project = app.activeProject
        subjects = []
        emptyTest = Test(id='Combined subjects')
        emptyTest.workLoads = []

        for sindex in self.subjectList.curselection():
            subjects.append(project.getSubjects()[sindex])
            
        VO2mean, Qmean, HBmean, SAO2mean = app.getMaxMinAvg(subjects=subjects)
        # print(VO2mean, Qmean, HBmean, SAO2mean)
        createdLoad = emptyTest.createLoad()
        createdLoad.details.setValue('VO2', VO2mean)
        createdLoad.details.setValue('Q', Qmean)
        createdLoad.details.setValue('[Hb]', HBmean)
        createdLoad.details.setValue('SaO2', SAO2mean)

        if app.activeTest == None:
            app.setActiveTest(emptyTest)
        else:
            app.activeTest.addWorkLoad(createdLoad)    
        
        app.testDetailModule.refreshTestDetails()
        app.envDetailModule.refresh()

    def updateSelection(self):
        self.subjectList.selection_set('end')

    def refreshList(self, index=None):
        activeProject = app.getActiveProject()
        try:
            subjects = activeProject.getSubjects()
        except AttributeError:
            subjects = []
        #print(subjects)
        self.subjectList.delete(0, 'end')
        for s in subjects:
            self.subjectList.insert('end', s.id)

        # If the index of current selection is given, use it
        if index != None:
            self.subjectList.select_set(index)

    def handleListboxSelect(self):
        try:
            # Set selected subject as active subject by index
            index = self.subjectList.curselection()[0]
            self.startSel = index
            subject = app.getActiveProject().getSubjects()[index]
            
            # Refresh app state
            app.setActiveSubject(subject)
            # app.setActiveTest(None)

            # Refresh views
            app.sidepanel_testList.refreshList()
        except IndexError:
            pass
        
class Options():
    def __init__(self, parent, mode, index = None):
        self.parent = parent
        self.mode = mode
        if index != None:
            self.index = index

        if self.mode == 'compare' or self.mode == 'mean' or self.mode == 'add':
            self.height = 4
        else:
            self.height = 3

        self.win = Toplevel(width=(self.parent.editButton.winfo_width() * 3), height=self.parent.editButton.winfo_height() * self.height, bg='#4eb1ff', borderwidth=3)
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
                
        if self.mode == 'add':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='Create subject', variable=self.var, value=0)
            opt1.grid(column=0, row=0, sticky='w', columnspan=2)
            opt2 = ttk.Radiobutton(container, text="Add last test's final load(s) as tab", variable=self.var, value=1)
            opt2.grid(column=0, row=1, sticky='w', columnspan=2)
            opt3 = ttk.Radiobutton(container, text="Combine max. loads and add as tab", variable=self.var, value=2)
            opt3.grid(column=0, row=2, sticky='w', columnspan=2)
            ttk.Button(footer, text='Next', command=self.add).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)
        
        elif self.mode == 'compare':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='Last loads of first tests', variable=self.var, value=0)
            opt1.grid(column=0, row=0, sticky='w')
            opt2 = ttk.Radiobutton(container, text='Last loads of last tests', variable=self.var, value=-1)
            opt2.grid(column=0, row=1, sticky='w')
            self.opt32 = ttk.Entry(container, width=3)
            opt3 = ttk.Radiobutton(container, text='Last Load of test number', variable=self.var, value=-999)
            opt3.grid(column=0, row=2, sticky='w')
            self.opt32.grid(column=1, row=2, sticky='w')
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
        
        elif self.mode == 'edit':
            ttk.Label(container, text='Subject name').pack()
            self.nameEntry = ttk.Entry(container)
            self.nameEntry.pack(expand=TRUE)
            self.nameEntry.insert(0, self.parent.subjectList.get(self.index))
            ttk.Button(footer, text='Save', command=self.edit).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)
            self.win.bind('<KeyPress-Return>', self.edit)
            
        self.win.bind('<KeyPress-Escape>', self.close)

    def edit(self, *args):
        oldName = self.parent.subjectList.get(self.index)
        subject = app.getActiveSubject()
        subject.setId(self.nameEntry.get())
        self.parent.refreshList(self.index)

        # If the subject's name is used in naming the tests, update tests as well
        for t in subject.tests:
            if oldName in t.id:
                t.id = t.id.replace(oldName, self.nameEntry.get())
        app.sidepanel_testList.refreshList()

        self.close()

    def add(self):
        if self.var.get() == 0:
            self.parent.createSubject()
        elif self.var.get() == 1:
            self.parent.addToActiveTest()
        else:
            self.parent.combineAndAdd()
        self.close()
        
    def close(self, *args):
        app.root.unbind('<Configure>', self.bindId)
        self.win.destroy()

    def compare(self):
        if self.var.get() == -999:
            self.parent.compareSubjects(int(self.opt32.get())-1)
        else:
            self.parent.compareSubjects(self.var.get())
        self.close()

    def plotMean(self):
        if self.var.get() == 0:
            self.parent.plotMeanSd()
        elif self.var.get() == 1:
            self.parent.plotMeanIqr()
        else:
            self.parent.plotMean95()
        self.close()

    def move(self, e):
        winX = self.parent.editButton.winfo_rootx() - self.parent.editButton.winfo_width()
        winY = self.parent.editButton.winfo_rooty() - (self.parent.editButton.winfo_height() * self.height)
        self.win.geometry("+%d+%d" % ( winX, winY ))
        self.win.lift()