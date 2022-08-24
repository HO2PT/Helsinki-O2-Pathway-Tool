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
                    "Tc @ rest": 37,
                    "Tc\u209A\u2091\u2090\u2096": 37,
                    "pH @ rest": 7.4,
                    "pH\u209A\u2091\u2090\u2096": 7.4
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
                    "Tc @ rest": '\N{DEGREE SIGN}C',
                    "Tc\u209A\u2091\u2090\u2096": '\N{DEGREE SIGN}C',
                    "pH @ rest": '',
                    "pH\u209A\u2091\u2090\u2096": '',
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
                    "Tc @ rest": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "Tc\u209A\u2091\u2090\u2096": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "pH": [""],
                    "pH @ rest": [""],
                    "pH\u209A\u2091\u2090\u2096": [""],
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
                    "Tc @ rest": 0,
                    "Tc\u209A\u2091\u2090\u2096": 0,
                    "pH @ rest": 0,
                    "pH\u209A\u2091\u2090\u2096": 0,
                    "PvO2": 0,
                    "DO2": 1
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
            "Tc @ rest": self.data['testDefaults']['Tc @ rest'],
            "Tc\u209A\u2091\u2090\u2096": self.data['testDefaults']['Tc\u209A\u2091\u2090\u2096'],
            "pH @ rest": self.data['testDefaults']['pH @ rest'],
            "pH\u209A\u2091\u2090\u2096": self.data['testDefaults']['pH\u209A\u2091\u2090\u2096']
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
            "Tc @ rest_unit": self.data['unitDefaults']['Tc @ rest'],
            "Tc\u209A\u2091\u2090\u2096_unit": self.data['unitDefaults']['Tc\u209A\u2091\u2090\u2096'],
            "pH_unit": '',
            "pH @ rest_unit": self.data['unitDefaults']['pH @ rest'],
            "pH\u209A\u2091\u2090\u2096_unit": self.data['unitDefaults']['pH\u209A\u2091\u2090\u2096'],
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
            "Tc @ rest_units": self.data['units']['Tc @ rest'],
            "Tc\u209A\u2091\u2090\u2096_units": self.data['units']['Tc\u209A\u2091\u2090\u2096'],
            "pH_units": '',
            "pH @ rest_units": self.data['units']['pH @ rest'],
            "pH\u209A\u2091\u2090\u2096_units": self.data['units']['pH\u209A\u2091\u2090\u2096'],
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
            "Tc @ rest_mc": self.data['mcDefaults']['Tc @ rest'],
            "Tc\u209A\u2091\u2090\u2096_mc": self.data['mcDefaults']['Tc\u209A\u2091\u2090\u2096'],
            "pH @ rest_mc": self.data['mcDefaults']['pH @ rest'],
            "pH\u209A\u2091\u2090\u2096_mc": self.data['mcDefaults']['pH\u209A\u2091\u2090\u2096'],
            "PvO2_mc": self.data['mcDefaults']['PvO2'],
            "DO2_mc": self.data['mcDefaults']['DO2']
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
                'Tc @ rest',
                'Tc\u209A\u2091\u2090\u2096',
                'pH @ rest',
                'pH\u209A\u2091\u2090\u2096',
                'PvO2'
            ]

            for i, v in enumerate(vars):
                if v == 'Tc @ rest' or v == 'Tc\u209A\u2091\u2090\u2096' or v == 'pH @ rest' or v == 'pH\u209A\u2091\u2090\u2096':
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
                                for key, val in self.testDefaults.items():
                                    l.getDetails().setValue(key, val)
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
        self.createNotification('info', 'Settings saved', 2000)

    def updatePhAndTemp(self, test):
        # Add linear change in pH and T
        pHrest = float(app.settings.testDefaults['pH @ rest'])
        Trest = float(app.settings.testDefaults['Tc @ rest'])
        pHpeak = float(app.settings.testDefaults['pH\u209A\u2091\u2090\u2096'])
        Tpeak = float(app.settings.testDefaults['Tc\u209A\u2091\u2090\u2096'])
        pHDif = float(pHrest) - float(pHpeak)
        Tdif = float(Tpeak) - float(Trest)

        # Filter possible empty loads
        nFilteredLoads = 0
        filteredLoads = []
        for i, l in enumerate(test.workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
                        
            if i == 0 or detailsDict['Load'] != 0:
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

        # Add linear change
        for i, w in enumerate(filteredLoads):
            details = w.getDetails()
            pHValue = pHrest - (i * pHstep)
            details.setValue('pH', f'{"{0:.2f}".format(pHValue)}')

            Tvalue = Trest + (i * Tstep)
            details.setValue('T', f'{"{0:.1f}".format(Tvalue)}')
        
    def createNotification(self, type, text, timeout):
        def destroy():
            self.notif.destroy()
            self.notifications = []

        if len(self.notifications) > 0:
            pass
        else:
            style = ttk.Style()
            style.configure('settings.TLabel', font=('TkDefaultFont', 12))
            
            if type == 'info':
                style.configure('settings.TLabel', background="green", foreground="white", anchor="CENTER")
            if type == 'error':
                style.configure('settings.TLabel', background="red", foreground="white", anchor="CENTER")

            self.notif = ttk.Label(self.notification, style='settings.TLabel', text=text)
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
                menu = Menu(self.menuButton, tearoff=False)
                units = settings.units[f"{label}_units"]
                if units != None and label != 'pH\u209A\u2091\u2090\u2096' and label != 'pH @ rest':
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