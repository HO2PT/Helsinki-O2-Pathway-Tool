from tkinter import *
from tkinter import ttk

from objects.app import app
from objects.project import Project
from objects.test import Test
from modules.notification import notification

class ProjectList(object):
    def __init__(self, sidePanel):
        self.startSel = None

        self.container = LabelFrame(sidePanel, text="Projects")
        self.container.pack(fill = BOTH, expand=TRUE)

        self.projectList = Listbox(self.container, exportselection=FALSE, height=1)
        self.projectList.pack(fill = BOTH, expand=TRUE)

        self.projectList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )
        self.projectList.bind('<Control-Button-1>', lambda e: self.handleCtrlSelect(e))
        self.projectList.bind('<Shift-Button-1>', lambda e: self.handleShiftSelect(e))

        buttonContainer = ttk.Frame(self.container)
        buttonContainer.pack()
        self.createButton = ttk.Button(buttonContainer, text='Add', command=lambda: self.createProject())
        self.createButton.grid(column=0, row=0)
        self.editButton = ttk.Button(buttonContainer, text='Edit', command=lambda: self.editProject())
        self.editButton.grid(column=1, row=0)
        self.deleteButton = ttk.Button(buttonContainer, text='Delete', command=lambda: self.deleteProject())
        self.deleteButton.grid(column=2, row=0)
        
        ttk.Button(buttonContainer, text='Import...').grid(column=0, row=1)
        # Mitä halutaan verrata???
        ttk.Button(buttonContainer, text='Compare', command=lambda: self.showComparisonOptions(), state=DISABLED).grid(column=1, row=1)
        ttk.Button(buttonContainer, text='Plot mean', command=lambda: self.showMeanOptions()).grid(column=2, row=1)

    def plotMeanSd(self):
        emptyTest = Test()
        app.plotMean(emptyTest, plotProject=True)
    
    def plotMeanIqr(self):
        emptyTest = Test()
        app.plotMean(emptyTest, plotProject=True, iqr=True)

    def showMeanOptions(self):
        if len(self.projectList.curselection()) == 1:
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
            notification.create('error', 'Select single project for plotting mean figure', '5000')

    def showComparisonOptions(self):
        if len(self.projectList.curselection()) > 1:
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
        app.deleteProject(index)
        self.refreshList()
        app.setActiveProject(None)
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()

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