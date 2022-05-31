from tkinter import *
from tkinter import ttk
from objects.app import app

class ProjectDetailsModule(ttk.Labelframe):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Labelframe.__init__(self, detailsPanel, text="Project details", borderwidth=5, padding=(5,5))
        self.configure(cursor='arrow')
        
        if app.settings.visDefaults['projectDetails']:
            self.pack(side = LEFT, padx=(5,5), anchor='n')

        self.configure(borderwidth=5)

        self.subjectCount = ttk.Label(self, text=None)
        self.subjectCount.pack(expand=False)

        # VO2 details
        self.VO2max = ttk.Label(self, text=None)
        self.VO2min = ttk.Label(self, text=None)
        self.VO2mean = ttk.Label(self, text=None)

        self.sep1 = ttk.Separator(self)

        # QaO2 details
        self.QaO2max = ttk.Label(self, text=None)
        self.QaO2min = ttk.Label(self, text=None)
        self.QaO2mean = ttk.Label(self, text=None)

        self.sep2 = ttk.Separator(self)

        # DO2 details
        self.DO2max = ttk.Label(self, text=None)
        self.DO2min = ttk.Label(self, text=None)
        self.DO2mean = ttk.Label(self, text=None)

        self.calculateButton = ttk.Button(self, text="Calculate", command=lambda: app.getMaxMinAvg(plotProject=True))

    def refreshDetails(self):
        self.VO2max.pack(expand=False)
        self.VO2min.pack(expand=False)
        self.VO2mean.pack(expand=False)
        self.sep1.pack(fill=X, pady=5)
        self.QaO2max.pack(expand=False)
        self.QaO2min.pack(expand=False)
        self.QaO2mean.pack(expand=False)
        self.sep2.pack(fill=X, pady=5)
        self.DO2max.pack(expand=False)
        self.DO2min.pack(expand=False)
        self.DO2mean.pack(expand=False)
        # Show buttons
        try:
            self.calculateButton.pack_info()
        except:
            self.calculateButton.pack(side=BOTTOM)
        
        activeProject = app.getActiveProject()
        try:
            self.subjectCount.config(text=f'Subjects: {len(activeProject.subjects)}')
            # VO2
            self.VO2max.config(text=f'Peak VO\u2082 max: {"{0:.1f}".format(float(activeProject.VO2max))}')
            self.VO2min.config(text=f'Peak VO\u2082 min: {"{0:.1f}".format(float(activeProject.VO2min))}')
            self.VO2mean.config(text=f'Peak VO\u2082 mean: {"{0:.1f}".format(float(activeProject.VO2mean))}')
            # QaO2
            self.QaO2max.config(text=f'Peak QaO\u2082 max: {"{0:.1f}".format(float(activeProject.QaO2max))}')
            self.QaO2min.config(text=f'Peak QaO\u2082 min: {"{0:.1f}".format(float(activeProject.QaO2min))}')
            self.QaO2mean.config(text=f'Peak QaO\u2082 mean: {"{0:.1f}".format(float(activeProject.QaO2mean))}')
            # DO2
            self.DO2max.config(text=f'Peak DO\u2082 max: {"{0:.1f}".format(float(activeProject.DO2max))}')
            self.DO2min.config(text=f'Peak DO\u2082 min: {"{0:.1f}".format(float(activeProject.DO2min))}')
            self.DO2mean.config(text=f'Peak DO\u2082 mean: {"{0:.1f}".format(float(activeProject.DO2mean))}')
        except:
            self.subjectCount.config(text=f'Subjects: 0')
            # VO2
            self.VO2max.config(text=f'Peak VO\u2082 max: 0.0')
            self.VO2min.config(text=f'Peak VO\u2082 min: 0.0')
            self.VO2mean.config(text=f'Peak VO\u2082 mean: 0.0')
            # QaO2
            self.QaO2max.config(text=f'Peak QaO\u2082 max: 0.0')
            self.QaO2min.config(text=f'Peak QaO\u2082 min: 0.0')
            self.QaO2mean.config(text=f'Peak QaO\u2082 mean: 0.0')
            # DO2
            self.DO2max.config(text=f'Peak DO\u2082 max: 0.0')
            self.DO2min.config(text=f'Peak DO\u2082 min: 0.0')
            self.DO2mean.config(text=f'Peak DO\u2082 mean: 0.0')