from tkinter import *
from tkinter import ttk
from modules.notification import notification
from objects.app import app

class EnvDetailModule(object):
    def __init__(self, detailsPanel):
        self.frame = ttk.Labelframe(detailsPanel, text="Environment details")
        self.frame.pack(side = LEFT, fill = BOTH, expand=TRUE)

        self.create()

    def create(self):
        self.container = ttk.Frame(self.frame)
        self.container.grid()

        self.elevLabel = ttk.Label(self.container, text='')
        self.elevLabel.grid(column=0, row=0)

        self.atmLabel = ttk.Label(self.container, text='')
        self.atmLabel.grid(column=0, row=1)

        self.fio2Label = ttk.Label(self.container, text='')
        self.fio2Label.grid(column=0, row=2)

        self.tempLabel = ttk.Label(self.container, text='')
        self.tempLabel.grid(column=0, row=3)

        self.calcMethod = ttk.LabelFrame(self.container, text='')
        self.calcMethod.grid(column=0, row=4, columnspan=2)

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
        self.fio2Label.configure(text='FiO2')
        envDetailRow(self.container, 'fio2')

        # Temperature
        self.tempLabel.configure(text='Temp')
        envDetailRow(self.container, 'temp')

        # PiO2 calculation method
        self.calcMethod.config(text='PiO2 calculation method')
        envDetailRow(self.calcMethod, 'pio2Method')

        #ttk.Button(self.container, text="Calculate", command=lambda: notification.create('info', 'Toimii', 3000)).pack(side=BOTTOM)

class envDetailRow(object):
    def __init__(self, container, label):
        self.container = container
        self.label = label
        id = app.getActiveTest().id
        self.envDetails = app.getActiveTest().getEnvDetails()
        
        if label == 'elevation':
            self.elevVar = StringVar(value=self.envDetails.elevation, name=f'{self.label}-{id}')
            self.elevVar.trace('w', self.updateElev)
            if self.elevVar not in app.strVars:
                app.strVars.append(self.elevVar)
            self.elevEntry = ttk.Entry(self.container, width=7, textvariable=self.elevVar)
            #self.elevEntry.pack(side=LEFT)
            self.elevEntry.grid(column=1, row=0)

        if label == 'atm':
            self.atmVar = StringVar(value=self.envDetails.atm, name=f'{self.label}-{app.getActiveTest().id}')
            self.atmVar.trace('w', self.updateAtm)
            if self.atmVar not in app.strVars:
                app.strVars.append(self.atmVar)
            self.atmEntry = ttk.Entry(self.container, width=7, textvariable=self.atmVar)
            #self.atmEntry.pack(side=LEFT)
            self.atmEntry.grid(column=1, row=1)

        if label == 'fio2':
            self.fio2Var = StringVar(value=self.envDetails.fio2, name=f'{self.label}-{app.getActiveTest().id}')
            self.fio2Var.trace('w', self.updateFio2)
            if self.fio2Var not in app.strVars:
                app.strVars.append(self.fio2Var)
            self.fio2Entry = ttk.Entry(self.container, width=7, textvariable=self.fio2Var)
            #self.fio2Entry.pack(side=LEFT)
            self.fio2Entry.grid(column=1, row=2)

        if label == 'temp':
            self.tempVar = StringVar(value=self.envDetails.temp, name=f'{self.label}-{app.getActiveTest().id}')
            self.tempVar.trace('w', self.updateTemp)
            if self.tempVar not in app.strVars:
                app.strVars.append(self.tempVar)
            self.tempEntry = ttk.Entry(self.container, width=7, textvariable=self.tempVar)
            #self.tempEntry.pack(side=LEFT)
            self.tempEntry.grid(column=1, row=3)

        if label == 'pio2Method':
            self.methodVar = IntVar(value=self.envDetails.pio2Method, name=f'{self.label}-{app.getActiveTest().id}') 
            if self.methodVar not in app.strVars:
                app.strVars.append(self.methodVar)
                    
            self.radio1 = ttk.Radiobutton(self.container, text='U.S SA', value=0, variable=self.methodVar)
            self.radio1.pack(anchor='w')

            self.radio2 = ttk.Radiobutton(self.container, text='MAE', value=1, variable=self.methodVar)
            self.radio2.pack(anchor='w')
            self.methodVar.trace('w', self.updatePio2Method)

    def updateElev(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, name, self.elevVar.get())

    def updateAtm(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, name, self.atmVar.get())

    def updateFio2(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, name, self.fio2Var.get())

    def updateTemp(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, name, self.tempVar.get())
    
    def updatePio2Method(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.envDetails, name, self.methodVar.get())