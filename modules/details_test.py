from tkinter import *
from tkinter import ttk
from objects.app import app

class TestDetailModule(object):    
    def __init__(self, detailsPanel):
        self.container = ttk.Labelframe(detailsPanel, text="Test details")
        self.container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        ## Details frame
        details = ttk.Frame(self.container)
        details.pack(side=LEFT, fill = BOTH, expand=TRUE)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        ttk.Button(details, text="Calculate").pack(side=BOTTOM)

        ## Load notebook
        self.loadsContainer = ttk.Frame(self.container)
        self.loadsContainer.pack(side=RIGHT)
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
        self.loadNotebook = ttk.Notebook(parent, style='loadNotebook.TNotebook')
        self.loadNotebook.bind('<Button-1>', lambda e: self.handleTabClick(e))

        # Add/edit button
        self.addButton = ttk.Button(parent, text='Add', command=lambda: self.addLoad())
        self.editButton = ttk.Button(parent, text='Edit', command=lambda: self.editLoad())

    def addLoad(self):
        # Add load to active test
        activeTest = app.getActiveTest()
        workLoadObject = activeTest.createLoad()
        i = len(self.loadTabs)
        details = workLoadObject.getDetails()

        newLoad = LoadTab(i, workLoadObject, details, self.loadNotebook)
            
        # Append tab
        self.loadTabs.append(newLoad)
        tabCount = self.loadNotebook.index('end')
        self.loadNotebook.insert('end', newLoad.containerFrame, text=newLoad.getName())
        self.loadNotebook.select(tabCount) 

        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)

    def refresh(self):
        self.loadTabs = []
        # Hide previous tabs
        for t in self.loadNotebook.tabs():
            self.loadNotebook.forget(t)

        activeTest = app.getActiveTest()

        # Fetch list of load objects
        loads = activeTest.getWorkLoads()
        
        for i, l in enumerate(loads):
            # Get load details
            details = l.getDetails()

            newLoad = LoadTab(i, l, details, self.loadNotebook)
            
            # Append tab
            self.loadTabs.append(newLoad)
            tabCount = self.loadNotebook.index('end')
            self.loadNotebook.insert('end', newLoad.containerFrame, text=l.getName())
            self.loadNotebook.select(tabCount) 

        self.loadNotebook.pack(expand=TRUE)
        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)

    def handleTabClick(self, e):
        clickedTabIndex = self.loadNotebook.index(f'@{e.x},{e.y}')
        activeTest = app.getActiveTest()
        workLoads = activeTest.getWorkLoads()

        if self.loadNotebook.identify(e.x, e.y) == 'close':
            self.loadNotebook.forget(clickedTabIndex)
            del workLoads[clickedTabIndex]
            
    def editLoad(self):
        index = self.loadNotebook.index('current')

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
        
        self.containerFrame = ttk.Frame(self.notebook)
        self.containerFrame.pack()
        
        self.canvas = Canvas(self.containerFrame)
        self.loadFrame = ttk.Frame(self.canvas)

        sbar = ttk.Scrollbar(self.containerFrame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT)
        self.canvas.create_window((0,0), window=self.loadFrame, anchor='nw')
        self.loadFrame.bind("<Configure>", self.callback)

        ttk.Label(self.loadFrame, text='Value').grid(column=1, row=0)
        ttk.Label(self.loadFrame, text='Unit').grid(column=2, row=0)
        ttk.Label(self.loadFrame, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.loadFrame, text='Calc.').grid(column=4, row=0)

        temp = []
        i = 0
        j = 1

        # Iterate through load details and print to Details module
        for key, value in self.details.getWorkLoadDetails().items():

            if i == 3:
                TestDetailRow(self.loadFrame, temp, self.details, j)
                temp=[]
                i = 0
                    
            temp.append([key, value])
            i = i + 1
            j = j + 1

    def callback(self,e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=225,height=250)
    
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

        ttk.Label(rowFrame, text=self.label, anchor='w').grid(column=0, row=row)
  
        #Value
        self.valueVar = StringVar(value=self.value, name=f'{self.label}-{app.getActiveTest().id}-{self.workLoadObject.id}')
        
        self.valueEntry = ttk.Entry(rowFrame, width=7, textvariable=self.valueVar)
        self.valueEntry.grid(column=1, row=row)
        self.valueVar.trace('w', self.updateValue)

        # Unit
        if self.label != 'pH':
            units = app.settings.getUnits()[f'{self.label}_units']
            print(f'UNITS: {units}')
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