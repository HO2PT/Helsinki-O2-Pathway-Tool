from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.ScrollableNotebook import ScrollableNotebook

class TestDetailModule(object):    
    def __init__(self, detailsPanel):
        self.container = ttk.Labelframe(detailsPanel, text="Test details")
        self.container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        ## Details frame
        details = ttk.Frame(self.container)
        details.pack(side=LEFT, fill = Y)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        #ttk.Button(details, text="Calculate", command=lambda: app.getActiveTest().getMaxLoad()).pack(side=BOTTOM)

        ## Load notebook
        self.loadsContainer = ttk.Frame(self.container)
        self.loadsContainer.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.loadNotebook = LoadNotebook(self.loadsContainer)

    def addLoad(self):
        self.loadNotebook.addLoad()

    def refreshTestDetails(self):
        # Refresh details
        self.testId.config(text=f'Id: {app.getActiveTest().id}')
        self.loadNotebook.refresh()

class LoadNotebook(object):
    def __init__(self, parent):
        self.loadTabs = []

        # Add 'x'-button to tabs
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        style.configure('loadNotebook.TNotebook')
        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("loadNotebook.TNotebook", [
            ("loadNotebook.TNotebook.client", {
                "sticky": "nswe"
            })
        ])
        style.layout("loadNotebook.TNotebook.Tab", [
            ("loadNotebook.TNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("loadNotebook.TNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("loadNotebook.TNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("loadNotebook.TNotebook.label", {"side": "left", "sticky": ''}),
                                    ("loadNotebook.TNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
        
        ## Notebook
        self.loadbook = ScrollableNotebook(parent,style="loadNotebook.TNotebook", wheelscroll=True)

        # Add/edit button
        self.addButton = ttk.Button(parent, text='Add', command=lambda: self.addLoad())
        self.editButton = ttk.Button(parent, text='Edit', command=lambda: self.editLoad())

    def addLoad(self):
        # Add load to active test
        activeTest = app.getActiveTest()
        workLoadObject = activeTest.createLoad()
        i = len(self.loadTabs)
        details = workLoadObject.getDetails()

        newLoad = LoadTab(i, workLoadObject, details, self.loadbook)
            
        # Append tab
        self.loadTabs.append(newLoad)
        tabCount = self.loadbook.index('end')
        self.loadbook.add(newLoad.loadFrame, text=newLoad.getName())
        self.loadbook.select(tabCount) 

        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)

    def refresh(self):
        self.loadTabs = []
        # Hide previous tabs
        for t in self.loadbook.tabs():
            self.loadbook.forget(t)

        activeTest = app.getActiveTest()

        # Fetch list of load objects
        loads = activeTest.getWorkLoads()
        
        for i, l in enumerate(loads):
            # Get load details
            details = l.getDetails()

            newLoad = LoadTab(i, l, details, self.loadbook)
            
            # Append tab
            self.loadTabs.append(newLoad)
            tabCount = self.loadbook.index('end')
            self.loadbook.add(newLoad.loadFrame, text=l.getName())
            self.loadbook.select(tabCount)

        self.loadbook.pack(fill="both",expand=True)
        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)
            
    def editLoad(self):
        index = self.loadbook.index('current')

        # Create edit popup
        editscreen = Toplevel(width=self.editButton.winfo_reqwidth()*2.6, height=self.editButton.winfo_reqheight()*3)
        editscreen.title('Edit')
        editscreenX = self.editButton.winfo_rootx()-self.editButton.winfo_reqwidth()*1.45
        ediscreenY = self.editButton.winfo_rooty()-(self.editButton.winfo_reqheight()*4.5)
        editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
        editscreen.pack_propagate(False)
        
        ttk.Label(editscreen, text='Load name').pack()
        nameEntry = ttk.Entry(editscreen)
        nameEntry.pack(expand=TRUE)
        ttk.Button(editscreen, text='Save', command=lambda: edit()).pack(side=BOTTOM,anchor='e')

        def edit():
            load = app.getActiveTest().getWorkLoads()[index]
            load.setName( nameEntry.get() )
            self.refresh()
            editscreen.destroy()

class LoadTab(object):
    def __init__(self, index, load, details, notebook):
        if load.getName() == None:
            self.name = f'Load{index+1}'
            load.setName(self.name)
        else:
            self.name = load.getName()
        self.details = details
        self.notebook = notebook
        
        self.loadFrame = ttk.Frame(self.notebook)
        self.loadFrame.pack(fill=BOTH, expand=TRUE)

        self.container = ttk.Frame(self.loadFrame)
        self.container.grid()

        # Left part
        self.loadFrame1 = ttk.Frame(self.container)
        self.loadFrame1.grid(column=0, row=0, sticky='nw')

        # Separator line
        ttk.Separator(self.container, orient='vertical').grid(column=1, row=0, sticky='ns')

        # Center part
        self.loadFrame2 = ttk.Frame(self.container)
        self.loadFrame2.grid(column=2, row=0, sticky='nw')

        # Separator line
        ttk.Separator(self.container, orient='vertical').grid(column=3, row=0, sticky='ns')

        # Right part
        self.loadFrame3 = ttk.Frame(self.container)
        self.loadFrame3.grid(column=4, row=0, sticky='nw')

        ttk.Label(self.loadFrame1, text='Value').grid(column=1, row=0)
        ttk.Label(self.loadFrame1, text='Unit').grid(column=2, row=0)
        ttk.Label(self.loadFrame1, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.loadFrame1, text='Calc.').grid(column=4, row=0)

        ttk.Label(self.loadFrame2, text='Value').grid(column=1, row=0)
        ttk.Label(self.loadFrame2, text='Unit').grid(column=2, row=0)
        ttk.Label(self.loadFrame2, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.loadFrame2, text='Calc.').grid(column=4, row=0)

        ttk.Label(self.loadFrame3, text='Value').grid(column=1, row=0)
        ttk.Label(self.loadFrame3, text='Unit').grid(column=2, row=0)
        ttk.Label(self.loadFrame3, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.loadFrame3, text='Calc.').grid(column=4, row=0)

        temp = []
        i = 0
        row = 1
        n = 1

        # Iterate through load details and print to Details module
        for key, value in self.details.getWorkLoadDetails().items():
            if i == 3:
                if n == 1:
                    TestDetailRow(self.loadFrame1, temp, self.details, row)
                    temp=[]
                    i = 0
                elif n == 2:
                    TestDetailRow(self.loadFrame2, temp, self.details, row)
                    temp=[]
                    i = 0
                else:
                    TestDetailRow(self.loadFrame3, temp, self.details, row)
                    temp=[]
                    i = 0
                        
            temp.append([key, value])
            i += 1
            row += 1

            if row == 24:
                n = 2

            if row == 42:
                n = 3
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
            
class TestDetailRow(object):

    def __init__(self, rowFrame, temp, workLoadObject, row):
        self.workLoadObject = workLoadObject
        self.flag = 0

        
        if temp[0][0] == 'id':
            self.label = temp[1][0]
            self.value = temp[1][1]
            self.unitLabel = temp[2][0]
            self.unit = temp[2][1]
            self.flag = 1
        else:
            self.label = temp[0][0]
            self.value = temp[0][1]
            self.unitLabel = temp[1][0]
            self.unit = temp[1][1]
            self.radioLabel = temp[2][0]
            self.radio = temp[2][1]

        if '2' in self.label:
            self.label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(rowFrame, text=self.label_subscripted, anchor='w').grid(column=0, row=row)
        else:
            ttk.Label(rowFrame, text=self.label, anchor='w').grid(column=0, row=row)
        

        #Value
        self.valueVar = StringVar(value=self.value, name=f'{self.label}-{app.getActiveTest().id}-{self.workLoadObject.id}')
            
        self.valueEntry = ttk.Entry(rowFrame, width=5, textvariable=self.valueVar)
        self.valueEntry.grid(column=1, row=row)
        self.valueVar.trace('w', self.updateValue)

        # Unit
        if self.label != 'pH' or self.label != 'pH0':
            units = app.settings.getUnits()[f'{self.label}_units']
            tempMenuButton = ttk.Menubutton(rowFrame)
            tempMenuButton.config(text=app.settings.getUnitDef()[f'{self.label}_unit'])

            tempMenu = Menu(tempMenuButton, tearoff=False)
            for i, u in enumerate(units):
                TestDetailMenuElem(tempMenu, tempMenuButton, u, i, units, f'{self.label}_unit', self.workLoadObject)
            tempMenuButton['menu']=tempMenu
            tempMenuButton.grid(column=2, row=row)

        if self.flag != 1:
            # Measured/Calculated
            self.mcVar = IntVar(value=self.radio, name=f'{self.radioLabel}-{app.getActiveTest().id}-{self.workLoadObject.id}')

            self.radio1 = ttk.Radiobutton(rowFrame, value=0, variable=self.mcVar)
            self.radio1.grid(column=3, row=row)

            self.radio2 = ttk.Radiobutton(rowFrame, value=1, variable=self.mcVar)
            self.radio2.grid(column=4, row=row)
            self.mcVar.trace('w', self.updateMC)
    
    def updateValue(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.workLoadObject, name, self.valueVar.get())

    def updateUnit(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.workLoadObject, name, self.unitVar.get())
    
    def updateMC(self, name, index, mode):
        name = name.split('-')[0]
        setattr(self.workLoadObject, name, self.mcVar.get())

class TestDetailMenuElem(object):
    def __init__(self, menu, menuButton, label, index, elems, name, workload):
        self.menu = menu
        self.menuButton = menuButton
        self.label = label
        self.index = index
        self.elems = elems
        self.name = name
        self.workLoad = workload

        self.menu.add_command(label=self.label, command=lambda: self.updateValue())

    def updateValue(self):
        self.menuButton.config(text=self.elems[self.index])
        self.workLoad.setUnit(self.name, self.elems[self.index])