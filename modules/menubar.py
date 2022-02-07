from pydoc import importfile
from tkinter import *
from tkinter import ttk

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
    settings.add_command(label ='Settings...', command = lambda: None)
    
    # View
    view = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='View', menu = view)
    view.add_command(label ='Add/hide', command = lambda: None)

    # Create demo graph
    menuBar.add_command(label ='Create demo graph', command=lambda: None)

    # About
    options = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label ='About', menu = options)
    options.add_command(label ='About O2 Pathway Tool', command = None)

    return menuBar