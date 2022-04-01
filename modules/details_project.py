from tkinter import *
from tkinter import ttk
from objects.app import app

class ProjectDetailsModule(ttk.Frame):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Frame.__init__(self, detailsPanel, *args, **kwargs)
        
        if app.settings.visDefaults['projectDetails']:
            self.pack(side = LEFT, fill=BOTH)

        self.configure(borderwidth=5)

        self.container = ttk.Labelframe(self, text="Project details", borderwidth=5)
        self.container.pack(fill=BOTH, expand=True)

        self.subjectCount = ttk.Label(self.container, text=None)
        self.subjectCount.pack(expand=False)

        # VO2 details
        self.VO2max = ttk.Label(self.container, text=None)
        self.VO2min = ttk.Label(self.container, text=None)
        self.VO2mean = ttk.Label(self.container, text=None)

        # QaO2 details
        self.QaO2max = ttk.Label(self.container, text=None)
        self.QaO2min = ttk.Label(self.container, text=None)
        self.QaO2mean = ttk.Label(self.container, text=None)

        # DO2 details
        self.DO2max = ttk.Label(self.container, text=None)
        self.DO2min = ttk.Label(self.container, text=None)
        self.DO2mean = ttk.Label(self.container, text=None)

        self.calculateButton = ttk.Button(self.container, text="Calculate", command=lambda: app.getMaxMinAvg(plotProject=True))

    def refreshDetails(self):
        self.VO2max.pack(expand=False)
        self.VO2min.pack(expand=False)
        self.VO2mean.pack(expand=False)
        self.QaO2max.pack(expand=False)
        self.QaO2min.pack(expand=False)
        self.QaO2mean.pack(expand=False)
        self.DO2max.pack(expand=False)
        self.DO2min.pack(expand=False)
        self.DO2mean.pack(expand=False)
        # Show buttons
        try:
            self.calculateButton.pack_info()
        except:
            self.calculateButton.pack(side=BOTTOM)
        
        activeProject = app.getActiveProject()
        self.subjectCount.config(text=f'Subjects: {len(activeProject.subjects)}')
        # VO2
        self.VO2max.config(text=f'VO\u2082\u2098\u2090\u2093 peak: {"{0:.1f}".format(float(activeProject.VO2max))}')
        self.VO2min.config(text=f'VO\u2082\u2098\u2090\u2093 min: {"{0:.1f}".format(float(activeProject.VO2min))}')
        self.VO2mean.config(text=f'VO\u2082\u2098\u2090\u2093 mean: {"{0:.1f}".format(float(activeProject.VO2mean))}')
        # QaO2
        self.QaO2max.config(text=f'QaO\u2082 peak: {"{0:.1f}".format(float(activeProject.QaO2max))}')
        self.QaO2min.config(text=f'QaO\u2082 min: {"{0:.1f}".format(float(activeProject.QaO2min))}')
        self.QaO2mean.config(text=f'QaO\u2082 mean: {"{0:.1f}".format(float(activeProject.QaO2mean))}')
        # DO2
        self.DO2max.config(text=f'DO\u2082 peak: {"{0:.1f}".format(float(activeProject.DO2max))}')
        self.DO2min.config(text=f'DO\u2082 min: {"{0:.1f}".format(float(activeProject.DO2min))}')
        self.DO2mean.config(text=f'DO\u2082 mean: {"{0:.1f}".format(float(activeProject.DO2mean))}')