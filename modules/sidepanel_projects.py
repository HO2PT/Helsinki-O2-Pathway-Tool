from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from modules.notification import notification
from modules.ProjectDataImporter import ProjectDataImporter
from copy import deepcopy

class ProjectList(object):
    def __init__(self, sidePanel):
        self.startSel = None

        self.container = ttk.LabelFrame(sidePanel, text="Projects")
        self.container.pack(fill = BOTH, expand=TRUE)
        self.container.configure(cursor='arrow')

        if app.platform == 'darwin':
            self.projectList = Listbox(
                self.container,
                exportselection=FALSE, 
                height=1, 
                activestyle='none', 
                background='#F5F6F7',
                highlightbackground='#F5F6F7',
                fg='black')
        else:
            self.projectList = Listbox(
                self.container, 
                exportselection=FALSE, 
                height=1, 
                activestyle='none')
        
        self.projectList.pack(fill = BOTH, expand=TRUE)

        self.projectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.projectList.bind('<Control-Button-1>', lambda e: self.handleCtrlSelect(e))
        self.projectList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))
        self.projectList.bind('<3>', self.deselectList)

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        # self.createButton = ttk.Button(buttonContainer, text='Add...', command=lambda: self.createProject())
        self.createButton = ttk.Button(buttonContainer, text='Add...', command=lambda: self.showCreateOptions())
        self.createButton.grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit...', command=lambda: self.editProject())
        self.editButton.grid(column=1, row=0)
        self.deleteButton = ttk.Button(buttonContainer, text='Delete', command=lambda: self.deleteProject())
        self.deleteButton.grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=lambda: ProjectDataImporter()).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare', command=lambda: self.showComparisonOptions(), state=DISABLED).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Statistics...', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def deselectList(self, e):
        self.projectList.select_clear(0, END)
        app.activeProject = None
        app.activeSubject = None
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

    def plotMeanSd(self):
        parentSubject = Subject(parentProject=app.activeProject)
        emptyTest = Test(parentSubject=parentSubject)
        app.plotMean(emptyTest, plotProject=True)
    
    def plotMeanIqr(self):
        parentSubject = Subject(parentProject=app.activeProject)
        emptyTest = Test(parentSubject=parentSubject)
        app.plotMean(emptyTest, plotProject=True, iqr=True)

    def plotMean95(self):
        parentSubject = Subject(parentProject=app.activeProject)
        emptyTest = Test(parentSubject=parentSubject)
        app.plotMean(emptyTest, plotProject=True, ci95=True)

    def showCreateOptions(self):
        Options(self, 'add')

    def showMeanOptions(self):
        if len(self.projectList.curselection()) == 1:
            Options(self, 'mean')
        else:
            notification.create('error', 'Select single project for plotting mean figure', '5000')

    def showComparisonOptions(self):
        if len(self.projectList.curselection()) > 1:
            Options(self, 'compare')
        else:
            notification.create('error', 'Select at least 2 projects for comparison', '5000')

    def handleCtrlSelect(self, e):
        index = f'@{e.x},{e.y}'
            
        if self.projectList.selection_includes(index):
            self.projectList.selection_clear(index)
        else:
            self.projectList.selection_set(index)
    
    def handleShiftSelect(self,e):
        endSel = f'@{e.x},{e.y}'
        self.projectList.selection_set(self.startSel, endSel)

    def editProject(self):
        try:
            if len(self.projectList.curselection()) < 2:
                index = self.projectList.curselection()[0]
                Options(self, 'edit', index)
            else:
                notification.create('error', 'Select only 1 project to edit', 5000)
        except:
            notification.create('error', 'Select at least 1 project to edit', 5000)

    def deleteProject(self):
        if len(self.projectList.curselection()) > 0:
            toBeDeleted = []

            for p in self.projectList.curselection():
                toBeDeleted.append(p)

            sortedToBeDeleted = sorted(toBeDeleted, reverse=True)
            for i in sortedToBeDeleted:
                del app.projects[i]
            
            self.refreshList()
            app.activeProject = None
            app.activeSubject = None
            app.sidepanel_subjectList.refreshList()
            app.sidepanel_testList.refreshList()
            app.projectDetailModule.refreshDetails()
        else:
            notification.create('error', 'Select project to be deleted', 5000)

    def refreshList(self, index=None):
        projects = app.getProjects()
        self.projectList.delete(0, 'end')
        for p in projects:
            self.projectList.insert('end', p.id)

        # If the index of current selection is given, use it
        if index != None:
            self.projectList.select_set(index)

    def addToList(self, id):
        self.projectList.insert('end', id)
        self.projectList.selection_clear(0, 'end')
        self.projectList.selection_set('end')

    def createProject(self):
        project = Project()
        self.projectList.insert('end', project.id)
        self.projectList.selection_clear(0, 'end')
        self.projectList.selection_set('end')

        # Update app state
        app.addProject(project)
        app.setActiveProject(project)
        app.setActiveSubject(None)
        # app.setActiveTest(None)

        # Refresh views
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

    def addMeanToActiveTest(self):
        parentSubject = Subject(parentProject=app.activeProject)
        emptyTest = Test(parentSubject=parentSubject)
        app.plotMean(emptyTest, plotProject=True, export=True) # Use the export to prevent plotting

        if app.activeTest == None:
            emptyTest.id = 'Joined data'
            # emptyTest.workLoads[0].name = f'{app.activeProject.id}(Mean)'
            app.setActiveTest(deepcopy(emptyTest))

        else:
            newTest = deepcopy(app.activeTest)
            app.activeTest = newTest
            if app.activeTest.id != 'Joined data':
                # app.activeTest.workLoads[0].setName(f'{app.activeTest.parentSubject.parentProject.id}-{app.activeTest.workLoads[0].parentTest.id}')
                app.activeTest.id = 'Joined data'

            loadCopy = deepcopy(emptyTest.workLoads[1])
            loadCopy.setName(f'{app.activeProject.id}-Mean')
            app.activeTest.addWorkLoad(loadCopy)

        app.testDetailModule.refreshTestDetails()

    def addMedianToActiveTest(self):
        parentSubject = Subject(parentProject=app.activeProject)
        emptyTest = Test(parentSubject=parentSubject)
        app.plotMean(emptyTest, plotProject=True, iqr=True, export=True) # Use the export to prevent plotting

        if app.activeTest == None:
            emptyTest.id = 'Joined data'
            # emptyTest.workLoads[0].name = f'{app.activeProject.id}(Median)'
            app.setActiveTest(deepcopy(emptyTest))

        else:
            newTest = deepcopy(app.activeTest)
            app.activeTest = newTest
            if app.activeTest.id != 'Joined data':
                # app.activeTest.workLoads[0].setName(f'{app.activeTest.parentSubject.parentProject.id}-{app.activeTest.workLoads[0].parentTest.id}')
                app.activeTest.id = 'Joined data'

            loadCopy = deepcopy(emptyTest.workLoads[1])
            loadCopy.setName(f'{app.activeProject.id}-Median')
            app.activeTest.addWorkLoad(loadCopy)

        app.testDetailModule.refreshTestDetails()

    def handleListboxSelect(self):
        # Set selected project as active project by clicked index
        try:
            index = self.projectList.curselection()[0]
            self.startSel = index
            project = app.projects[index]
            app.setActiveProject(project)

            # Refresh app state
            app.setActiveSubject(None)

            # Refresh views
            app.sidepanel_subjectList.refreshList()
            app.sidepanel_testList.refreshList()
            app.projectDetailModule.refreshDetails()
        except IndexError:
            pass

class Options():
    def __init__(self, parent, mode, index=None):
        self.parent = parent
        self.mode = mode
        if index != None:
            self.index = index

        if self.mode == 'compare' or self.mode == 'add' or self.mode == 'mean':
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

        if app.platform == 'linux':
            container = Frame(self.win, bd=0, bg='#EFEBE7')
            footer = Frame(self.win, bd=0, bg='#EFEBE7')
        elif app.platform == 'darwin':
            container = Frame(self.win, bd=0, bg='#F5F6F7')
            footer = Frame(self.win, bd=0, bg='#F5F6F7')
        else:
            container = Frame(self.win, bd=0)
            footer = Frame(self.win, bd=0)
        
        container.pack(fill=BOTH, expand=True)
        footer.pack(fill=BOTH, expand=True)

        if self.mode == 'mean':
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
            ttk.Label(container, text='Project name').pack()
            self.nameEntry = ttk.Entry(container)
            self.nameEntry.pack(expand=TRUE)
            self.nameEntry.insert(0, app.getProjects()[self.index].id)
            ttk.Button(footer, text='Save', command=self.edit).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)
            self.win.bind('<KeyPress-Return>', self.edit)

        elif self.mode == 'compare':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='First tests', variable=self.var, value=0)
            opt1.grid(column=1, row=0, sticky='w')
            opt2 = ttk.Radiobutton(container, text='Last tests', variable=self.var, value=-1)
            opt2.grid(column=1, row=1, sticky='w')
            self.opt32 = ttk.Entry(container, width=3)
            opt3 = ttk.Radiobutton(container, text='Test number', variable=self.var, value=-999)
            opt3.grid(column=1, row=2, sticky='w')
            self.opt32.grid(column=2, row=2, sticky='w')
            ttk.Button(footer, text='Save', command=lambda: None).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)

        elif self.mode == 'add':
            self.var = IntVar(value=0)
            opt1 = ttk.Radiobutton(container, text='Create project', variable=self.var, value=0)
            opt1.grid(column=0, row=0, sticky='w', columnspan=2)
            opt2 = ttk.Radiobutton(container, text="Add mean values as tab", variable=self.var, value=1)
            opt2.grid(column=0, row=1, sticky='w', columnspan=2)
            opt3 = ttk.Radiobutton(container, text="Add median values as tab", variable=self.var, value=2)
            opt3.grid(column=0, row=2, sticky='w', columnspan=2)
            ttk.Button(footer, text='Next', command=self.add).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(footer, text='Close', command=self.close).pack(side=LEFT, fill=X, expand=True)
        
        self.win.bind('<KeyPress-Escape>', self.close)

    def close(self):
        if self.var.get() == -999:
            self.compareSubjects(int(self.opt32.get())-1)
        else:
            self.compareSubjects(self.var.get())
        self.close()

    def edit(self, *args):
        project = app.getProjects()[self.index]
        project.setId(self.nameEntry.get())
        self.parent.refreshList(self.index)
        self.close()

    def plotMean(self):
        if self.var.get() == 0:
            self.parent.plotMeanSd()
        elif self.var.get() == 1:
            self.parent.plotMeanIqr()
        else:
            self.parent.plotMean95()
        self.close()

    def add(self):
        if self.var.get() == 0:
            self.parent.createProject()
        elif self.var.get() == 1:
            self.parent.addMeanToActiveTest()
        else:
            self.parent.addMedianToActiveTest()
        self.close()
    
    def close(self, *args):
        app.root.unbind('<Configure>', self.bindId)
        self.win.destroy()

    def move(self, e):
        winX = self.parent.editButton.winfo_rootx() - self.parent.editButton.winfo_width()
        winY = self.parent.editButton.winfo_rooty() - (self.parent.editButton.winfo_height() * self.height)
        self.win.geometry("+%d+%d" % ( winX, winY ))
        self.win.lift()