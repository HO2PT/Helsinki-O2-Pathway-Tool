import pickle
from tkinter import *
from tkinter import ttk
from objects.app import app

class Settings(object):

    def __init__(self):  
        self.vars = [] 
        try:
            settingsFile = open('settings.pkl', "rb")
            self.data = pickle.load(settingsFile)
            settingsFile.close()
            self.processData()
        except:
            #print('SETTINGS NOT FOUND')
            defData = {
                # "userMode": 0,
                "layout": {
                    'sideMenu': True,
                    'allDetails': True,
                    'projectDetails': True,
                    'testDetails': True,
                    'envDetails': False,
                },
                "envDefaults": {
                    "elevation": 1000,
                    "atm": 101,
                    "fio2": 21,
                    "temp": 20,
                    "rh": 40
                },
                "testDefaults":{
                    "Tc @ rest": 37,
                    "Tc\u209A\u2091\u2090\u2096": 37,
                    "pH @ rest": 7.4,
                    "pH\u209A\u2091\u2090\u2096": 7.4
                },
                "unitDefaults":{
                    "Load": 'W',
                    "VO2": 'ml/min',
                    "HR": 'bpm',
                    "Sv": 'ml',
                    "Q": 'l/min',
                    "Hb": 'g/l',
                    "SaO2": '%',
                    "CaO2": 'ml/l',
                    "SvO2": '%',
                    "CvO2": 'ml/l',
                    "CavO2": 'ml/l',
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
                    "VO2": ['ml/min', 'l/min'],
                    "HR": ["bpm"],
                    "Sv": ['ml', 'l'],
                    "Q": ['l/min', 'ml/min'],
                    "Hb": ["g/l", "g/dl"],
                    "SaO2": ["%"],
                    "CaO2": ["ml/l", "ml/dl"],
                    "SvO2": ["%"],
                    "CvO2": ["ml/l", "ml/dl"],
                    "CavO2": ["ml/l", "ml/dl"],
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
                    "Sv": 0,
                    "Q": 0,
                    "Hb": 0,
                    "SaO2": 0,
                    "CaO2": 0,
                    "SvO2": 0,
                    "CvO2": 0,
                    "CavO2": 0,
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

        # app.activeMode = self.data['userMode']
        #print(f'SETTINGS LOADED')

    def processData(self):
        # self.userMode = self.data['userMode']

        self.visDefaults = {
            'sideMenu': self.data['layout']['sideMenu'],
            'allDetails': self.data['layout']['allDetails'],
            'projectDetails': self.data['layout']['projectDetails'],
            'testDetails': self.data['layout']['testDetails'],
            'envDetails': self.data['layout']['envDetails']
        }

        self.envDefaults = {
            'elevation': self.data['envDefaults']['elevation'],
            'atm': self.data['envDefaults']['atm'],
            'fio2': self.data['envDefaults']['fio2'],
            'temp': self.data['envDefaults']['temp'],
            'rh': self.data['envDefaults']['rh']
        }

        self.testDefaults = {
            "Tc @ rest": self.data['testDefaults']['Tc @ rest'],
            "Tc\u209A\u2091\u2090\u2096": self.data['testDefaults']['Tc\u209A\u2091\u2090\u2096'],
            "pH @ rest": self.data['testDefaults']['pH @ rest'],
            "pH\u209A\u2091\u2090\u2096": self.data['testDefaults']['pH\u209A\u2091\u2090\u2096']
        }

        self.unitDefaults = {
            "Load_unit": self.data['unitDefaults']['Load'],
            "VO2_unit": self.data['unitDefaults']['VO2'],
            "HR_unit": self.data['unitDefaults']['HR'],
            "Sv_unit": self.data['unitDefaults']['Sv'],
            "Q_unit": self.data['unitDefaults']['Q'],
            "Hb_unit": self.data['unitDefaults']['Hb'],
            "SaO2_unit": self.data['unitDefaults']['SaO2'],
            "CaO2_unit": self.data['unitDefaults']['CaO2'],
            "SvO2_unit": self.data['unitDefaults']['SvO2'],
            "CvO2_unit": self.data['unitDefaults']['CvO2'],
            "CavO2_unit": self.data['unitDefaults']['CavO2'],
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
            "VO2_units": self.data['units']['VO2'],
            "HR_units": self.data['units']['HR'],
            "Sv_units": self.data['units']['Sv'],
            "Q_units": self.data['units']['Q'],
            "Hb_units": self.data['units']['Hb'],
            "SaO2_units": self.data['units']['SaO2'],
            "CaO2_units": self.data['units']['CaO2'],
            "SvO2_units": self.data['units']['SvO2'],
            "CvO2_units": self.data['units']['CvO2'],
            "CavO2_units": self.data['units']['CavO2'],
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
            "Temperature_units": self.data['units']['Temperature']
        }

        self.mcDefaults = {
            "VO2_mc": self.data['mcDefaults']['VO2'],
            "HR_mc": self.data['mcDefaults']['HR'],
            "Sv_mc": self.data['mcDefaults']['Sv'],
            "Q_mc": self.data['mcDefaults']['Q'],
            "Hb_mc": self.data['mcDefaults']['Hb'],
            "SaO2_mc": self.data['mcDefaults']['SaO2'],
            "CaO2_mc": self.data['mcDefaults']['CaO2'],
            "SvO2_mc": self.data['mcDefaults']['SvO2'],
            "CvO2_mc": self.data['mcDefaults']['CvO2'],
            "CavO2_mc": self.data['mcDefaults']['CavO2'],
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
        settingsWindow = Toplevel()
        settingsWindow.title("Settings")
        settingsWindow.geometry("500x500")

        settingsX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/1.5)
        settingsY = app.root.winfo_rooty() + (app.root.winfo_reqheight()*0.1)
        settingsWindow.geometry("+%d+%d" % ( settingsX, settingsY ))
        
        self.sideMenu = Listbox(settingsWindow, exportselection=FALSE, width=20)
        self.sideMenu.pack(side=LEFT, fill=Y)
        self.sideMenu.pack_propagate(False)
        self.sideMenu.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        # self.sideMenu.insert('end', 'General')
        self.sideMenu.insert('end', 'Test')
        self.sideMenu.insert('end', 'Environmental')

        rightContainer = ttk.Frame(settingsWindow)
        rightContainer.pack(fill=BOTH, expand=1)

        self.notification = ttk.Frame(rightContainer, height=25)
        self.notification.pack(fill=X)
        
        self.settingsContainer = ttk.Frame(rightContainer)
        self.settingsContainer.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.sideMenu.selection_set(0)
        self.handleListboxSelect(0)

        settingsWindow.mainloop()

    def handleListboxSelect(self, index=None):
        index = self.sideMenu.curselection()[0]

        for child in self.settingsContainer.winfo_children():
            child.destroy()

        # app.intVars = []

        # if index == 0:
        #     labelFrame = LabelFrame(self.settingsContainer, text='General defaults')
        #     labelFrame.grid()
        #     container = ttk.Frame(labelFrame)
        #     container.grid()

        #     UserMode(self, container)
        if index == 1: # Environmental
            labelFrame = LabelFrame(self.settingsContainer, text='Environmental defaults')
            labelFrame.pack(fill=BOTH, expand=1, pady=(5,5), padx=(5,5))
            container = ttk.Frame(labelFrame)
            container.grid()
            self.menuButtons = {}

            #### Elevation
            ttk.Label(container, text='Elevation').grid(column=0, row=0)
            elevEntry = ttk.Entry(container, width=7)
            elevEntry.insert(0, self.envDefaults['elevation'])
            elevEntry.grid(column=1, row=0)

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
            atmEntry = ttk.Entry(container, width=7)
            atmEntry.insert(0, self.envDefaults['atm'])
            atmEntry.grid(column=1, row=1)

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
            fio2Entry = ttk.Entry(container, width=7)
            fio2Entry.insert(0, self.envDefaults['fio2'])
            fio2Entry.grid(column=1, row=2)
            ttk.Label(container, text='%').grid(column=2, row=2)

            #### Temperature
            ttk.Label(container, text='Temperature').grid(column=0, row=3)
            tempEntry = ttk.Entry(container, width=7)
            tempEntry.insert(0, self.envDefaults['temp'])
            tempEntry.grid(column=1, row=3)

            # Temperature unit
            units = self.units['Temperature_units']
            tempMenuButton = ttk.Menubutton(container)
            self.menuButtons['Temperature'] = tempMenuButton
            tempMenuButton.config(text=self.unitDefaults['Temperature_unit'])

            #### RH%
            ttk.Label(container, text='RH%').grid(column=0, row=4)
            rhEntry = ttk.Entry(container, width=7)
            rhEntry.insert(0, self.envDefaults['rh'])
            rhEntry.grid(column=1, row=4)
            ttk.Label(container, text='%').grid(column=2, row=4)

            tempMenu = Menu(tempMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(tempMenu, tempMenuButton, u, i, units)
            tempMenuButton['menu']=tempMenu
            tempMenuButton.grid(column=2, row=5)

            ttk.Button(container, text='Save', command=lambda: saveSettings()).grid(column=2, row=5, sticky='E')

            def saveSettings():
                # Values
                self.envDefaults['elevation'] = elevEntry.get()
                self.envDefaults['atm'] = atmEntry.get()
                self.envDefaults['fio2'] = fio2Entry.get()
                self.envDefaults['temp'] = tempEntry.get()
                self.envDefaults['rh'] = rhEntry.get()

                # Units
                for key, val in self.menuButtons.items():
                    self.unitDefaults[key+'_unit'] = val.cget('text')

                    # Save changes to settings.pkl-file
                    self.data['unitDefaults'][key] = val.cget('text')

                # Save changes to settings.pkl-file
                self.data['envDefaults']['elevation'] = elevEntry.get()
                self.data['envDefaults']['atm'] = atmEntry.get()
                self.data['envDefaults']['fio2'] = fio2Entry.get()
                self.data['envDefaults']['temp'] = tempEntry.get()
                self.data['envDefaults']['rh'] = rhEntry.get()

                settingsFile = open('settings.pkl', 'wb')
                pickle.dump(self.data, settingsFile)
                settingsFile.close()

                self.createNotification('info', 'Settings saved', 5000)
                
        elif index == 0: # Test
            labelFrame = LabelFrame(self.settingsContainer, text='Test defaults')
            labelFrame.pack(fill=BOTH, expand=1, pady=(5,5), padx=(5,5))
            # labelFrame.grid_columnconfigure(0, weight=1)
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

            #### Load
            ttk.Label(container, text='Load').grid(column=0, row=1)
            units = self.units['Load_units']
            loadMenuButton = ttk.Menubutton(container)
            self.menuButtons['Load'] = loadMenuButton
            loadMenuButton.config(text=self.unitDefaults['Load_unit'])

            loadMenu = Menu(loadMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(loadMenu, loadMenuButton, u, i, units)
            loadMenuButton['menu']=loadMenu
            loadMenuButton.grid(column=2, row=1)

            #### VO2
            SettingsRow(self, container, 'VO2', 0, 2)

            #### HR
            SettingsRow(self, container, 'HR', 0, 3)

            #### SV
            SettingsRow(self, container, 'Sv', 0, 4)

            #### Q
            SettingsRow(self, container, 'Q', 0, 5)

            #### Hb
            SettingsRow(self, container, 'Hb', 0, 6)

            #### SaO2
            SettingsRow(self, container, 'SaO2', 0, 7)

            #### CaO2
            SettingsRow(self, container, 'CaO2', 0, 8)

            #### SvO2
            SettingsRow(self, container, 'SvO2', 0, 9)

            #### CvO2
            SettingsRow(self, container, 'CvO2', 0, 10)

            #### CavO2
            SettingsRow(self, container, 'CavO2', 0, 11)

            #### QaO2
            SettingsRow(self, container, 'QaO2', 0, 12)

            #### Tc @ rest
            SettingsRow(self, container, 'Tc @ rest', 1, 13)

            #### Tc\u209A\u2091\u2090\u2096
            SettingsRow(self, container, 'Tc\u209A\u2091\u2090\u2096', 1, 14)

            # pH @ rest
            SettingsRow(self, container, 'pH @ rest', 1, 15)

            # pH\u209A\u2091\u2090\u2096
            SettingsRow(self, container, 'pH\u209A\u2091\u2090\u2096', 1, 16)

            #### PvO2
            SettingsRow(self, container, 'PvO2', 0, 17)

            ttk.Button(container, text='Save', command=lambda: saveSettings()).grid(column=4, row=18, sticky='E')

            def saveSettings():
                for key, val in self.entries.items():
                    self.testDefaults[key] = val.get()
                    self.data['testDefaults'][key] = val.get()
                
                for key, val in self.menuButtons.items():
                    self.unitDefaults[key+'_unit'] = val.cget('text')
                    self.data['unitDefaults'][key] = val.cget('text')

                for key, val in self.mcs.items():
                    self.mcDefaults[key] = val.get()
                    self.data['mcDefaults'][key] = val.get()

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
                    app.testDetailModule.refreshTestDetails()

                settingsFile = open('settings.pkl', 'wb')
                pickle.dump(self.data, settingsFile)
                settingsFile.close()

                self.createNotification('info', 'Settings saved', 5000)

    def createNotification(self, type, text, timeout):
        style = ttk.Style()
        
        if type == 'info':
            style.configure('settings.TLabel', background="green", foreground="white", anchor="CENTER")
        if type == 'error':
            style.configure('settings.TLabel', background="red", foreground="white", anchor="CENTER")

        notif = ttk.Label(self.notification, style='settings.TLabel', text=text)
        notif.pack(fill=X)
        notif.after(timeout, lambda: notif.destroy())

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
        self.menuButton = ttk.Menubutton(parent)
        settings.menuButtons[label] = self.menuButton
        self.menuButton.config(text=settings.unitDefaults[f'{label}_unit'])

        # Entry
        if entryFlag == 1:
            tempEntry = ttk.Entry(parent, width=7)
            settings.entries[label] = tempEntry
            tempEntry.insert(0, settings.testDefaults[label])
            tempEntry.grid(column=1, row=row)

         # Unit
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

        # Measured/Calculated
        self.intVar = IntVar(value=settings.mcDefaults[f'{label}_mc'], name=f'{label}_mc')
        if self.intVar not in app.intVars:
            app.intVars.append(self.intVar)
        self.radio1 = ttk.Radiobutton(parent, value=0, variable=self.intVar)
        self.radio1.grid(column=3, row=row)

        self.radio2 = ttk.Radiobutton(parent, value=1, variable=self.intVar)
        self.radio2.grid(column=4, row=row)
        settings.mcs[f'{label}_mc'] = self.intVar

""" class UserMode(object):
    def __init__(self, settings, parent):
        # Measured/Calculated
        ttk.Label(parent, text='User mode').grid(column=0, row=0)
        self.intVar = IntVar(value=settings.userMode, name=f'userMode')
        if self.intVar not in app.intVars:
            app.intVars.append(self.intVar)

        self.radio1 = ttk.Radiobutton(parent, value=0, variable=self.intVar, text='Basic mode')
        self.radio1.grid(column=1, row=1, sticky='W')

        self.radio2 = ttk.Radiobutton(parent, value=1, variable=self.intVar, text='Advanced mode')
        self.radio2.grid(column=1, row=2, sticky='W')
    
        ttk.Button(parent, text='Save', command=lambda: self.saveSettings(settings)).grid(column=1, row=3, sticky='E')

    def saveSettings(self, settings):
        # Apply change to layout
        if self.intVar.get() == 0: # Basic
            app.menu.showBasicLayout()
        else: # Advanced
            app.menu.showAdvLayout()

        settings.userMode = self.intVar.get()
        settings.data['userMode'] = self.intVar.get()

        settingsFile = open('settings.pkl', 'wb')
        pickle.dump(settings.data, settingsFile)
        settingsFile.close()

        if self.intVar.get() == 0:
            settings.createNotification('info', f'Usermode set to Basic', 5000)
        else:
            settings.createNotification('info', f'Usermode set to Advanced', 5000) """