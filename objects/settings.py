import pickle
from tkinter import *
from tkinter import ttk
from objects.app import app

class Settings(object):
    def __init__(self):  
        self.vars = []
        self.notifications = []
        try:
            settingsFile = open('settings.pkl', "rb")
            self.data = pickle.load(settingsFile)
            settingsFile.close()
            self.processData()
        except:
            defData = {
                "layout": {
                    'sideMenu': True,
                    'allDetails': True,
                    'projectDetails': True,
                    'testDetails': True,
                    'envDetails': False,
                },
                "envDefaults": {
                    "Elevation": 1000,
                    "Atm": 101,
                    "FiO2": 21,
                    "Temp": 20,
                    "Rh": 40
                },
                "testDefaults":{
                    "loadMode": 0,
                    "T @ rest": 37,
                    "T": 37,
                    "pH @ rest": 7.4,
                    "pH": 7.4
                },
                "unitDefaults":{
                    "Load": 'W',
                    "Velocity": 'km/h',
                    "Incline": "\N{DEGREE SIGN}",
                    "VO2": 'ml/min',
                    "HR": 'bpm',
                    "SV": 'ml',
                    "Q": 'l/min',
                    "[Hb]": 'g/l',
                    "SaO2": '%',
                    "CaO2": 'ml/l',
                    "SvO2": '%',
                    "CvO2": 'ml/l',
                    "C(a-v)O2": 'ml/l',
                    "QaO2": 'ml/min',
                    "T": '\N{DEGREE SIGN}C',
                    "T @ rest": '\N{DEGREE SIGN}C',
                    "pH @ rest": '',
                    "pH": '',
                    "PvO2": 'mmHg',
                    "DO2": 'ml/min/mmHg',
                    "Elevation": 'm',
                    "ATM": 'kPa',
                    "FiO2": '%',
                    "Temperature": '\N{DEGREE SIGN}C',
                    "Rh": "%"
                },
                "units": {
                    "Load": ['W', 'kJ'],
                    "Velocity": ['km/h', 'm/s', 'mph'],
                    "Incline": ["\N{DEGREE SIGN}", "%"],
                    "VO2": ['ml/min', 'l/min'],
                    "HR": ["bpm"],
                    "SV": ['ml', 'l'],
                    "Q": ['l/min', 'ml/min'],
                    "[Hb]": ["g/l", "g/dl"],
                    "SaO2": ["%"],
                    "CaO2": ["ml/l", "ml/dl"],
                    "SvO2": ["%"],
                    "CvO2": ["ml/l", "ml/dl"],
                    "C(a-v)O2": ["ml/l", "ml/dl"],
                    "QaO2": ["ml/min", "l/min"],
                    "T": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "T @ rest": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "pH": [""],
                    "pH @ rest": [""],
                    "PvO2": ["mmHg"],
                    "DO2": ["ml/min/mmHg"],
                    "Elevation": ['m', 'km', 'ft'],
                    "ATM": ['kPa', 'bar', 'psi', 'mmHg'],
                    "FiO2": ["%"],
                    "Temperature": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "Rh": ["%"]
                },
                "mcDefaults":{
                    "VO2": 0,
                    "HR": 0,
                    "SV": 0,
                    "Q": 0,
                    "[Hb]": 0,
                    "SaO2": 0,
                    "CaO2": 0,
                    "SvO2": 0,
                    "CvO2": 0,
                    "C(a-v)O2": 0,
                    "QaO2": 0,
                    "T": 0,
                    "T @ rest": 0,
                    "pH": 0,
                    "pH @ rest": 0,
                    "PvO2": 0,
                    "DO2": 1
                },
                "decimals":{
                    'l/min': 2,
                    'ml/min': 2,
                    'ml/l':  2,
                    'ml/dl': 2,
                    'ml/min/mmHg': 1,
                    'g/l': 1,
                    'g/dl': 1,
                    'mmHg': 2,
                    '\N{DEGREE SIGN}C': 1,
                    'K': 1,
                    'F': 1,
                    'ml': 0,
                    'bpm': 0,
                    '%': 0,
                    'm': 0,
                    'km': 1,
                    'ft': 0,
                    'kPa': 1,
                    'bar': 1,
                    'psi': 0,
                    'W': 0,
                    'kJ': 0,
                    'km/h': 1,
                    'm/s': 1,
                    'mph': 1
                }
            }

            settingsFile = open('settings.pkl', 'wb')
            pickle.dump(defData, settingsFile)
            settingsFile.close()

            settingsFile = open('settings.pkl', "rb")
            self.data = pickle.load(settingsFile)
            settingsFile.close()
            self.processData()

    def processData(self):
        self.visDefaults = {
            'sideMenu': self.data['layout']['sideMenu'],
            'allDetails': self.data['layout']['allDetails'],
            'projectDetails': self.data['layout']['projectDetails'],
            'testDetails': self.data['layout']['testDetails'],
            'envDetails': self.data['layout']['envDetails']
        }

        self.envDefaults = {
            'Elevation': self.data['envDefaults']['Elevation'],
            'Atm': self.data['envDefaults']['Atm'],
            'FiO2': self.data['envDefaults']['FiO2'],
            'Temp': self.data['envDefaults']['Temp'],
            'Rh': self.data['envDefaults']['Rh']
        }

        self.testDefaults = {
            "loadMode": self.data['testDefaults']['loadMode'],
            "T @ rest": self.data['testDefaults']['T @ rest'],
            "T": self.data['testDefaults']['T'],
            "pH @ rest": self.data['testDefaults']['pH @ rest'],
            "pH": self.data['testDefaults']['pH']
        }

        self.unitDefaults = {
            "Load_unit": self.data['unitDefaults']['Load'],
            "Velocity_unit": self.data['unitDefaults']['Velocity'],
            "Incline_unit": self.data['unitDefaults']['Incline'],
            "VO2_unit": self.data['unitDefaults']['VO2'],
            "HR_unit": self.data['unitDefaults']['HR'],
            "SV_unit": self.data['unitDefaults']['SV'],
            "Q_unit": self.data['unitDefaults']['Q'],
            "[Hb]_unit": self.data['unitDefaults']['[Hb]'],
            "SaO2_unit": self.data['unitDefaults']['SaO2'],
            "CaO2_unit": self.data['unitDefaults']['CaO2'],
            "SvO2_unit": self.data['unitDefaults']['SvO2'],
            "CvO2_unit": self.data['unitDefaults']['CvO2'],
            "C(a-v)O2_unit": self.data['unitDefaults']['C(a-v)O2'],
            "QaO2_unit": self.data['unitDefaults']['QaO2'],
            "T_unit": self.data['unitDefaults']['T'],
            "T @ rest_unit": self.data['unitDefaults']['T @ rest'],
            "pH_unit": '',
            "pH @ rest_unit": self.data['unitDefaults']['pH @ rest'],
            "PvO2_unit": self.data['unitDefaults']['PvO2'],
            "DO2_unit": self.data['unitDefaults']['DO2'],
            "Elevation_unit": self.data['unitDefaults']['Elevation'],
            "ATM_unit": self.data['unitDefaults']['ATM'],
            "FiO2_unit": self.data['unitDefaults']['FiO2'],
            "Temperature_unit": self.data['unitDefaults']['Temperature']
        }

        self.units = {
            "Load_units": self.data['units']['Load'],
            "Velocity_units": self.data['units']['Velocity'],
            "Incline_units": self.data['units']['Incline'],
            "VO2_units": self.data['units']['VO2'],
            "HR_units": self.data['units']['HR'],
            "SV_units": self.data['units']['SV'],
            "Q_units": self.data['units']['Q'],
            "[Hb]_units": self.data['units']['[Hb]'],
            "SaO2_units": self.data['units']['SaO2'],
            "CaO2_units": self.data['units']['CaO2'],
            "SvO2_units": self.data['units']['SvO2'],
            "CvO2_units": self.data['units']['CvO2'],
            "C(a-v)O2_units": self.data['units']['C(a-v)O2'],
            "QaO2_units": self.data['units']['QaO2'],
            "T_units": self.data['units']['T'],
            "T @ rest_units": self.data['units']['T @ rest'],
            "pH_units": '',
            "pH @ rest_units": self.data['units']['pH @ rest'],
            "PvO2_units": self.data['units']['PvO2'],
            "DO2_units": self.data['units']['DO2'],
            "Elevation_units": self.data['units']['Elevation'],
            "ATM_units": self.data['units']['ATM'],
            "FiO2_units": self.data['units']['FiO2'],
            "Temperature_units": self.data['units']['Temperature'],
            "Rh_units": '%'
        }

        self.mcDefaults = {
            "VO2_mc": self.data['mcDefaults']['VO2'],
            "HR_mc": self.data['mcDefaults']['HR'],
            "SV_mc": self.data['mcDefaults']['SV'],
            "Q_mc": self.data['mcDefaults']['Q'],
            "[Hb]_mc": self.data['mcDefaults']['[Hb]'],
            "SaO2_mc": self.data['mcDefaults']['SaO2'],
            "CaO2_mc": self.data['mcDefaults']['CaO2'],
            "SvO2_mc": self.data['mcDefaults']['SvO2'],
            "CvO2_mc": self.data['mcDefaults']['CvO2'],
            "C(a-v)O2_mc": self.data['mcDefaults']['C(a-v)O2'],
            "QaO2_mc": self.data['mcDefaults']['QaO2'],
            "T @ rest_mc": self.data['mcDefaults']['T @ rest'],
            "T_mc": self.data['mcDefaults']['T'],
            "pH @ rest_mc": self.data['mcDefaults']['pH @ rest'],
            "pH_mc": self.data['mcDefaults']['pH'],
            "PvO2_mc": self.data['mcDefaults']['PvO2'],
            "DO2_mc": self.data['mcDefaults']['DO2']
        }

        self.decimals = {
            'l/min': self.data['decimals']['l/min'],
            'ml/min': self.data['decimals']['ml/min'],
            'ml/l':  self.data['decimals']['ml/l'],
            'ml/dl': self.data['decimals']['ml/dl'],
            'ml/min/mmHg': self.data['decimals']['ml/min/mmHg'],
            'g/l': self.data['decimals']['g/l'],
            'g/dl': self.data['decimals']['g/dl'],
            'mmHg': self.data['decimals']['mmHg'],
            '\N{DEGREE SIGN}C': self.data['decimals']['\N{DEGREE SIGN}C'],
            'K': self.data['decimals']['K'],
            'F': self.data['decimals']['F'],
            'ml': self.data['decimals']['ml'],
            'bpm': self.data['decimals']['bpm'],
            '%': self.data['decimals']['%'],
            'm': self.data['decimals']['m'],
            'km': self.data['decimals']['km'],
            'ft': self.data['decimals']['ft'],
            'kPa': self.data['decimals']['kPa'],
            'bar': self.data['decimals']['bar'],
            'psi': self.data['decimals']['psi'],
            'W': self.data['decimals']['W'],
            'kJ': self.data['decimals']['kJ'],
            'km/h': self.data['decimals']['km/h'],
            'm/s': self.data['decimals']['m/s'],
            'mph': self.data['decimals']['mph']
        }

    def getUnitDef(self):
        return self.unitDefaults

    def getUnits(self):
        return self.units

    def getEnvDef(self):
        return self.envDefaults

    def getTestDef(self):
        return self.testDefaults

    def getMcDef(self):
        return self.mcDefaults

    def getDecimals(self):
        return self.decimals

    def saveLayout(self, side, details, project, test, env):
        self.data['layout']['sideMenu'] = side
        self.data['layout']['allDetails'] = details
        self.data['layout']['projectDetails'] = project
        self.data['layout']['testDetails'] = test
        self.data['layout']['envDetails'] = env

        settingsFile = open('settings.pkl', 'wb')
        pickle.dump(self.data, settingsFile)
        settingsFile.close()

    def openSettings(self):
        self.settingsWindow = Toplevel(width=500, height=500)
        self.settingsWindow.title("Settings")
        self.settingsWindow.pack_propagate(False)
        self.settingsWindow.update_idletasks()
        self.settingsWindow.tk.call('wm', 'iconphoto', self.settingsWindow._w, PhotoImage(file='Img/ho2pt.png'))

        initX = int(app.root.winfo_screenwidth()) * 0.5 - int(self.settingsWindow.winfo_width()) * 0.5
        initY = int(app.root.winfo_screenheight()) * 0.5 - int(self.settingsWindow.winfo_height()) * 0.5
        self.settingsWindow.geometry("+%d+%d" % ( initX, initY ))
        
        self.sideMenu = Listbox(self.settingsWindow, exportselection=FALSE, width=20)
        self.sideMenu.pack(side=LEFT, fill=Y)
        self.sideMenu.pack_propagate(False)
        self.sideMenu.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        self.sideMenu.insert('end', 'Test')
        self.sideMenu.insert('end', 'Environmental')

        self.rightContainer = ttk.Frame(self.settingsWindow)
        self.notification = ttk.Frame(self.rightContainer, height=20)
        if app.platform == 'linux':
            self.canvas = Canvas(self.rightContainer, bg='#EFEBE7')
        else:
            self.canvas = Canvas(self.rightContainer)
        self.scrollbar = ttk.Scrollbar(self.rightContainer, orient=VERTICAL, command=self.canvas.yview)
        self.contentWrapper = ttk.Frame(self.canvas)
        self.footer = ttk.Frame(self.rightContainer)

        self.contentWrapper.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.contentWrapper, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.mouseWheelBindId = app.root.bind_all('<MouseWheel>', self.handleMouseWheel)

        # Top part
        rightContainerTop = ttk.Frame(self.contentWrapper)
        rightContainerTop.pack()

        self.settingsContainer = ttk.Frame(rightContainerTop)
        self.settingsContainer.pack(side=LEFT, fill=BOTH, expand=TRUE)

        ttk.Button(self.footer, text='Cancel', command=lambda: self.cancel()).pack(side=RIGHT, padx=(5,20))
        ttk.Button( self.footer, text='Save', command=lambda: self.saveSettings( self.sideMenu.curselection()[0] ) ).pack(side=RIGHT)
        
        # Set initial selections
        self.sideMenu.selection_set(0)
        self.handleListboxSelect(0)

        # Pack every widget
        self.rightContainer.pack(side=RIGHT, fill=BOTH, expand=True)
        self.notification.pack(side=TOP, fill=X)
        self.footer.pack(side=BOTTOM, fill=X)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.settingsWindow.protocol("WM_DELETE_WINDOW", self.cancel)

        self.settingsWindow.mainloop()

    def cancel(self):
        app.root.unbind('<MouseWheel>', self.mouseWheelBindId)
        self.notifications = []
        self.settingsWindow.destroy()

    def handleMouseWheel(self, e):
        if self.settingsContainer.winfo_reqheight() > self.rightContainer.winfo_reqheight():
            self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    def handleListboxSelect(self, index=None):
        index = self.sideMenu.curselection()[0]

        for child in self.settingsContainer.winfo_children():
            child.destroy()

        if index == 0: # Test

            # Select loads or velocity/incline
            selectionFrame = ttk.Labelframe(self.settingsContainer, text='Use', padding=(5,5))
            selectionFrame.pack(fill=X, pady=(5,5), padx=(5,5), anchor='nw')
            ttk.Label(selectionFrame, text='Load').grid(column=1, row=0, sticky='w')
            ttk.Label(selectionFrame, text='Velocity / Incline').grid(column=1, row=1, sticky='w')
            self.selVar = IntVar(value=self.testDefaults['loadMode'])
            ttk.Radiobutton(selectionFrame, variable=self.selVar, value=0).grid(column=0, row=0)
            ttk.Radiobutton(selectionFrame, variable=self.selVar, value=1).grid(column=0, row=1)

            # Select default values/units
            labelFrame = ttk.Labelframe(self.settingsContainer, text='Value & Unit defaults')
            labelFrame.pack(fill=X, pady=(5,5), padx=(5,5), anchor='nw')
            container = ttk.Frame(labelFrame)
            container.grid()

            self.entries = {}
            self.menuButtons = {}
            self.mcs = {}

            #### Headers
            ttk.Label(container, text='Value').grid(column=1, row=0)
            ttk.Label(container, text='Unit').grid(column=2, row=0)
            ttk.Label(container, text='Meas.').grid(column=3, row=0)
            ttk.Label(container, text='Calc.').grid(column=4, row=0)

            vars = [
                'Load', 
                'Velocity',
                'Incline',
                'VO2',
                'HR',
                'SV',
                'Q',
                '[Hb]',
                'SaO2',
                'CaO2',
                'SvO2',
                'CvO2',
                'C(a-v)O2',
                'QaO2',
                'T @ rest',
                'T',
                'pH @ rest',
                'pH',
                'PvO2'
            ]

            for i, v in enumerate(vars):
                if v == 'T @ rest' or v == 'T' or v == 'pH @ rest' or v == 'pH':
                    SettingsRow(self, container, v, 1, i+1)
                else:
                    SettingsRow(self, container, v, 0, i+1)

        elif index == 1: # Environmental
            labelFrame = ttk.Labelframe(self.settingsContainer, text='Environmental defaults', padding=(5,5))
            labelFrame.pack(fill=BOTH, expand=1, pady=(5,5), padx=(5,5))
            container = ttk.Frame(labelFrame)
            container.grid()
            self.menuButtons = {}

            #### Elevation
            ttk.Label(container, text='Elevation').grid(column=0, row=0)
            self.elevEntry = ttk.Entry(container, width=7)
            self.elevEntry.insert(0, self.envDefaults['Elevation'])
            self.elevEntry.grid(column=1, row=0)

            # Elevation unit
            units = self.units['Elevation_units']
            elevMenuButton = ttk.Menubutton(container)
            self.menuButtons['Elevation'] = elevMenuButton
            elevMenuButton.config(text=self.unitDefaults['Elevation_unit'])

            if app.platform == 'linux':
                elevMenu = Menu(elevMenuButton, tearoff=False, background='#EFEBE7')
            else:
                elevMenu = Menu(elevMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(elevMenu, elevMenuButton, u, i, units)
            elevMenuButton['menu']=elevMenu
            elevMenuButton.grid(column=2, row=0)

            #### Atmosphere pressure
            ttk.Label(container, text='ATM').grid(column=0, row=1)
            self.atmEntry = ttk.Entry(container, width=7)
            self.atmEntry.insert(0, self.envDefaults['Atm'])
            self.atmEntry.grid(column=1, row=1)

            # Atmosphere pressure unit
            units = self.units['ATM_units']
            atmMenuButton = ttk.Menubutton(container)
            self.menuButtons['ATM'] = atmMenuButton
            atmMenuButton.config(text=self.unitDefaults['ATM_unit'])

            if app.platform == 'linux':
                atmMenu = Menu(atmMenuButton, tearoff=False, background='#EFEBE7')
            else:
                atmMenu = Menu(atmMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(atmMenu, atmMenuButton, u, i, units)
            atmMenuButton['menu']=atmMenu
            atmMenuButton.grid(column=2, row=1)

            # FiO2
            ttk.Label(container, text='FiO\u2082').grid(column=0, row=2)
            self.fio2Entry = ttk.Entry(container, width=7)
            self.fio2Entry.insert(0, self.envDefaults['FiO2'])
            self.fio2Entry.grid(column=1, row=2)
            ttk.Label(container, text='%').grid(column=2, row=2)

            #### Temperature
            ttk.Label(container, text='Temperature').grid(column=0, row=3)
            self.tempEntry = ttk.Entry(container, width=7)
            self.tempEntry.insert(0, self.envDefaults['Temp'])
            self.tempEntry.grid(column=1, row=3)

            # Temperature unit
            units = self.units['Temperature_units']
            tempMenuButton = ttk.Menubutton(container)
            self.menuButtons['Temperature'] = tempMenuButton
            tempMenuButton.config(text=self.unitDefaults['Temperature_unit'])

            if app.platform == 'linux':
                tempMenu = Menu(tempMenuButton, tearoff=False, background='#EFEBE7')
            else:
                tempMenu = Menu(tempMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(tempMenu, tempMenuButton, u, i, units)
            tempMenuButton['menu']=tempMenu
            tempMenuButton.grid(column=2, row=3)

            #### %RH
            ttk.Label(container, text='%RH').grid(column=0, row=4)
            self.rhEntry = ttk.Entry(container, width=7)
            self.rhEntry.insert(0, self.envDefaults['Rh'])
            self.rhEntry.grid(column=1, row=4)
            ttk.Label(container, text='%').grid(column=2, row=4)

    def saveSettings(self, option):
        
        if option == 0: # Test
            for key, val in self.entries.items():
                self.testDefaults[key] = val.get()
                self.data['testDefaults'][key] = val.get()
                
            for key, val in self.menuButtons.items():
                self.unitDefaults[key+'_unit'] = val.cget('text')
                self.data['unitDefaults'][key] = val.cget('text')

            for key, val in self.mcs.items():
                self.mcDefaults[key] = val.get()
                self.data['mcDefaults'][key] = val.get()

            # Save selection of loads/velocity & incline
            self.testDefaults['loadMode'] = self.selVar.get()
            self.data['testDefaults']['loadMode'] = self.selVar.get()
                
            ## Update change to every project
            projects = app.getProjects()
            if len(projects) > 0:
                for p in projects:
                    subjects = p.getSubjects()
                    for s in subjects:
                        tests = s.getTests()
                        for t in tests:
                            loads = t.getWorkLoads()
                            for l in loads:
                                for key, val in self.unitDefaults.items():
                                    l.getDetails().setUnit(key, val)
                                # if l.details.isImported == False:
                                    for key, val in self.testDefaults.items():
                                        l.getDetails().setValue(key, val)
                            if loads[0].details.isImported == False:
                                self.updatePhAndTemp(t)

        elif option == 1: # Environmental
            # Values
            self.envDefaults['Elevation'] = self.elevEntry.get()
            self.envDefaults['Atm'] = self.atmEntry.get()
            self.envDefaults['FiO2'] = self.fio2Entry.get()
            self.envDefaults['Temp'] = self.tempEntry.get()
            self.envDefaults['Rh'] = self.rhEntry.get()

            # Units
            for key, val in self.menuButtons.items():
                self.unitDefaults[key+'_unit'] = val.cget('text')

                # Save changes to settings.pkl-file
                self.data['unitDefaults'][key] = val.cget('text')

            # Save changes to settings.pkl-file
            self.data['envDefaults']['Elevation'] = self.elevEntry.get()
            self.data['envDefaults']['Atm'] = self.atmEntry.get()
            self.data['envDefaults']['FiO2'] = self.fio2Entry.get()
            self.data['envDefaults']['Temp'] = self.tempEntry.get()
            self.data['envDefaults']['Rh'] = self.rhEntry.get()

            ## Update change to every project
            projects = app.getProjects()
            if len(projects) > 0:
                for p in projects:
                    subjects = p.getSubjects()
                    for s in subjects:
                        tests = s.getTests()
                        for t in tests:
                            for l in t.workLoads:
                                if l.details.isImported == False:
                                    for key, val in self.unitDefaults.items():
                                        l.envDetails.setDetail(key, val)
                                    for key, val in self.envDefaults.items():
                                        l.envDetails.setDetail(key, val)
                            

        settingsFile = open('settings.pkl', 'wb')
        pickle.dump(self.data, settingsFile)
        settingsFile.close()

        # If there is an active test visible in the details panel
        # refresh its details as well, as it is in some cases a
        # deepcopy of the original test or constructed by the user
        if app.activeTest != None:
            for l in app.activeTest.workLoads:
                for key, val in self.unitDefaults.items():
                    l.getDetails().setUnit(key, val)
                    l.envDetails.setDetail(key, val)
                for key, val in self.testDefaults.items():
                    l.getDetails().setValue(key, val)
                for key, val in self.envDefaults.items():
                    l.envDetails.setDetail(key, val)
            self.updatePhAndTemp(app.activeTest)

            app.testDetailModule.refreshTestDetails()
            app.envDetailModule.refresh()
            
        app.projectDetailModule.refreshDetails()
        self.createNotification('info', 'Settings saved', 2000)

    def updatePhAndTemp(self, test):
        # Add linear change in pH and T
        pHrest = float(app.settings.testDefaults['pH @ rest'])
        Trest = float(app.settings.testDefaults['T @ rest'])
        pHpeak = float(app.settings.testDefaults['pH'])
        Tpeak = float(app.settings.testDefaults['T'])
        # pHDif = float(pHrest) - float(pHpeak)
        # Tdif = float(Tpeak) - float(Trest)

        for l in test.workLoads:
            l.details.setValue('pH', f'{"{0:.2f}".format(pHpeak)}')
            l.details.setValue('pH @ rest', f'{"{0:.2f}".format(pHrest)}')

            decimals = self.decimals[test.workLoads[0].details.getWorkLoadDetails()['T_unit']]
            l.details.setValue('T', f'{"{0:.{decimals}f}".format(Tpeak, decimals=decimals)}')
            l.details.setValue('T @ rest', f'{"{0:.{decimals}f}".format(Trest, decimals=decimals)}')

        """ # Filter possible empty loads
        nFilteredLoads = 0
        filteredLoads = []

        for i, l in enumerate(test.workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
                        
            if l.details.isImported:
                if i == 0 or detailsDict['Load'] != 0:
                    nFilteredLoads += 1
                    filteredLoads.append(l)
            else:
                nFilteredLoads += 1
                filteredLoads.append(l)

        if nFilteredLoads > 1:
            if pHrest != pHpeak:
                test.getWorkLoads()[-1].getDetails().setValue('pH', pHpeak)

            if Trest != Tpeak:
                test.getWorkLoads()[-1].getDetails().setValue('T', Tpeak)

            pHstep = pHDif / (nFilteredLoads-1)
            Tstep = Tdif / (nFilteredLoads-1)
        else:
            pHstep = 0
            Tstep = 0

        if len(filteredLoads) > 1:
            # Add linear change
            for i, w in enumerate(filteredLoads):
                details = w.getDetails()
                pHValue = pHrest - (i * pHstep)
                details.setValue('pH', f'{"{0:.2f}".format(pHValue)}')

                Tvalue = Trest + (i * Tstep)
                decimals = self.decimals[test.workLoads[0].details.getWorkLoadDetails()['T_unit']]
                details.setValue('T', f'{"{0:.{decimals}f}".format(Tvalue, decimals=decimals)}')
        else:
            details = filteredLoads[0].getDetails()
            details.setValue('pH', f'{"{0:.2f}".format(pHpeak)}')
            details.setValue('pH @ rest', f'{"{0:.2f}".format(pHrest)}')

            decimals = self.decimals[test.workLoads[0].details.getWorkLoadDetails()['T_unit']]
            details.setValue('T', f'{"{0:.{decimals}f}".format(Tpeak, decimals=decimals)}')
            details.setValue('T @ rest', f'{"{0:.{decimals}f}".format(Trest, decimals=decimals)}') """
        
    def createNotification(self, type, text, timeout):
        def destroy():
            self.notif.destroy()
            self.notifications = []

        if len(self.notifications) > 0:
            pass
        else:
            style = ttk.Style()
            style.configure('settings.TLabel')
            
            if type == 'info':
                style.configure('settings.TLabel', background="green", foreground="white", anchor="CENTER")
            if type == 'error':
                style.configure('settings.TLabel', background="red", foreground="white", anchor="CENTER")

            self.notif = ttk.Label(self.notification, style='settings.TLabel', text=text, font='Arial 12')
            self.notif.pack(fill=X)
            self.notifications.append(self.notif)
            self.notif.after(timeout, destroy)

class MenuElem(object):
    def __init__(self, menu, menuButton, label, index, elems):
        self.menu = menu
        self.menuButton = menuButton
        self.label = label
        self.index = index
        self.elems = elems

        self.menu.add_command(label=self.label, command=lambda: self.testi())

    def testi(self):
        self.menuButton.config(text=self.elems[self.index])

class SettingsRow(object):
    def __init__(self, settings, parent, label, entryFlag, row):

        # Menubutton
        if '2' in label:
            label_subscripted = label.replace('2', '\u2082')
            ttk.Label(parent, text=label_subscripted).grid(column=0, row=row)
        else:
            ttk.Label(parent, text=label).grid(column=0, row=row)

        # Entry
        if entryFlag == 1:
            tempEntry = ttk.Entry(parent, width=7)
            settings.entries[label] = tempEntry
            tempEntry.insert(0, settings.testDefaults[label])
            tempEntry.grid(column=1, row=row)

        # Unit
        try:
            self.menuButton = ttk.Menubutton(parent)
            settings.menuButtons[label] = self.menuButton
            self.menuButton.config(text=settings.unitDefaults[f'{label}_unit'])

            if len(settings.units[f"{label}_units"]) != 1:
                if app.platform == 'linux':
                    menu = Menu(self.menuButton, tearoff=False, background='#EFEBE7')
                else:
                    menu = Menu(self.menuButton, tearoff=False)
                units = settings.units[f"{label}_units"]
                if units != None and label != 'pH' and label != 'pH @ rest':
                    for i, u in enumerate(units):
                        MenuElem(menu, self.menuButton, u, i, units)
                    self.menuButton['menu']=menu
                    self.menuButton.grid(column=2, row=row)
            else:
                ttk.Label(parent, text=settings.units[f"{label}_units"][0]).grid(column=2, row=row)
        except KeyError:
            pass

        # Measured/Calculated
        try:
            self.intVar = IntVar(value=settings.mcDefaults[f'{label}_mc'])
            self.radio1 = ttk.Radiobutton(parent, value=0, variable=self.intVar)
            self.radio1.grid(column=3, row=row)

            self.radio2 = ttk.Radiobutton(parent, value=1, variable=self.intVar)
            self.radio2.grid(column=4, row=row)
            settings.mcs[f'{label}_mc'] = self.intVar
        except KeyError:
            pass