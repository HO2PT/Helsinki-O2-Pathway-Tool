from tkinter import *
from tkinter import ttk

from objects.app import app
from objects.project import Project
from objects.test import Test
from modules.notification import notification
from modules.DataImporter import DataImporter

class ProjectList(object):
    def __init__(self, sidePanel):
        self.startSel = None

        self.container = LabelFrame(sidePanel, text="Projects")
        self.container.pack(fill = BOTH, expand=TRUE)
        self.container.configure(cursor='arrow')

        self.projectList = Listbox(self.container, exportselection=FALSE, height=1)
        self.projectList.pack(fill = BOTH, expand=TRUE)

        self.projectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.projectList.bind('<Control-Button-1>', lambda e: self.handleCtrlSelect(e))
        self.projectList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        self.createButton = ttk.Button(buttonContainer, text='Add...', command=lambda: self.createProject())
        self.createButton.grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit...', command=lambda: self.editProject())
        self.editButton.grid(column=1, row=0)
        self.deleteButton = ttk.Button(buttonContainer, text='Delete', command=lambda: self.deleteProject())
        self.deleteButton.grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...', command=lambda: DataImporter()).grid(column=0, row=1)
        ttk.Button(buttonContainer, text='Compare', command=lambda: self.showComparisonOptions(), state=DISABLED).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Statistics...', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def plotMeanSd(self):
        emptyTest = Test()
        app.plotMean(emptyTest, plotProject=True)
    
    def plotMeanIqr(self):
        emptyTest = Test()
        app.plotMean(emptyTest, plotProject=True, iqr=True)

    def plotMean95(self):
        emptyTest = Test()
        app.plotMean(emptyTest, plotProject=True, ci95=True)

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
        if len(self.projectList.curselection()) < 2:
            index = self.projectList.curselection()[0]
            Options(self, 'edit', index)
        else:
            notification.create('error', 'Select only 1 project to edit', 5000)

    def deleteProject(self):
        if len(self.projectList.curselection()) > 0:
            index = self.projectList.curselection()[0]
            app.deleteProject(index)
            self.refreshList()
            app.setActiveProject(None)
            app.sidepanel_subjectList.refreshList()
            app.sidepanel_testList.refreshList()
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
        # app.setActiveTest(None)

        # Refresh views
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

    def handleListboxSelect(self):
        # Set selected project as active project by clicked index
        index = self.projectList.curselection()[0]
        self.startSel = index
        project = app.projects[index]
        app.setActiveProject(project)

        # Refresh app state
        app.setActiveSubject(None)
        # app.setActiveTest(None)

        # Refresh views
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

class Options():
    def __init__(self, parent, mode, index=None):
        self.parent = parent
        self.mode = mode
        if index != None:
            self.index = index

        if self.mode == 'compare' or self.mode == 'mean':
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
    
    def close(self, *args):
        app.root.unbind('<Configure>', self.bindId)
        self.win.destroy()

    def move(self, e):
        winX = self.parent.editButton.winfo_rootx() - self.parent.editButton.winfo_width()
        winY = self.parent.editButton.winfo_rooty() - (self.parent.editButton.winfo_height() * self.height)
        self.win.geometry("+%d+%d" % ( winX, winY ))
        self.win.lift()