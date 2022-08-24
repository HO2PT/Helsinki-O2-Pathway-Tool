import gc
from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.ScrollableNotebook import ScrollableNotebook

class TestDetailModule(ttk.Labelframe):
    def __init__(self, detailsPanel, *args, **kwargs):
        ttk.Labelframe.__init__(self, detailsPanel, text="Test details", borderwidth=5)
        self.configure(cursor='arrow')

        if app.settings.visDefaults['testDetails']:
            self.pack(side = LEFT, padx=(5,5), anchor='n')

        self.configure(borderwidth=5)

        ## Details frame
        details = ttk.Frame(self)
        details.pack(side=LEFT, fill = BOTH)
        
        details.pack_configure(padx=5)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        ## Load notebook
        self.loadsContainer = ttk.Frame(self)
        self.loadNotebook = LoadNotebook(self.loadsContainer)

    def addLoad(self):
        self.loadNotebook.addLoad()

    def refreshTestDetails(self):
        try:
            self.testId.config(text=f'Id: {app.getActiveTest().id}')
            self.testId.pack()
            self.loadsContainer.pack(side=LEFT, fill=BOTH)
            self.loadNotebook.refresh()
        except:
            pass
        
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
            pHValue = float(f'{"{0:.2f}".format(pHrest - (i * pHstep))}')
            pHvalues.append(pHValue)
            details.setValue('pH', pHValue)

            Tvalue = float(f'{"{0:.1f}".format(Trest + (i * Tstep))}')
            Tvalues.append(Tvalue)
            details.setValue('T', Tvalue)

        return pHvalues, Tvalues

    def addLoad(self):
        # Add load to active test
        activeTest = app.getActiveTest()
        isImported = False

        for w in activeTest.workLoads:
            if w.details.isImported:
                isImported = True

        workLoadObject = activeTest.createLoad()
        i = len(self.loadTabs)
        if not isImported:
            pHvalues, Tvalues = self.updatePhAndTemp()
        details = workLoadObject.getDetails()

        newLoad = LoadTab(i, workLoadObject, details, self.loadbook)

        # Append tab
        self.loadTabs.append(newLoad)
        tabCount = self.loadbook.index('end')
        self.loadbook.add(newLoad.loadFrame, text=newLoad.getName())
        self.loadbook.select(tabCount) 

        if not isImported:
            for i, l in enumerate(self.loadTabs):
                l.updateValues('pH', pHvalues[i])
                l.updateValues('T', Tvalues[i])

        self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
        self.editButton.pack(side=LEFT, expand=TRUE, fill=X)

    def refresh(self, index=None):
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
                else:
                    continue
            else:
                newLoad = LoadTab(i, l, details, self.loadbook)
            
                # Append tab
                self.loadTabs.append(newLoad)
                tabCount = self.loadbook.index('end')
                self.loadbook.add(newLoad.loadFrame, text=l.getName())
        
        # If the index of a tab is given, select the tab
        if index != None:
            self.loadbook.select(index)
        else:
            self.loadbook.select(tabCount)

        try:
            self.loadbook.pack_info()
        except:
            self.loadbook.pack(fill=BOTH,expand=True)
            self.addButton.pack(side=LEFT, expand=TRUE, fill=X)
            self.editButton.pack(side=LEFT, expand=TRUE, fill=X)
            
    def editLoad(self):
        index = self.loadbook.index('current')
        load = app.getActiveTest().getWorkLoads()[index]

        # Create edit popup
        editscreen = Toplevel(width=self.editButton.winfo_width(), height=self.editButton.winfo_height()*4, bg='#4eb1ff', borderwidth=3)
        editscreen.overrideredirect(True)
        editscreen.focus_force()
        editscreenX = self.loadbook.winfo_rootx() + (self.loadbook.winfo_width()/2 - editscreen.cget('width')/2)
        ediscreenY = self.editButton.winfo_rooty() - (self.loadbook.winfo_height()/2 + editscreen.cget('height')/2)
        editscreen.geometry("+%d+%d" % ( editscreenX, ediscreenY ))
        editscreen.pack_propagate(False)

        def move(e):
            winX = self.loadbook.winfo_rootx() + (self.loadbook.winfo_width()/2 - editscreen.cget('width')/2)
            winY = self.editButton.winfo_rooty() - (self.loadbook.winfo_height()/2 + editscreen.cget('height')/2)
            editscreen.geometry("+%d+%d" % ( winX, winY ))
            editscreen.configure(width=self.editButton.winfo_width())
            editscreen.lift()

        self.bindId = app.root.bind('<Configure>', move)

        container = Frame(editscreen, bd=0, padx=10, pady=10)
        container.pack(fill=BOTH, expand=True)
        
        footer = Frame(editscreen, bd=0, padx=10)
        footer.pack(fill=BOTH, expand=True)
        ttk.Label(container, text='Set load name').pack()
        nameEntry = ttk.Entry(container, width=30)
        nameEntry.focus_force()
        nameEntry.pack(expand=TRUE)
        nameEntry.insert(0, load.name)

        def edit(e=None):
            load.setName( nameEntry.get() )
            self.refresh(index)
            editscreen.destroy()
            app.root.unbind('<Configure>', self.bindId)

        def close(*args):
            editscreen.destroy()
            app.root.unbind('<Configure>', self.bindId)

        ttk.Button(footer, text='Save', command=edit).pack(side=LEFT, fill=X, expand=True)
        ttk.Button(footer, text='Close', command=close).pack(side=LEFT, fill=X, expand=True)
        editscreen.bind('<KeyPress-Return>', edit)
        editscreen.bind('<KeyPress-Escape>', close)

class LoadTab(object):
    def __init__(self, index, load, details, notebook):
        self.name = load.getName()
        self.details = details
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
        ttk.Label(a, text='Or').grid(column=1, row=0)
        ttk.Separator(a).grid(column=2, row=0, sticky='we')
        
        temp = ['Q', loadDetails['Q'], loadDetails['Q_unit'], loadDetails['Q_MC']]
        self.detailRows.append( TestDetailRow(extra, temp, self.details, 3) )

        # Details - Load/Speed/Incline
        extra2 = ttk.Labelframe(self.loadFrame3, text='Details')
        extra2.grid(column=0, row=4, columnspan=5, sticky='we', pady=(30,0), padx=5)
        
        if app.settings.getTestDef()['loadMode'] == 0:
            temp = ['Load', loadDetails['Load'], loadDetails['Load_unit']]
            self.detailRows.append( TestDetailRow(extra2, temp, self.details, 3) )
        else:
            temp = ['Velocity', loadDetails['Velocity'], loadDetails['Velocity_unit']]
            self.detailRows.append( TestDetailRow(extra2, temp, self.details, 3) )
            temp = ['Incline', loadDetails['Incline'], loadDetails['Incline_unit']]
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
        self.unit = temp[2]

        try:
            self.radio = temp[3]
        except:
            self.radio = None

        if '2' in self.label:
            self.label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(rowFrame, text=self.label_subscripted, anchor='w').grid(column=0, row=row, sticky='we')
        else:
            ttk.Label(rowFrame, text=self.label, anchor='w').grid(column=0, row=row, sticky='we')

        # Value
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
                self.tempMenuButton = ttk.Menubutton(rowFrame)
                self.tempMenuButton.config(text=self.unit)

                tempMenu = Menu(self.tempMenuButton, tearoff=False)
                for i, u in enumerate(units):
                    menuelem = TestDetailMenuElem(tempMenu, self.tempMenuButton, u, i, units, f'{self.label}_unit', self.workLoadObject)
                    self.objects.append(menuelem)
                self.tempMenuButton['menu']=tempMenu
                self.tempMenuButton.grid(column=2, row=row, sticky='we')
        else:
            ttk.Label(rowFrame, text=units[0]).grid(column=2, row=row)

        # Measured/Calculated
        if self.radio != None:
            self.mcVar = IntVar(value=self.radio)
            self.vars.append(self.mcVar)
            self.radio1 = ttk.Radiobutton(rowFrame, value=0, variable=self.mcVar)
            self.radio1.grid(column=3, row=row)

            self.radio2 = ttk.Radiobutton(rowFrame, value=1, variable=self.mcVar)
            self.radio2.grid(column=4, row=row)
            mctraceid = self.mcVar.trace('w', self.updateMC)
            self.traceids.append(mctraceid)
        
    def updateValue(self, name, index, mode):
        self.workLoadObject.setValue(self.label, self.valueVar.get())

    def updateUnit(self, name, index, mode):
        # Update unit change to every load
        for l in app.getActiveTest().getWorkLoads():
            l.setUnit(self.label, self.unitVar.get())
    
    def updateMC(self, name, index, mode):
        self.workLoadObject.setMC(f'{self.label}_MC', self.mcVar.get())

        # Update every load
        for l in app.getActiveTest().getWorkLoads():
            l.getDetails().setMC(f'{self.label}_MC', self.mcVar.get())

        loadTabs = app.testDetailModule.loadNotebook.loadTabs

        for l in loadTabs:
            l.updateMCs(f'{self.label}_MC', self.mcVar.get())

class TestDetailMenuElem(object):
    def __init__(self, menu, menuButton, label, index, elems, name, workload):
        self.menuButton = menuButton
        self.index = index
        self.elems = elems
        self.name = name

        menu.add_command(label=label, command=self.updateValue)

    def updateValue(self):
        self.menuButton.config(text=self.elems[self.index])

        for l in app.getActiveTest().getWorkLoads():
            l.getDetails().setUnit(self.name, self.elems[self.index])

        loadTabs = app.testDetailModule.loadNotebook.loadTabs

        for l in loadTabs:
            l.updateUnitButtons(self.name, self.elems[self.index])
        