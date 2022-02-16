from tabnanny import process_tokens
from tkinter import *
from objects.app import app
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
    file.add_separator()
    file.add_command(label ='Exit', command = root.destroy)

    # Settings
    settings = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='Settings', menu = settings)

    # Settings - mode
    modes = Menu(menuBar, tearoff = 0)
    settings.add_cascade(label ='Modes', menu = modes)
    modes.add_command(label ='Basic Mode', command = lambda: None)
    modes.add_command(label ='Advanced Mode', command = lambda: None)

    # Settings - default settings
    settings.add_command(label ='Settings...', command = lambda: app.settings.openSettings())
    
    # View
    view = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='View', menu = view)
    view.add_checkbutton(label ='Hide side menu', command = lambda: hideSidePanel())
    view.add_checkbutton(label ='Hide project details', command = lambda: hideProject())
    view.add_checkbutton(label ='Hide test details', command = lambda: hideTest())
    view.add_checkbutton(label ='Hide environment details', command = lambda: hideEnvDetails())

    # Create demo graph
    menuBar.add_command(label ='Create demo graph', command=lambda: createDemoGraph())

    # About
    options = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='About', menu = options)
    options.add_command(label ='About O2 Pathway Tool', command = None)

    return menuBar

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

def hideProject():
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

def hideTest():
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