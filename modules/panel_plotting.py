from tkinter import *
from tkinter import ttk

class PlottingPanel(object):
    def __init__(self, mainFrame):
        print("PlottingPanel instance created")

        #s = ttk.Style()
        #s.configure('plottingPanel.TFrame', background="blue")

        container = ttk.Frame(mainFrame)
        container.pack(fill=BOTH, expand=TRUE)

        # Plots notebook
        plotNotebook = ttk.Notebook(container)
        plotNotebook.pack(expand=TRUE, fill=BOTH)

        # Plot initial Tab
        tab0 = ttk.Frame(plotNotebook, width=300, height=200)
        tab0.pack(expand=TRUE)

        # Plot canvasframe
        canvasFrame = ttk.Frame(tab0)
        canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        # Loads notebook frame
        loadNotebookFrame = ttk.Frame(tab0)
        loadNotebookFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)
        
        # Load notebook
        loadNotebook = ttk.Notebook(loadNotebookFrame)
        loadNotebook.pack(expand=TRUE, fill=BOTH)
        # Initial Tab
        loadtab0 = ttk.Frame(loadNotebook)
        loadtab0.pack(expand=TRUE, fill=BOTH)
        loadNotebook.add(loadtab0, text='+')
        
        plotNotebook.add(tab0, text='+')