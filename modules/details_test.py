from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.workLoadDetails import WorkLoadDetails

class TestDetailModule(object):    
    def __init__(self, detailsPanel):
        container = ttk.Labelframe(detailsPanel, text="Test details")
        container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        ## Details frame
        details = ttk.Frame(container)
        details.pack(side=LEFT, fill = BOTH, expand=TRUE)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        ttk.Button(details, text="Calculate").pack(side=BOTTOM)
        #

        ## Load notebook frame
        loadsContainer = ttk.Frame(container)
        loadsContainer.pack(side=RIGHT)

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
        #

        ## Notebook
        #self.loadNotebook = ttk.Notebook(loadsContainer, style='loadNotebook.TNotebook')
        self.loadNotebook = ttk.Notebook(loadsContainer)
        
        self.loadNotebook.pack(expand=TRUE)
        self.loadNotebook.bind('<Button-1>', lambda e: self.handleTabClick(e))

        # Initial Tab
        self.tab0 = ttk.Frame(self.loadNotebook, width=200, height=200)
        self.tab0.pack(expand=TRUE)
        
        self.loadNotebook.add(self.tab0, text='+')

    def handleTabClick(self, e):
        clickedTabIndex = self.loadNotebook.index(f'@{e.x},{e.y}')
        tabCount = self.loadNotebook.index('end')  

        if clickedTabIndex == tabCount-1:
            self.addLoad()
        """ if self.loadNotebook.identify(e.x, e.y) == 'close':
            self.loadNotebook.forget(clickedTabIndex)
        else:
            self.addLoad() """

    """ def createTab(self, e):
        # Make sure '+'-tab is pressed
        clickedTabIndex = self.loadNotebook.index(f'@{e.x},{e.y}')
        tabCount = self.loadNotebook.index('end')      

        if clickedTabIndex == tabCount-1:
            load = ttk.Frame(self.loadNotebook, width=300, height=200)
            load.pack(expand=TRUE)
            ttk.Label(load, text="qwerty").pack()
            self.loadNotebook.insert(tabCount-1, load, text=f'Load{tabCount}') """

    def addLoad(self):
        loadFrame = ttk.Frame(self.loadNotebook)
        loadFrame.pack(expand=TRUE)

        # Add load to active test
        activeTest = app.getActiveTest()
        print(f'WORKING WITH TEST: {activeTest.id}')
        workLoadObject = WorkLoadDetails()
        activeTest.addWorkLoad(workLoadObject)
        #print(f'WORKING WITH ID: {workLoadObject.id}')

        temp = []
        i = 0

        # Iterate through load details and print to Details module
        for key, value in workLoadObject.getWorkLoadDetails().items():

            if i == 3:
                rowFrame = ttk.Frame(loadFrame)
                rowFrame.pack(fill=X)
                TestDetailRow(rowFrame, temp, workLoadObject)
                    
                temp=[]
                i = 0
                
            temp.append([key, value])
            i = i + 1

        # Append tab
        tabCount = self.loadNotebook.index('end')
        self.loadNotebook.insert(tabCount-1, loadFrame, text=f'Load{tabCount}')
        self.loadNotebook.select(tabCount-1)

    def getTestData(self):
        pass

    def refreshTestDetails(self):
        activeTest = app.getActiveTest()
        self.testId.config(text=f'Id: {activeTest.id}')

        # Refresh load notebook
        loads = activeTest.getWorkLoads()
        print(f'LOADS: {loads}')

class TestDetailRow(object):

    def __init__(self, rowFrame, temp, workLoadObject):
        self.workLoadObject = workLoadObject
        self.flag = 0

        #print(f'CREATING ROWS FOR LOAD WITH ID: {self.workLoadObject.id}')

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

        ttk.Label(rowFrame, text=self.label, anchor='w').pack(side=LEFT)
  
        #Value
        self.valueVar = StringVar(value=self.value, name=f'{self.label}-{self.workLoadObject.id}')
        app.strVars.append(self.valueVar)
        self.valueEntry = ttk.Entry(rowFrame, width=7, textvariable=self.valueVar)
        self.valueEntry.pack(side=LEFT)
        #self.valueVar.trace( 'w', lambda name, index, mode, sv=self.valueVar: self.updateValue(name, workLoadObject) )
        self.valueVar.trace('w', self.updateValue)

        #Unit
        self.unitVar = StringVar(value=self.unit, name=f'{self.unitLabel}-{self.workLoadObject.id}')
        app.strVars.append(self.unitVar)
        self.unitEntry = ttk.Entry(rowFrame, width=7, textvariable=self.unitVar)
        self.unitEntry.pack(side=LEFT)
        #self.unitEntry.insert(0, self.unit)
        self.unitVar.trace('w', self.updateUnit)

        if self.flag != 1:
            # Measured/Calculated
            self.mcVar = IntVar(value=self.radio, name=f'{self.radioLabel}-{self.workLoadObject.id}')
            app.strVars.append(self.mcVar)
            self.radio1 = ttk.Radiobutton(rowFrame, value=0, variable=self.mcVar)
            self.radio1.pack(side=LEFT)

            self.radio2 = ttk.Radiobutton(rowFrame, value=1, variable=self.mcVar)
            self.radio2.pack(side=LEFT)
            self.mcVar.trace('w', self.updateMC)
    
    def updateValue(self, name, index, mode):
        #print(f'UPDATING LOAD WITH ID: {self.workLoadObject.id}')
        name = name.split('-')[0]
        #print( f'{name} BEFORE: {getattr(self.workLoadObject, name)}' )
        setattr(self.workLoadObject, name, self.valueVar.get())
        #print( f'{name} AFTER: {getattr(self.workLoadObject, name)}' )

    def updateUnit(self, name, index, mode):
        #print( f'{name} BEFORE: {getattr(self.workLoadObject, name)}' )
        name = name.split('-')[0]
        setattr(self.workLoadObject, name, self.unitVar.get())
        #print( f'{name} AFTER: {getattr(self.workLoadObject, name)}' )
    
    def updateMC(self, name, index, mode):
        #print( f'{name} BEFORE: {getattr(self.workLoadObject, name)}' )
        name = name.split('-')[0]
        setattr(self.workLoadObject, name, self.mcVar.get())
        #print( f'{name} AFTER: {getattr(self.workLoadObject, name)}' )