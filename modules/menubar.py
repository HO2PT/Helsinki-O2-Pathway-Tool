import os
from tkinter import *
from objects.app import app
from tkinter.filedialog import asksaveasfile
import pandas as pd
from modules.notification import notification

def createMenu(root):
    menuBar = Menu(root)

    # Adding File Menu and commands
    file = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='File', menu = file)

    importFile = Menu(menuBar, tearoff = 0)
    importFile.add_command(label ='Project...', command = lambda: None)
    importFile.add_command(label ='Subject...', command = lambda: None)
    importFile.add_command(label ='Test...', command = lambda: None)

    file.add_cascade(label ='Import', menu = importFile)
    file.add_command(label='Export...', command=lambda: exportData())
    file.add_separator()
    file.add_command(label ='Exit', command = root.destroy)

    # Settings
    settings = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='Settings', menu = settings)

    # Settings - mode
    modes = Menu(menuBar, tearoff = 0)
    settings.add_cascade(label ='Modes', menu = modes)
    # Get default usermode from settings
    var = IntVar(value=app.getActiveMode(), name='userMode')
    if var not in app.intVars:
        app.intVars.append(var)
    basic = modes.add_radiobutton(label ='Basic Mode', value=0, variable=var, command = lambda: setMode(var))
    advanced = modes.add_radiobutton(label ='Advanced Mode', value=1, variable=var, command = lambda: setMode(var))
    

    # Settings - default settings
    settings.add_command(label ='Settings...', command = lambda: app.settings.openSettings())
    
    # View
    view = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='View', menu = view)
    view.add_checkbutton(label ='Hide side menu', command = lambda: hideSidePanel())
    view.add_checkbutton(label ='Hide project details', command = lambda: hideProjectDetails())
    view.add_checkbutton(label ='Hide test details', command = lambda: hideTestDetails())
    view.add_checkbutton(label ='Hide environment details', command = lambda: hideEnvDetails())

    # Create demo graph
    menuBar.add_command(label ='Create demo graph', command=lambda: createDemoGraph())

    # About
    options = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='About', menu = options)
    options.add_command(label ='About O2 Pathway Tool', command = None)
    
    return menuBar

def exportData():
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

def setMode(var):
    app.setActiveMode(var.get())
    if var.get() == 0:
        showBasicLayout()
    else:
        showAdvLayout()

def createDemoGraph():
    print('Creating demograph')
    #app.plottingPanel.plot()

def hideSidePanel():
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

def hideProjectDetails():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container
    
    if projectContainer.winfo_manager():
        projectContainer.pack_forget()
    else:
        testContainer.pack_forget()
        envContainer.pack_forget()
        projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

def hideTestDetails():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container
    
    if testContainer.winfo_manager():
        testContainer.pack_forget()
    else:
        projectContainer.pack_forget()
        envContainer.pack_forget()
        projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

def hideEnvDetails():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container
    
    if envContainer.winfo_manager():
        envContainer.pack_forget()
    else:
        projectContainer.pack_forget()
        testContainer.pack_forget()
        projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
        envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

def showAdvLayout():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container

    projectContainer.pack_forget()
    testContainer.pack_forget()
    envContainer.pack_forget()

    projectContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
    testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)
    envContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)

def showBasicLayout():
    testContainer = app.testDetailModule.container
    envContainer = app.envDetailModule.frame
    projectContainer = app.projectDetailModule.container

    projectContainer.pack_forget()
    testContainer.pack_forget()
    envContainer.pack_forget()

    testContainer.pack(side = LEFT, fill = BOTH, expand=TRUE)