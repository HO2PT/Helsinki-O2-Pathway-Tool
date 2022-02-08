from tkinter import *
from tkinter import ttk

class ProjectDetailsModule(object):
    def __init__(self, detailsPanel):
        container = ttk.Labelframe(detailsPanel, text="Project details")
        container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        ttk.Button(container, text="Calculate").pack(side=BOTTOM)
