import gc
from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.ScrollableNotebook import ScrollableNotebook
from objects.test import Test

class TestDetailModule(ttk.Frame):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Frame.__init__(self, detailsPanel, *args, **kwargs)
        self.configure(cursor='arrow')
        
        if app.settings.visDefaults['testDetails']:
            self.pack(side = LEFT, fill = BOTH, expand=TRUE)

        self.configure(borderwidth=5)
        self.container = ttk.Labelframe(self, text="Test details", borderwidth=5)
        self.container.pack(fill = BOTH, expand=TRUE)

        ## Details frame
        details = ttk.Frame(self.container)
        details.pack(side=LEFT, fill = BOTH)#, expand=TRUE)
        
        details.pack_configure(padx=5)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        ## Load notebook
        self.loadsContainer = ttk.Frame(self.container)
        self.loadNotebook = LoadNotebook(self.loadsContainer)

    def addLoad(self):
        self.loadNotebook.addLoad()

    def refreshTestDetails(self):
        # Refresh details
        # if there is no active test, create a dummy test
        try:
            self.testId.config(text=f'Id: {app.getActiveTest().id}')
        except:
            emptyTest = Test()
            app.setActiveTest(emptyTest)
            self.testId.config(text=f'Id: {app.getActiveTest().id}')

        self.testId.pack()
        self.loadsContainer.pack(side=LEFT, fill=BOTH)#, expand=TRUE)
        self.loadNotebook.refresh()
        
class LoadNotebook(object):
    def __init__(self, parent):
        self.loadTabs = []
        # self.parent = parent

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
        self.loadbook = ScrollableNotebook(parent, parentObj=self, style="loadNotebook.TNotebook", wheelscroll=True)

        # Add/edit button
        self.addButton = ttk.Button(parent, text='Add', command=lambda: self.addLoad())
        self.editButton = ttk.Button(parent, text='Edit...', command=lambda: self.editLoad())

    def updatePhAndTemp(self):
        activeTest = app.getActiveTest()

        # Add linear change in pH and T
        pHrest = float(app.settings.testDefaults['pH @ rest'])
        Trest = float(app.settings.testDefaults['Tc @ rest'])
        pHpeak = float(app.settings.testDefaults['pH\u209A\u2091\u2090\u2096'])
        Tpeak = float(app.settings.testDefaults['Tc\u209A\u2091\u2090\u2096'])
        pHDif = float(pHrest) - float(pHpeak)
        Tdif = float(Tpeak) - float(Trest)

        if len(activeTest.getWorkLoads()) > 0:
            if pHrest != pHpeak:
                activeTest.getWorkLoads()[-1].getDetails().setValue('pH', pHpeak)

            if Trest != Tpeak:
                activeTest.getWorkLoads()[-1].getDetails().setValue('T', Tpeak)

            pHstep = pHDif / (len(activeTest.getWorkLoads())-1)
            pHvalues = []

            Tstep = Tdif / (len(activeTest.getWorkLoads())-1)
            Tvalues = []

        # Add linear change
        for i, w in enumerate(activeTest.getWorkLoads()):
            details = w.getDetails()
            pHValue = pHrest - (i * pHstep)
            pHvalues.append(f'{"{0:.2f}".format(pHValue)}')
            details.setValue('pH', pHValue)

            Tvalue = Trest + (i * Tstep)
            Tvalues.append(f'{"{0:.1f}".format(Tvalue)}')
            details.setValue('T', Tvalue)

        return pHvalues, Tvalues

    def addLoad(self):
        # Add load to active test
        activeTest = app.getActiveTest()
        workLoadObject = activeTest.createLoad()
        i = len(self.loadTabs)
        pHvalues, Tvalues = self.updatePhAndTemp()
        details = workLoadObject.getDetails()

        newLoad = LoadTab(i, workLoadObject, details, self.loadbook)

        # Append tab
        self.loadTabs.append(newLoad)
        tabCount = self.loadbook.index('end')
        self.loadbook.add(newLoad.loadFrame, text=newLoad.getName())
        self.loadbook.select(tabCount) 

        for i, l in enumerate(self.loadTabs):
            if i != 0 and i != len(self.loadTabs)-1:
                l.updateValues('pH', pHvalues[i])
                l.updateValues('T', Tvalues[i])

        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)

    def refresh(self):
        for t in self.loadbook.tabs():
            self.loadbook.forget(t)

        for tab in self.loadTabs: # Delete loadtab objects
            for r in tab.detailRows:
                if len(r.objects) != 0:
                    for o in r.objects:
                        del o
                for i, v in enumerate(r.vars):
                    v.trace_vdelete('w', r.traceids[i] )
                    del v
                # asd = id(r)
                r.destroy()
                del r
            tab.loadFrame.destroy()
            del tab
        gc.collect()
        
        self.loadTabs = []
        activeTest = app.getActiveTest()
        
        # Fetch list of load objects
        loads = activeTest.getWorkLoads()
        
        for i, l in enumerate(loads):
            # Get load details
            details = l.getDetails()

            # Skip possible empty loads
            if details.isImported == True:

                if i == 0 or details.getWorkLoadDetails()['Load'] != 0:
                    newLoad = LoadTab(i, l, details, self.loadbook)
                
                    # Append tab
                    self.loadTabs.append(newLoad)
                    tabCount = self.loadbook.index('end')
                    self.loadbook.add(newLoad.loadFrame, text=l.getName())
                    self.loadbook.select(tabCount)
                else:
                    continue
            else:
                newLoad = LoadTab(i, l, details, self.loadbook)
            
                # Append tab
                self.loadTabs.append(newLoad)
                tabCount = self.loadbook.index('end')
                self.loadbook.add(newLoad.loadFrame, text=l.getName())
                self.loadbook.select(tabCount)

        try:
            self.loadbook.pack_info()
        except:
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
        if 'Load' in load.getName():
            self.name = f'Load{index+1}'
            load.setName(self.name)
        else:
            self.name = load.getName()
        self.details = details
        # self.notebook = notebook
        self.detailRows = []
        
        self.loadFrame = ttk.Frame(notebook)
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
        items1 = ['VO2','[Hb]','SaO2']
        items2 = ['CaO2', 'CvO2','C(a-v)O2','QaO2','SvO2','PvO2']
        items3 = ['T', 'pH']

        loadDetails = self.details.getWorkLoadDetails()

        for row, i in enumerate(items1):
            label = i
            value = loadDetails[i]
            unit = loadDetails[f'{i}_unit']
            mc = loadDetails[f'{i}_MC']
            temp = [label, value, unit, mc]
            self.detailRows.append( TestDetailRow(self.loadFrame1, temp, self.details, row+1) )

        for row, i in enumerate(items2):
            label = i
            value = loadDetails[i]
            unit = loadDetails[f'{i}_unit']
            mc = loadDetails[f'{i}_MC']
            temp = [label, value, unit, mc]
            self.detailRows.append( TestDetailRow(self.loadFrame2, temp, self.details, row+1) )

        for row, i in enumerate(items3):
            label = i
            value = loadDetails[i]
            unit = loadDetails[f'{i}_unit']
            mc = loadDetails[f'{i}_MC']
            temp = [label, value, unit, mc]
            self.detailRows.append( TestDetailRow(self.loadFrame3, temp, self.details, row+1) )

        # HR/SV or Q
        extra = ttk.Labelframe(self.loadFrame1, text='Either')
        extra.grid(column=0, row=4, columnspan=5, sticky='we', pady=(10,0), padx=5)
        extra.columnconfigure(0, weight=1)
        extra.columnconfigure(1, weight=1)
        extra.columnconfigure(2, weight=1)
        extra.columnconfigure(3, weight=1)
        extra.columnconfigure(4, weight=1)
        
        temp = ['HR', loadDetails['HR'], loadDetails['HR_unit'], loadDetails['HR_MC']]
        self.detailRows.append( TestDetailRow(extra, temp, self.details, 0) )
        temp = ['SV', loadDetails['SV'], loadDetails['SV_unit'], loadDetails['SV_MC']]
        self.detailRows.append( TestDetailRow(extra, temp, self.details, 1) )

        a = ttk.Frame(extra)
        a.grid(column=0, row=2, sticky='we', columnspan=5)
        a.columnconfigure(0, minsize=5)
        a.columnconfigure(1, weight=0)
        a.columnconfigure(2, weight=3)
        ttk.Separator(a).grid(column=0, row=0, sticky='we')
        ttk.Label(a, text='Or').grid(column=1, row=0)#, columnspan=5)
        ttk.Separator(a).grid(column=2, row=0, sticky='we')
        
        temp = ['Q', loadDetails['Q'], loadDetails['Q_unit'], loadDetails['Q_MC']]
        self.detailRows.append( TestDetailRow(extra, temp, self.details, 3) )

        # Details - Load/Speed/Incline
        extra2 = ttk.Labelframe(self.loadFrame3, text='Details')
        extra2.grid(column=0, row=4, columnspan=5, sticky='we', pady=(30,0), padx=5)
        
        if app.settings.getTestDef()['loadMode'] == 0:
            temp = ['Load', loadDetails['Load']]
            self.detailRows.append( TestDetailRow(extra2, temp, self.details, 3) )
        else:
            temp = ['Velocity', loadDetails['Velocity']]
            self.detailRows.append( TestDetailRow(extra2, temp, self.details, 3) )
            temp = ['Incline', loadDetails['Incline']]
            self.detailRows.append( TestDetailRow(extra2, temp, self.details, 4) )
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def updateValues(self, label, value):
        for r in self.detailRows:
            if r.label == label:
                r.valueVar.set(value)

    def updateUnitButtons(self, unit, value):
        for r in self.detailRows:
            if hasattr(r, 'tempMenuButton'):
                unitName = f'{r.label}_unit'
                if unitName == unit:
                    r.tempMenuButton.configure(text=value)

    def updateMCs(self, mc, value):
        for r in self.detailRows:
            name = f'{r.label}_MC'
            if name == f'{mc}':
                r.mcVar.set(value)
            
class TestDetailRow(ttk.Frame):
    def __init__(self, rowFrame, temp, workLoadObject, row, *args, **kwargs):
        ttk.Frame.__init__(self, rowFrame, *args, **kwargs)
        self.grid()
        self.workLoadObject = workLoadObject
        self.vars = []
        self.objects = []
        self.traceids = []

        self.label = temp[0]
        self.value = temp[1]
        try:
            self.unit = temp[2]
        except:
            self.unit = 0
        try:
            self.radio = temp[3]
        except:
            self.radio = None


        if '2' in self.label:
            self.label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(rowFrame, text=self.label_subscripted, anchor='w').grid(column=0, row=row, sticky='we')
        else:
            ttk.Label(rowFrame, text=self.label, anchor='w').grid(column=0, row=row, sticky='we')
            
        #Value
        self.valueVar = StringVar(value=self.value)
        self.vars.append(self.valueVar)
        self.valueEntry = ttk.Entry(rowFrame, width=5, textvariable=self.valueVar)
        self.valueEntry.grid(column=1, row=row, sticky='we')
        valtraceid = self.valueVar.trace('w', self.updateValue)
        self.traceids.append(valtraceid)

        # Unit
        units = app.settings.getUnits()[f'{self.label}_units']
        if len(units) != 1:
            if self.label != 'pH':
                units = app.settings.getUnits()[f'{self.label}_units']
                self.tempMenuButton = ttk.Menubutton(rowFrame)
                self.tempMenuButton.config(text=app.settings.getUnitDef()[f'{self.label}_unit'])

                tempMenu = Menu(self.tempMenuButton, tearoff=False)
                for i, u in enumerate(units):
                    menuelem = TestDetailMenuElem(tempMenu, self.tempMenuButton, u, i, units, f'{self.label}_unit', self.workLoadObject)
                    self.objects.append(menuelem)
                self.tempMenuButton['menu']=tempMenu
                self.tempMenuButton.grid(column=2, row=row, sticky='we')
        else:
            ttk.Label(rowFrame, text=units[0]).grid(column=2, row=row)

        if self.radio != None:
            # Measured/Calculated
            self.mcVar = IntVar(value=self.radio)
            self.vars.append(self.mcVar)
            self.radio1 = ttk.Radiobutton(rowFrame, value=0, variable=self.mcVar)
            self.radio1.grid(column=3, row=row)

            self.radio2 = ttk.Radiobutton(rowFrame, value=1, variable=self.mcVar)
            self.radio2.grid(column=4, row=row)
            mctraceid = self.mcVar.trace('w', self.updateMC)
            self.traceids.append(mctraceid)
        
    def updateValue(self, name, index, mode):
        # name = name.split('-')[0]
        self.workLoadObject.setValue(self.label, self.valueVar.get())
        # setattr(self.workLoadObject, name, self.valueVar.get())

    def updateUnit(self, name, index, mode):
        # name = name.split('-')[0]
        # Update unit change to every load
        for l in app.getActiveTest().getWorkLoads():
            #print(l)
            l.setUnit(self.label, self.unitVar.get())
        # self.workLoadObject.setUnit(name, self.unitVar.get())
        # setattr(self.workLoadObject, name, self.unitVar.get())
    
    def updateMC(self, name, index, mode):
        # name = name.split('-')[0]
        self.workLoadObject.setMC(f'{self.label}_MC', self.mcVar.get())

        # Update every load
        for l in app.getActiveTest().getWorkLoads():
            l.getDetails().setMC(f'{self.label}_MC', self.mcVar.get())
            # print(l.getDetails().getWorkLoadDetails())

        loadTabs = app.testDetailModule.loadNotebook.loadTabs

        for l in loadTabs:
            l.updateMCs(f'{self.label}_MC', self.mcVar.get())

        # setattr(self.workLoadObject, name, self.mcVar.get())

class TestDetailMenuElem(object):
    def __init__(self, menu, menuButton, label, index, elems, name, workload):
        # self.menu = menu
        self.menuButton = menuButton
        # self.label = label
        self.index = index
        self.elems = elems
        self.name = name
        # self.workLoad = workload

        # self.menu.add_command(label=self.label, command=lambda: self.updateValue())
        menu.add_command(label=label, command=lambda: self.updateValue())

    def updateValue(self):
        self.menuButton.config(text=self.elems[self.index])
        for l in app.getActiveTest().getWorkLoads():
            l.getDetails().setUnit(self.name, self.elems[self.index])
            # print(l.getDetails().getWorkLoadDetails())

        loadTabs = app.testDetailModule.loadNotebook.loadTabs

        for l in loadTabs:
            l.updateUnitButtons(self.name, self.elems[self.index])
        
        # self.workLoad.setUnit(self.name, self.elems[self.index])
        