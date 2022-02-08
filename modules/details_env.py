from tkinter import *
from tkinter import ttk
from modules.notification import notification

class EnvDetailModule(object):
    def __init__(self, detailsPanel):
        container = ttk.Labelframe(detailsPanel, text="Environment details")
        container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        ttk.Button(container, text="Calculate", command=lambda: notification.create('info', 'Toimii', 3000)).pack(side=BOTTOM)