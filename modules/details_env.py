from tkinter import *
from tkinter import ttk
from objects.app import app

class EnvDetailModule(ttk.Frame):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Frame.__init__(self, detailsPanel, *args, **kwargs)

        self.labels = []
        self.detailRows = []
        self.vars = ['Elevation', 'ATM', 'FiO2', 'Temp', 'Rh']

        if app.settings.visDefaults['envDetails']:
            self.pack(side = LEFT, fill = Y)
        
        self.configure(borderwidth=5)
        self.frame = ttk.Labelframe(self, text="Environment details", borderwidth=5)
        self.frame.pack(fill=Y, expand=True)

        self.dummy = ttk.Label(self.frame, text='')
        self.dummy.pack()

        self.container = ttk.Frame(self.frame, height=10)        

        self.elevLabel = ttk.Label(self.container, text='')
        self.elevDetail = envDetailRow(self.container, 'Elevation', 1, 0)
        self.labels.append(self.elevLabel)
        self.detailRows.append(self.elevDetail)

        self.atmLabel = ttk.Label(self.container, text='')
        self.atmDetail = envDetailRow(self.container, 'ATM', 1, 1)
        self.labels.append(self.atmLabel)
        self.detailRows.append(self.atmDetail)

        self.fio2Label = ttk.Label(self.container, text='')
        self.fio2Detail = envDetailRow(self.container, 'FiO2', 1, 2)
        self.labels.append(self.fio2Label)
        self.detailRows.append(self.fio2Detail)

        self.tempLabel = ttk.Label(self.container, text='')
        self.tempDetail = envDetailRow(self.container, 'Temperature', 1, 3)
        self.labels.append(self.tempLabel)
        self.detailRows.append(self.tempDetail)

        self.rhLabel = ttk.Label(self.container, text='')
        self.rhDetail = envDetailRow(self.container, 'Rh', 1, 4)
        self.labels.append(self.rhLabel)
        self.detailRows.append(self.rhDetail)

        self.calcMethod = ttk.Labelframe(self.container, text='')
        self.calcMetodRow = envDetailRow(self.calcMethod, 'PiO2Method', 1, 5)

    def refresh(self):
        self.dummy.destroy()
        self.container.grid()
        self.elevLabel.grid(column=0, row=0)
        self.atmLabel.grid(column=0, row=1)
        self.fio2Label.grid(column=0, row=2)
        self.tempLabel.grid(column=0, row=3)
        self.rhLabel.grid(column=0, row=4)
        self.calcMethod.grid(column=0, row=5, columnspan=3)

        self.envDetails = app.getActiveTest().getEnvDetails().getDetails()

        for i, v in enumerate(self.vars):
            self.detailRows[i].var.set(self.envDetails[v])
            self.detailRows[i].menuButton.config(text=self.envDetails[f'{v}_unit'])
            if v == 'FiO2':
                self.labels[i].configure(text='FiO\u2082')
            elif v == 'Rh':
                self.labels[i].configure(text=f'{v}%')
            else:
                self.labels[i].configure(text=v)

        # PiO2 calculation method
        self.calcMethod.configure(text='PiO\u2082 calculation method')
        self.calcMetodRow.var.set(self.envDetails['PiO2Method'])

class envDetailRow(object):
    def __init__(self, container, label, col, row):
        self.container = container
        self.label = label
        self.unitDefs = app.settings.getUnitDef()
        self.envUnits = app.settings.getUnits()
        self.menuButtons = {}

        self.var = StringVar()
        self.var.trace('w', self.updateVar)

        if label == 'PiO2Method':  
            self.radio1 = ttk.Radiobutton(self.container, text='U.S SA', value=0, variable=self.var)
            self.radio1.pack(anchor='w')

            self.radio2 = ttk.Radiobutton(self.container, text='MAE', value=1, variable=self.var)
            self.radio2.pack(anchor='w')
        else:
            # Value
            self.entry = ttk.Entry(self.container, width=7, textvariable=self.var)
            self.entry.grid(column=col, row=row)

            # Unit
            self.menuButton = ttk.Menubutton(self.container)
            self.menuButtons[label] = self.menuButton

            varMenu = Menu(self.menuButton, tearoff=False)
            units = self.envUnits[f'{label}_units']
            if len(units) > 1:
                for i, u in enumerate(units):
                    EnvMenuElem(varMenu, self.menuButton, u, i, units, f'{label}_unit')
                self.menuButton['menu']=varMenu
                self.menuButton.grid(column=col+1, row=row)
            else:
                ttk.Label(self.container, text='%').grid(column=col+1, row=row)

    def updateVar(self, name, index, mode):
        app.getActiveTest().getEnvDetails().setDetail(self.label, self.var.get())

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