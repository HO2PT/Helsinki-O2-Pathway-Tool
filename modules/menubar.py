from tkinter import *
from modules.Help import Help
from modules.About import About
from objects.app import app
from objects.test import Test
from modules.notification import notification
from modules.ProjectDataImporter import ProjectDataImporter
from modules.DataExporter import DataExporter
from modules.TestDataImporter import TestDataImporter
from modules.SubjectDataImporter import SubjectDataImporter

class MenuBar(object):
    def __init__(self, root):
        self.menuBar = Menu(root)

        # Adding File Menu and commands
        file = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='File', menu = file)
        
        # File... -> Import...
        importFile = Menu(self.menuBar, tearoff = 0)
        importFile.add_command(label ='Project...', command = lambda: ProjectDataImporter())
        importFile.add_command(label ='Subject...', command = lambda: SubjectDataImporter())
        importFile.add_command(label ='Test...', command = lambda: TestDataImporter())
        
        # File... -> Export... -> Project...
        exportMenuProject = Menu(self.menuBar, tearoff=0)
        exportMenuProject.add_command(label='Project to new file...', command=lambda: DataExporter(toNew=1))
        exportMenuProject.add_command(label='Project to imported file...', command=lambda: DataExporter(toNew=0))
        
        # File... -> Export... -> Plots
        exportMenuPlots = Menu(self.menuBar, tearoff=0)
        exportMenuPlots.add_command(label='Plots to new file...', command=lambda: DataExporter(toNew=1, onlyPlots=1))
        exportMenuPlots.add_command(label='Plots to imported file...', command=lambda: DataExporter(toNew=0, onlyPlots=1))
        
        # File... -> Export...
        exportMenu = Menu(self.menuBar, tearoff=0)
        exportMenu.add_cascade(label='Project...', menu=exportMenuProject)
        exportMenu.add_cascade(label='Subject...', state=DISABLED)
        exportMenu.add_cascade(label='Test...', state=DISABLED)
        exportMenu.add_cascade(label='Plots...', menu=exportMenuPlots)

        # File...
        file.add_cascade(label ='Import...', menu=importFile)
        file.add_cascade(label='Export...', menu=exportMenu)
        file.add_separator()
        file.add_command(label ='Exit', command = root.destroy)

        # Settings
        settings = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='Settings', menu = settings)

        # Settings - default settings
        settings.add_command(label ='Settings...', command = lambda: app.settings.openSettings())
        
        # View
        self.view = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='View', menu = self.view)
        # Check if hidden on startup
        text = self.checkVisibility('side')
        self.view.add_command(label = f'{text} side menu', command = lambda: self.hideSidePanel())
        text = self.checkVisibility('project')
        self.view.add_command(label =f'{text} project details', command = lambda: self.hideProjectDetails())
        text = self.checkVisibility('test')
        self.view.add_command(label =f'{text} test details', command = lambda: self.hideTestDetails())
        text = self.checkVisibility('environment')
        self.view.add_command(label =f'{text} environment details', command = lambda: self.hideEnvDetails())
        text = self.checkVisibility('all')
        self.view.add_command(label =f'{text} all details', command = lambda: self.hideAllDetails())

        # Create demo graph
        self.menuBar.add_command(label ='Create demo graph', command=lambda: self.createDemoGraph())

        # About
        options = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='Help', menu = options)
        options.add_command(label ='Help...', command = lambda: Help())
        options.add_command(label ='About O2 Pathway Tool', command = lambda: About())

    def checkVisibility(self, object):
        if object == 'side':
            try:
                app.sidePanel.sidePanel.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'project':
            try:
                app.projectDetailModule.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'test':
            try:
                app.testDetailModule.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'environment':
            try:
                app.envDetailModule.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'all':
            try:
                app.detailsPanel.detailsPanel.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'

    def getMenubar(self):
        return self.menuBar

    def createDemoGraph(self):
        demoTest = Test()
        demoTest.workLoads[0].setDemoDetails()
        app.setActiveTest(demoTest)
        app.sidepanel_testList.refreshList()
        app.testDetailModule.refreshTestDetails()
        app.plottingPanel.plot()

    def hideAllDetails(self):
        text = self.view.entrycget(4, 'label')
        if text == 'Hide all details':
            self.view.entryconfigure(4, label='Show all details')
        else:
            self.view.entryconfigure(4, label='Hide all details')
        detailsPanel = app.detailsPanel.detailsPanel
        notifPanel = notification.notifPanel
        plottingPanel = app.plottingPanel

        if detailsPanel.winfo_manager():
            detailsPanel.pack_forget()
        else:
            notifPanel.pack_forget()
            plottingPanel.pack_forget()
            notifPanel.pack(fill=X)
            detailsPanel.pack(side=TOP, fill=X)
            plottingPanel.pack(fill=BOTH, expand=TRUE)

    def hideSidePanel(self):
        text = self.view.entrycget(0, 'label')
        if text == 'Hide side menu':
            self.view.entryconfigure(0, label='Show side menu')
        else:
            self.view.entryconfigure(0, label='Hide side menu')
        
        sidePanel = app.sidePanel.sidePanel
        notifPanel = notification.notifPanel
        detailsPanel = app.detailsPanel.detailsPanel
        plottingPanel = app.plottingPanel

        if sidePanel.winfo_manager(): # if visible -> hide
            sidePanel.pack_forget()
        else: # if hidden -> show and reorganize layout
            notifPanel.pack_forget()
            detailsPanel.pack_forget()
            plottingPanel.pack_forget()
            sidePanel.pack(side=LEFT, fill=Y)
            notifPanel.pack(fill=X)
            detailsPanel.pack(side=TOP, fill=X)
            plottingPanel.pack(fill=BOTH, expand=TRUE)

    def hideProjectDetails(self):
        text = self.view.entrycget(1, 'label')
        if text == 'Hide project details':
            self.view.entryconfigure(1, label='Show project details')
        else:
            self.view.entryconfigure(1, label='Hide project details')
        testContainer = app.testDetailModule
        envContainer = app.envDetailModule
        projectContainer = app.projectDetailModule
        
        if projectContainer.winfo_manager():
            projectContainer.pack_forget()
        else:
            testContainer.pack_forget()
            envContainer.pack_forget()

            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, padx=(5,5), anchor='n')
            
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, padx=(5,5), anchor='n')

            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, padx=(5,5), anchor='n')

    def hideTestDetails(self):
        text = self.view.entrycget(2, 'label')
        if text == 'Hide test details':
            self.view.entryconfigure(2, label='Show test details')
        else:
            self.view.entryconfigure(2, label='Hide test details')
        testContainer = app.testDetailModule
        envContainer = app.envDetailModule
        projectContainer = app.projectDetailModule
        
        if testContainer.winfo_manager():
            testContainer.pack_forget()
        else:
            projectContainer.pack_forget()
            envContainer.pack_forget()
            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, padx=(5,5), anchor='n')
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, padx=(5,5), anchor='n')
            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, padx=(5,5), anchor='n')

    def hideEnvDetails(self):
        text = self.view.entrycget(3, 'label')
        if text == 'Hide environment details':
            self.view.entryconfigure(3, label='Show environment details')
        else:
            self.view.entryconfigure(3, label='Hide environment details')
        testContainer = app.testDetailModule
        envContainer = app.envDetailModule
        projectContainer = app.projectDetailModule
        
        if envContainer.winfo_manager():
            envContainer.pack_forget()
        else:
            projectContainer.pack_forget()
            testContainer.pack_forget()
            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, padx=(5,5), anchor='n')
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, padx=(5,5), anchor='n')
            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, padx=(5,5), anchor='n')