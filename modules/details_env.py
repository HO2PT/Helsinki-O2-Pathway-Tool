from tkinter import *
from tkinter import ttk
from objects.app import app

class EnvDetailModule(ttk.Frame):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Frame.__init__(self, detailsPanel, *args, **kwargs)

        self.frame = ttk.Labelframe(detailsPanel, text="Environment details", borderwidth=5)
        if app.settings.visDefaults['envDetails']:
            self.frame.pack(side = LEFT, fill = Y)
        
        self.configure(borderwidth=5)
        self.frame = ttk.Labelframe(self, text="Environment details", borderwidth=5)
        #print(self.frame.pack_info())

        self.create()

    def create(self):
        self.container = ttk.Frame(self.frame)
        self.container.grid()
        #print(self.container.grid_info())

        self.elevLabel = ttk.Label(self.container, text='')
        self.elevLabel.grid(column=0, row=0)

        self.atmLabel = ttk.Label(self.container, text='')
        self.atmLabel.grid(column=0, row=1)

        self.fio2Label = ttk.Label(self.container, text='')
        self.fio2Label.grid(column=0, row=2)

        self.tempLabel = ttk.Label(self.container, text='')
        self.tempLabel.grid(column=0, row=3)

        self.rhLabel = ttk.Label(self.container, text='')
        self.rhLabel.grid(column=0, row=4)

        self.calcMethod = ttk.LabelFrame(self.container, text='')
        self.calcMethod.grid(column=0, row=5, columnspan=2)

    def refresh(self):
        self.container.destroy()
        self.create()
        
        # Elevation
        self.elevLabel.configure(text='Elevation')
        envDetailRow(self.container, 'elevation')

        # Atmosphere pressure
        self.atmLabel.configure(text='ATM')
        envDetailRow(self.container, 'atm')

        # Fraction of inspired oxygen
        self.fio2Label.configure(text='FiO\u2082')
        envDetailRow(self.container, 'fio2')

        # Temperature
        self.tempLabel.configure(text='Temp')
        envDetailRow(self.container, 'temp')

        # %RH
        self.rhLabel.configure(text='RH%')
        envDetailRow(self.container, 'rh')

        # PiO2 calculation method
        self.calcMethod.config(text='PiO\u2082 calculation method')
        envDetailRow(self.calcMethod, 'pio2Method')

class envDetailRow(object):
    def __init__(self, container, label):
        self.container = container
        self.label = label
        id = app.getActiveTest().id
        self.envDetails = app.getActiveTest().getEnvDetails()
        self.unitDefs = app.settings.getUnitDef()
        self.envUnits = app.settings.getUnits()
        self.menuButtons = {}
        
        if label == 'elevation':
            # Value
            self.elevVar = StringVar(value=self.envDetails.elevation)#, name=f'{self.label}-{id}')
            self.elevVar.trace('w', self.updateElev)
            self.elevEntry = ttk.Entry(self.container, width=7, textvariable=self.elevVar)
            self.elevEntry.grid(column=1, row=0)

            # Unit
            elevMenuButton = ttk.Menubutton(self.container)
            self.menuButtons['Elevation'] = elevMenuButton
            elevMenuButton.config(text=self.unitDefs['Elevation_unit'])

            elevMenu = Menu(elevMenuButton, tearoff=False)
            units = self.envUnits['Elevation_units']
            for i, u in enumerate(units):
                EnvMenuElem(elevMenu, elevMenuButton, u, i, units, 'Elevation_unit')
            elevMenuButton['menu']=elevMenu
            elevMenuButton.grid(column=2, row=0)

        if label == 'atm':
            # Value
            self.atmVar = StringVar(value=self.envDetails.atm)#, name=f'{self.label}-{app.getActiveTest().id}')
            self.atmVar.trace('w', self.updateAtm)
            self.atmEntry = ttk.Entry(self.container, width=7, textvariable=self.atmVar)
            self.atmEntry.grid(column=1, row=1)

            # Unit
            atmMenuButton = ttk.Menubutton(container)
            self.menuButtons['ATM'] = atmMenuButton
            atmMenuButton.config(text=self.unitDefs['ATM_unit'])

            atmMenu = Menu(atmMenuButton, tearoff=False)
            units = self.envUnits['ATM_units']
            for i, u in enumerate(units):
                EnvMenuElem(atmMenu, atmMenuButton, u, i, units, 'ATM_unit')
            atmMenuButton['menu']=atmMenu
            atmMenuButton.grid(column=2, row=1)

        if label == 'fio2':
            # Value
            self.fio2Var = StringVar(value=self.envDetails.fio2)#, name=f'{self.label}-{app.getActiveTest().id}')
            self.fio2Var.trace('w', self.updateFio2)
            self.fio2Entry = ttk.Entry(self.container, width=7, textvariable=self.fio2Var)
            self.fio2Entry.grid(column=1, row=2)

            # Unit
            ttk.Label(self.container, text='%').grid(column=2, row=2)

        if label == 'temp':
            # Value
            self.tempVar = StringVar(value=self.envDetails.temp)#, name=f'{self.label}-{app.getActiveTest().id}')
            self.tempVar.trace('w', self.updateTemp)
            self.tempEntry = ttk.Entry(self.container, width=7, textvariable=self.tempVar)
            self.tempEntry.grid(column=1, row=3)

            # Unit            
            tempMenuButton = ttk.Menubutton(container)
            self.menuButtons['Temperature'] = tempMenuButton
            tempMenuButton.config(text=self.unitDefs['Temperature_unit'])

            tempMenu = Menu(tempMenuButton, tearoff=False)
            units = self.envUnits['Temperature_units']
            for i, u in enumerate(units):
                EnvMenuElem(tempMenu, tempMenuButton, u, i, units, 'Temperature_unit')
            tempMenuButton['menu']=tempMenu
            tempMenuButton.grid(column=2, row=3)
        
        if label == 'rh':
            # Value
            self.rhVar = StringVar(value=self.envDetails.rh)#, name=f'{self.label}-{app.getActiveTest().id}')
            self.rhVar.trace('w', self.updateRh)
            self.rhEntry = ttk.Entry(self.container, width=7, textvariable=self.rhVar)
            self.rhEntry.grid(column=1, row=4)

            # Unit
            ttk.Label(self.container, text='%').grid(column=2, row=4)

        if label == 'pio2Method':
            self.methodVar = IntVar(value=self.envDetails.pio2Method)#, name=f'{self.label}-{app.getActiveTest().id}') 
                    
            self.radio1 = ttk.Radiobutton(self.container, text='U.S SA', value=0, variable=self.methodVar)
            self.radio1.pack(anchor='w')

            self.radio2 = ttk.Radiobutton(self.container, text='MAE', value=1, variable=self.methodVar)
            self.radio2.pack(anchor='w')
            self.methodVar.trace('w', self.updatePio2Method)

    def updateElev(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.elevVar.get())

    def updateAtm(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.atmVar.get())

    def updateFio2(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.fio2Var.get())

    def updateTemp(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.tempVar.get())

    def updateRh(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.rhVar.get())
    
    def updatePio2Method(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, self.label, self.methodVar.get())


class EnvMenuElem(object):
    def __init__(self, menu, menuButton, unit, index, units, name=None):
        self.menu = menu
        self.menuButton = menuButton
        self.name = name
        self.index = index
        self.units = units

        self.menu.add_command(label=unit, command=lambda: self.updateValue())

    def updateValue(self):
        self.menuButton.config(text=self.units[self.index])
        app.getActiveTest().getEnvDetails().setDetail(self.name, self.units[self.index])