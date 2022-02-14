from tkinter import *
from tkinter import ttk

class Plot(object):
    def _init__(self, plotNotebook, loadNotebook):
        self.plotNotebook = plotNotebook
        self.loadNotebook = loadNotebook

        # Plot initial Tab
        tab0 = ttk.Frame(plotNotebook, width=300, height=200)
        tab0.pack(expand=TRUE)

        # Initial Tab
        loadtab0 = ttk.Frame(loadNotebook)
        loadtab0.pack(expand=TRUE, fill=BOTH)
        loadNotebook.add(loadtab0, text='+')
        
        plotNotebook.add(tab0, text='+')