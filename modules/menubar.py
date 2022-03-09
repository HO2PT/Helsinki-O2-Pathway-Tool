import os
from tkinter import *
from objects.app import app
from tkinter.filedialog import asksaveasfile
import pandas as pd
from modules.notification import notification
from objects.test import Test

class MenuBar(object):
    def __init__(self, root):
        self.menuBar = Menu(root)

        # Adding File Menu and commands
        file = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='File', menu = file)

        importFile = Menu(self.menuBar, tearoff = 0)
        importFile.add_command(label ='Project...', command = lambda: None)
        importFile.add_command(label ='Subject...', command = lambda: None)
        importFile.add_command(label ='Test...', command = lambda: None)

        file.add_cascade(label ='Import', menu = importFile)
        file.add_command(label='Export...', command=lambda: self.exportData())
        file.add_separator()
        file.add_command(label ='Exit', command = root.destroy)

        # Settings
        settings = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label ='Settings', menu = settings)

        # Settings - mode
        modes = Menu(self.menuBar, tearoff = 0)
        settings.add_cascade(label ='Modes', menu = modes)
        # Get default usermode from settings
        var = IntVar(value=app.getActiveMode(), name='userMode')
        if var not in app.intVars:
            app.intVars.append(var)
        basic = modes.add_radiobutton(label ='Basic Mode', value=0, variable=var, command = lambda: self.setMode(var))
        advanced = modes.add_radiobutton(label ='Advanced Mode', value=1, variable=var, command = lambda: self.setMode(var))
        

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
        self.menuBar.add_cascade(label ='About', menu = options)
        options.add_command(label ='About O2 Pathway Tool', command = None)

    def checkVisibility(self, object):
        if object == 'side':
            try:
                app.sidePanel.sidePanel.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'project':
            try:
                app.projectDetailModule.container.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'test':
            try:
                app.testDetailModule.container.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'environment':
            try:
                app.envDetailModule.frame.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'
        elif object == 'all':
            try:
                """ app.projectDetailModule.container.pack_info()
                app.testDetailModule.container.pack_info()
                app.envDetailModule.frame.pack_info() """
                app.detailsPanel.detailsPanel.pack_info()
                return 'Hide'
            except TclError:
                return 'Show'

    def getMenubar(self):
        return self.menuBar

    def exportData(self):
        print('exporting')
        data = []
        temp=[]
        imgs = []
        
        for i, p in enumerate(app.getPlottingPanel().plots):
            #print(f'PLOT: {p.plot}')
            #print(f'TEST: {p.activeTest}')
            #print(f'LOADS: {p.workLoads}')
            #print(f'DETAILS: {p.workLoads[0].getDetails().getWorkLoadDetails()}')
            details = p.workLoads[0].getDetails().getWorkLoadDetails()
            img = p.plot[0].savefig(f'plot{i}.png')
            imgs.append( img )
            
            #data = [['tom', 10], ['nick', 15], ['juli', 14], ['testi', img]]
            for d in p.workLoads:
                det = d.getDetails().getWorkLoadDetails()
                i = 0

                # Iterate through load details and print to Details module
                for key, value in det.items():
                    if i == 3:
                        label = temp[0][0]
                        val = temp[0][1]
                        unit = temp[1][1]
                        mc = temp[2][1]
                        data.append( [label, val, unit, mc] )
                        temp=[]
                        i = 0
                    
                    temp.append([key,value])
                    i = i + 1
        
        # Create the pandas DataFrame
        df = pd.DataFrame(data, columns = ['','Value', 'Unit', 'Meas(0)/Calc(1)'])
        #print(data)
        # Create excel
        saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
        fileName = saveFile.name.split('/')[-1]
        #print(f'FILENAME: {fileName}')
        writer = pd.ExcelWriter(f'{fileName}.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        asd = ['F1', 'K1', 'Q1']
        # Add plot images
        for i, im in enumerate(imgs):
            imgDest = f'{os.getcwd()}/plot{i}.png'
            worksheet.insert_image(asd[i], imgDest)
        
        writer.save()
        notification.create('info', 'Data successfully exported', 5000)

    def setMode(self, var):
        app.setActiveMode(var.get())
        if var.get() == 0:
            self.showBasicLayout()
        else:
            self.showAdvLayout()

    def createDemoGraph(self):
        print('Creating demograph')
        demoTest = Test()
        demoTest.workLoads[0].setDemoDetails()
        app.setActiveTest(demoTest)
        print( app.getActiveTest().getWorkLoads()[0].getDetails().getWorkLoadDetails() )
        app.plottingPanel.plot()

    def hideAllDetails(self):
        text = self.view.entrycget(4, 'label')
        print(self.view.entrycget(4, 'label'))
        if text == 'Hide all details':
            self.view.entryconfigure(4, label='Show all details')
        else:
            self.view.entryconfigure(4, label='Hide all details')
        detailsPanel = app.detailsPanel.detailsPanel
        notifPanel = notification.notifPanel
        plottingPanel = app.plottingPanel.container

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
        print(self.view.entrycget(0, 'label'))
        if text == 'Hide side menu':
            self.view.entryconfigure(0, label='Show side menu')
        else:
            self.view.entryconfigure(0, label='Hide side menu')
        
        sidePanel = app.sidePanel.sidePanel
        notifPanel = notification.notifPanel
        detailsPanel = app.detailsPanel.detailsPanel
        plottingPanel = app.plottingPanel.container

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
        print(self.view.entrycget(1, 'label'))
        if text == 'Hide project details':
            self.view.entryconfigure(1, label='Show project details')
        else:
            self.view.entryconfigure(1, label='Hide project details')
        testContainer = app.testDetailModule.container
        envContainer = app.envDetailModule.frame
        projectContainer = app.projectDetailModule.container
        
        if projectContainer.winfo_manager():
            projectContainer.pack_forget()
        else:
            testContainer.pack_forget()
            envContainer.pack_forget()

            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
            
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

    def hideTestDetails(self):
        text = self.view.entrycget(2, 'label')
        print(self.view.entrycget(2, 'label'))
        if text == 'Hide test details':
            self.view.entryconfigure(2, label='Show test details')
        else:
            self.view.entryconfigure(2, label='Hide test details')
        testContainer = app.testDetailModule.container
        envContainer = app.envDetailModule.frame
        projectContainer = app.projectDetailModule.container
        
        if testContainer.winfo_manager():
            testContainer.pack_forget()
        else:
            projectContainer.pack_forget()
            envContainer.pack_forget()
            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

    def hideEnvDetails(self):
        text = self.view.entrycget(3, 'label')
        print(self.view.entrycget(3, 'label'))
        if text == 'Hide environment details':
            self.view.entryconfigure(3, label='Show environment details')
        else:
            self.view.entryconfigure(3, label='Hide environment details')
        testContainer = app.testDetailModule.container
        envContainer = app.envDetailModule.frame
        projectContainer = app.projectDetailModule.container
        
        if envContainer.winfo_manager():
            envContainer.pack_forget()
        else:
            projectContainer.pack_forget()
            testContainer.pack_forget()
            text = self.view.entrycget(1, 'label')
            if text == 'Hide project details':
                projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
            text = self.view.entrycget(2, 'label')
            if text == 'Hide test details':
                testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
            text = self.view.entrycget(3, 'label')
            if text == 'Hide environment details':
                envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

    def showAdvLayout(self):
        testContainer = app.testDetailModule.container
        envContainer = app.envDetailModule.frame
        projectContainer = app.projectDetailModule.container

        projectContainer.pack_forget()
        testContainer.pack_forget()
        envContainer.pack_forget()

        self.view.entryconfigure(1, label='Hide project menu')
        projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        self.view.entryconfigure(2, label='Hide test menu')
        testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        self.view.entryconfigure(3, label='Hide environment menu')
        envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

    def showBasicLayout(self):
        testContainer = app.testDetailModule.container
        envContainer = app.envDetailModule.frame
        projectContainer = app.projectDetailModule.container

        self.view.entryconfigure(1, label='Show project menu')
        projectContainer.pack_forget()
        testContainer.pack_forget()
        self.view.entryconfigure(3, label='Show environment menu')
        envContainer.pack_forget()

        testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)