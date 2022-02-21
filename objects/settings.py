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
            print('SETTINGS NOT FOUND')
            defData = {
                "userMode": 0,
                "envDefaults": {
                    "elevation": 1000,
                    "atm": 101,
                    "fio2": 21,
                    "temp": 20
                },
                "testDefaults":{
                    "T": 37,
                    "pH": 7.4
                },
                "unitDefaults":{
                    "Load": ['W', 'kJ'],
                    "VO2": ['ml/min', 'l/min'],
                    "HR": ["bpm"],
                    "Sv": ['ml', 'l'],
                    "Q": ['l/min', 'ml/min'],
                    "Hb": ["g/l"],
                    "SaO2": ["%"],
                    "CaO2": ["ml/l"],
                    "SvO2": ["%"],
                    "CvO2": ["ml/l"],
                    "CavO2": ["ml/l"],
                    "QaO2": ["ml/min"],
                    "T": ['\N{DEGREE SIGN}C', 'F', 'K'],
                    "pH": [""],
                    "PvO2": ["mmHg"],
                    "DO2": ["ml/min/mmHg"],
                    "Elevation": ["m"],
                    "ATM": ["kPa"],
                    "FiO2": ["%"],
                    "Temperature": ["\N{DEGREE SIGN}C"]
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
                    "pH": 0,
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

        app.activeMode = self.data['userMode']
        print(f'SETTINGS LOADED')

    def processData(self):
        self.userMode = self.data['userMode']

        self.envDefaults = {
            'elevation': self.data['envDefaults']['elevation'],
            'atm': self.data['envDefaults']['atm'],
            'fio2': self.data['envDefaults']['fio2'],
            'temp': self.data['envDefaults']['temp']
        }

        self.testDefaults = {
            "T": self.data['testDefaults']['T'],
            "pH": self.data['testDefaults']['pH']
        }

        self.unitDefaults = {
            "Load_unit": self.data['unitDefaults']['Load'][0],
            "VO2_unit": self.data['unitDefaults']['VO2'][0],
            "HR_unit": self.data['unitDefaults']['HR'][0],
            "Sv_unit": self.data['unitDefaults']['Sv'][0],
            "Q_unit": self.data['unitDefaults']['Q'][0],
            "Hb_unit": self.data['unitDefaults']['Hb'][0],
            "SaO2_unit": self.data['unitDefaults']['SaO2'][0],
            "CaO2_unit": self.data['unitDefaults']['CaO2'][0],
            "SvO2_unit": self.data['unitDefaults']['SvO2'][0],
            "CvO2_unit": self.data['unitDefaults']['CvO2'][0],
            "CavO2_unit": self.data['unitDefaults']['CavO2'][0],
            "QaO2_unit": self.data['unitDefaults']['QaO2'][0],
            "T_unit": self.data['unitDefaults']['T'][0],
            "pH_unit": self.data['unitDefaults']['pH'][0],
            "PvO2_unit": self.data['unitDefaults']['PvO2'][0],
            "DO2_unit": self.data['unitDefaults']['DO2'][0],
            "Elevation_unit": self.data['unitDefaults']['Elevation'],
            "ATM_unit": self.data['unitDefaults']['ATM'],
            "FiO2_unit": self.data['unitDefaults']['FiO2'],
            "Temperature_unit": self.data['unitDefaults']['Temperature']
        }

        self.units = {
            "Load_units": self.data['unitDefaults']['Load'],
            "VO2_units": self.data['unitDefaults']['VO2'],
            "HR_units": self.data['unitDefaults']['HR'],
            "Sv_units": self.data['unitDefaults']['Sv'],
            "Q_units": self.data['unitDefaults']['Q'],
            "Hb_units": self.data['unitDefaults']['Hb'],
            "SaO2_units": self.data['unitDefaults']['SaO2'],
            "CaO2_units": self.data['unitDefaults']['CaO2'],
            "SvO2_units": self.data['unitDefaults']['SvO2'],
            "CvO2_units": self.data['unitDefaults']['CvO2'],
            "CavO2_units": self.data['unitDefaults']['CavO2'],
            "QaO2_units": self.data['unitDefaults']['QaO2'],
            "T_units": self.data['unitDefaults']['T'],
            "pH_units": self.data['unitDefaults']['pH'],
            "PvO2_units": self.data['unitDefaults']['PvO2'],
            "DO2_units": self.data['unitDefaults']['DO2'],
            "Elevation_units": self.data['unitDefaults']['Elevation'],
            "ATM_units": self.data['unitDefaults']['ATM'],
            "FiO2_units": self.data['unitDefaults']['FiO2'],
            "Temperature_units": self.data['unitDefaults']['Temperature']
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
            "T_mc": self.data['mcDefaults']['T'],
            "pH_mc": self.data['mcDefaults']['pH'],
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

    def openSettings(self):
        settingsWindow = Toplevel()
        settingsWindow.title("Settings")
        settingsWindow.geometry("500x500")

        settingsX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/1.5)
        settingsY = app.root.winfo_rooty() + (app.root.winfo_reqheight()*0.1)
        settingsWindow.geometry("+%d+%d" % ( settingsX, settingsY ))

        self.notification = ttk.Frame(settingsWindow, height=25)
        self.notification.pack(fill=X)
        
        self.sideMenu = Listbox(settingsWindow, exportselection=FALSE, width=5)
        self.sideMenu.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.sideMenu.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect() )

        self.sideMenu.insert('end', 'General')
        self.sideMenu.insert('end', 'Environmental')
        self.sideMenu.insert('end', 'Test')
        
        self.settingsContainer = ttk.Frame(settingsWindow)
        self.settingsContainer.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.sideMenu.selection_set(0)
        self.handleListboxSelect(0)

        settingsWindow.mainloop()

    def handleListboxSelect(self, index=None):
        index = self.sideMenu.curselection()[0]

        for child in self.settingsContainer.winfo_children():
            child.destroy()

        app.intVars = []

        if index == 0:
            labelFrame = LabelFrame(self.settingsContainer, text='General defaults')
            labelFrame.grid()
            container = ttk.Frame(labelFrame)
            container.grid()

            UserMode(self, container)
        elif index == 1: # Environmental
            labelFrame = LabelFrame(self.settingsContainer, text='Environmental defaults')
            labelFrame.grid()
            container = ttk.Frame(labelFrame)
            container.grid()
            self.menuButtons = {}

            #### Elevation
            ttk.Label(container, text='Elevation').grid(column=0, row=0)
            elevEntry = ttk.Entry(container, width=7)
            elevEntry.insert(0, self.envDefaults['elevation'])
            elevEntry.grid(column=1, row=0)

            # Elevation unit
            units = ('m', 'km', 'ft')
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
            units = ('kPa', 'bar', 'psi')
            atmMenuButton = ttk.Menubutton(container)
            self.menuButtons['ATM'] = atmMenuButton
            atmMenuButton.config(text=self.unitDefaults['ATM_unit'])

            atmMenu = Menu(atmMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(atmMenu, atmMenuButton, u, i, units)
            atmMenuButton['menu']=atmMenu
            atmMenuButton.grid(column=2, row=1)

            # FiO2
            ttk.Label(container, text='FiO2').grid(column=0, row=2)
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
            units = ('\N{DEGREE SIGN}C', 'F', 'K')
            tempMenuButton = ttk.Menubutton(container)
            self.menuButtons['Temperature'] = tempMenuButton
            tempMenuButton.config(text=self.unitDefaults['Temperature_unit'])

            tempMenu = Menu(tempMenuButton, tearoff=False)
            for i, u in enumerate(units):
                MenuElem(tempMenu, tempMenuButton, u, i, units)
            tempMenuButton['menu']=tempMenu
            tempMenuButton.grid(column=2, row=3)

            ttk.Button(container, text='Save', command=lambda: saveSettings()).grid(column=2, row=5, sticky='E')

            def saveSettings():
                self.envDefaults['elevation'] = elevEntry.get()
                self.envDefaults['atm'] = atmEntry.get()
                self.envDefaults['fio2'] = fio2Entry.get()
                self.envDefaults['temp'] = tempEntry.get()

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

                settingsFile = open('settings.pkl', 'wb')
                pickle.dump(self.data, settingsFile)
                settingsFile.close()

                self.createNotification('info', 'Settings saved', 5000)
                print('SAVING SETTINGS')
        elif index == 2: # Test
            labelFrame = LabelFrame(self.settingsContainer, text='Test defaults')
            labelFrame.grid()
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

            #### T
            SettingsRow(self, container, 'T', 1, 13)

            # pH
            SettingsRow(self, container, 'pH', 1, 14)

            #### PvO2
            SettingsRow(self, container, 'PvO2', 0, 15)

            ttk.Button(container, text='Save', command=lambda: saveSettings()).grid(column=4, row=16, sticky='E')

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
        menu = Menu(self.menuButton, tearoff=False)
        units = settings.units[f"{label}_units"]
        if units != None:
            for i, u in enumerate(units):
                MenuElem(menu, self.menuButton, u, i, units)
            self.menuButton['menu']=menu
            self.menuButton.grid(column=2, row=row)

        # Measured/Calculated
        self.intVar = IntVar(value=settings.mcDefaults[f'{label}_mc'], name=f'{label}_mc')
        if self.intVar not in app.intVars:
            app.intVars.append(self.intVar)
        self.radio1 = ttk.Radiobutton(parent, value=0, variable=self.intVar)
        self.radio1.grid(column=3, row=row)

        self.radio2 = ttk.Radiobutton(parent, value=1, variable=self.intVar)
        self.radio2.grid(column=4, row=row)
        settings.mcs[f'{label}_mc'] = self.intVar

class UserMode(object):
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
        settings.userMode = self.intVar.get()
        settings.data['userMode'] = self.intVar.get()

        settingsFile = open('settings.pkl', 'wb')
        pickle.dump(settings.data, settingsFile)
        settingsFile.close()

        if self.intVar.get() == 0:
            settings.createNotification('info', f'Usermode set to Basic', 5000)
        else:
            settings.createNotification('info', f'Usermode set to Advanced', 5000)