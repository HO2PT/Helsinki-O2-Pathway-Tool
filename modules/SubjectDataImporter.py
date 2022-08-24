import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.messagebox import askokcancel
from pandastable import Table, TableModel
from objects.app import app
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from modules.notification import notification

# Stage 0: id
# Stage 1: loads
# Stage 2: vo2
# Stage 3: HORIZONTAL LINE
# Stage 4: hr
# Stage 5: sv
# Stage 6: HORIZONTAL LINE
# Stage 7: q
# Stage 8: HORIZONTAL LINE
# Stage 9: hb
# Stage 10: sao2
# Stage 11: CaO2
# Stage 12: CvO2
# Stage 13: CavO2
# Stage 14: QaO2
# Stage 15: SvO2
# Stage 16: PvO2
# Stage 17: T
# Stage 18: pH

class SubjectDataImporter(object):
    def __init__(self, subject=None):
        self.stage = 0
        self.tests = {}
        self.currentDf = None
        self.tempLocData = {}
        self.dataMode = None
        self.addLinearDist = False
        self.newSubject = False
        self.newProject = False
        self.testList = []
        self.imported = {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False
        }

        # Create a project if any project is not set active
        if app.activeProject == None:
            self.project = Project()
            self.newProject = True
        else:
            self.project = app.activeProject

        # Create a subject if any subject is not set active
        if subject == None:
            self.subject = Subject(parentProject=self.project)
            self.newSubject = True
        else:
            self.subject = subject

        file = askopenfile(mode ='r')
        if file is not None:
            try:
                self.data = pd.ExcelFile(file.name)
            except:
                notification.create('error', 'Can not open file.', 5000)
                return

            self.dfList= {}

            for sheet in self.data.sheet_names:
                self.dfList[sheet] = pd.read_excel(self.data, sheet, header=None, keep_default_na=False)

            self.templateUsed = False

            if self.newSubject == True:
                params = [
                    'Load',
                    'Velocity',
                    'Incline',
                    'VO2',
                    '[Hb]',
                    'SaO2',
                    'HR',
                    'SV',
                    'Q',
                    'CaO2',
                    'CvO2',
                    'C(a-v)O2',
                    'QaO2',
                    'SvO2',
                    'PvO2',
                    'T',
                    'pH'
                ]

                # Check if template excel is used and import data automatically
                for sheetName, sheet in self.dfList.items():
                    if sheet.loc[0,0] == 'Subject-template':
                        self.subject.setId(self.dfList[sheetName].loc[2,1]) #loc[y,x]
                        self.cols = []

                        testId = f'{self.subject.id}-{sheetName}'
                        self.test = Test(id=testId, parentSubject=self.subject)
                        self.testList.append(self.test)

                        self.test.workLoads = []

                        # Check the number of loads and save column indexes
                        for i, x in enumerate(self.dfList[sheetName].loc[4,:]):
                            if 'Load' in str(x):
                                self.cols.append(i)

                        # Import values load by load
                        for i in self.cols:
                            colHasValues = False

                            for value in self.dfList[sheetName].loc[5:,i]:
                                if value != '':
                                    colHasValues = True
                            
                            # If there are values given -> create a workload
                            if colHasValues:
                                newLoad = self.test.createLoad()
                                newLoad.setName(sheet.loc[4,i])
                                newLoad.details.isImported = True
                                
                                # Start importing from row 5
                                index = 5
                                for p in params:
                                    value = self.dfList[sheetName].loc[index,i]
                                    
                                    # Replace null values with 0
                                    if value == '':
                                        value = 0

                                    newLoad.details.setValue(p, value)
                                    index += 1
                            else:
                                continue

                        self.templateUsed = True

                for t in self.testList:
                    tempAddLinearity = False
                    pHAddLinearity = False

                    for w in t.workLoads:
                        details = w.details.getWorkLoadDetails()
                        if details['T'] == 0:
                            tempAddLinearity = True
                        if details['pH'] == 0:
                            pHAddLinearity = True

                    if tempAddLinearity:
                        self.addLinearDistT(t)

                    if pHAddLinearity:
                        self.addLinearDistPH(t)
                
            if self.templateUsed:
                self.closeImporter(mode=1)
                return

            self.window = Toplevel()
            self.window.title('Subject import')
            self.window.geometry('750x500')
            self.window.update_idletasks()
            self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='Img/ho2pt.png'))
            windowX = int(self.window.winfo_screenwidth()) * 0.5 - int(self.window.winfo_width()) * 0.5
            windowY = int(self.window.winfo_screenheight()) * 0.5 - int(self.window.winfo_height()) * 0.5
            self.window.geometry("+%d+%d" % ( windowX, windowY ))

            # Left panel
            self.leftPanel = ttk.Frame(self.window, padding=(5,5))
            self.leftPanel.pack(side=LEFT, fill=Y)

            # Scrollbar
            self.yScroll = ttk.Scrollbar(self.leftPanel, orient=VERTICAL)
            self.yScroll.pack(side=RIGHT, fill=Y)

            # Progression
            ttk.Label(self.leftPanel, text='Subject import steps').pack()
            self.progressionList = Listbox(self.leftPanel, yscrollcommand=self.yScroll.set, activestyle='none')
            options = [
                'Test ID(s) * \U0001F878',
                'Load(s) *',
                'VO\u2082 *',
                '\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015',
                'HR *',
                'SV *',
                '\u2015 or \u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015',
                'Q *',
                '\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015',
                '[Hb] *',
                'SaO\u2082 *',
                'CaO\u2082',
                'CvO\u2082',
                'C(a-v)O\u2082',
                'QaO\u2082',
                'SvO\u2082',
                'PvO\u2082',
                'T',
                'pH'
            ]

            for opt in options:
                self.progressionList.insert('end', opt)

            self.progressionList.itemconfig(3, fg="gray")
            self.progressionList.itemconfig(6, fg="gray")
            self.progressionList.itemconfig(8, fg="gray")

            self.progressionList.pack(expand=1, fill=BOTH)
            self.progressionList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect(e) )

            self.yScroll['command'] = self.progressionList.yview

            # Right panel
            self.rightPanel = ttk.Frame(self.window, padding=(5,5))
            self.rightPanel.pack(side=RIGHT, fill=BOTH, expand=1)

            # Notification bar
            notifFrame = ttk.Frame(self.rightPanel)
            notifFrame.pack(fill=X)
            self.notif = ttk.Label(notifFrame, text='', anchor='center', foreground='white', font=('TkDefaultFont', 12))
            self.notif.pack(fill=X)

            # Instructions
            headerFrame = ttk.Frame(self.rightPanel)
            headerFrame.pack(fill=X)
            self.instructionText = ttk.Label(headerFrame, text='Define column/row containing ID(s)')
            self.instructionText.pack()

            # Create menubutton for selection of excel sheet
            sheetFrame = ttk.Labelframe(headerFrame, text='Select excel sheet')
            sheetFrame.pack(side=LEFT)
            self.menuButton = ttk.Menubutton(sheetFrame, text=list(self.data.sheet_names)[0])
            menu = Menu(self.menuButton, tearoff=False)

            for s in self.data.sheet_names:
                DataMenuElem(self, menu,self.menuButton, s)

            self.menuButton['menu'] = menu
            self.menuButton.pack(side=LEFT)

            # Mass selection entries
            self.strVar = StringVar(value='row')
            self.selMenuButton = ttk.Menubutton(headerFrame, textvariable=self.strVar)
            selMenu = Menu(self.selMenuButton, tearoff=False)
            selMenu.add_command(label='row', command= lambda: self.strVar.set('row'))
            selMenu.add_command(label='column', command= lambda: self.strVar.set('column'))
            self.selMenuButton['menu'] = selMenu

            self.varStart = IntVar()
            self.varEnd = IntVar()
            self.startEntry = ttk.Entry(headerFrame, textvariable=self.varStart, width=10)
            self.endEntry = ttk.Entry(headerFrame, textvariable=self.varEnd, width=10)
            
            # Packing in reversed order
            ttk.Button(headerFrame, text='Set', command=self.setMassSel).pack(side=RIGHT)
            self.endEntry.pack(side=RIGHT)
            ttk.Label(headerFrame, text='to').pack(side=RIGHT)
            self.startEntry.pack(side=RIGHT)
            self.selMenuButton.pack(side=RIGHT)
            ttk.Label(headerFrame, text='Select from:').pack(side=RIGHT, fill=X)

            # Data frame
            dataFrame = ttk.Frame(self.rightPanel)
            dataFrame.pack(fill=BOTH, expand=True)

            # Footer
            self.footer = ttk.Frame(self.rightPanel)
            self.footer.pack(side=BOTTOM, fill=X)

            self.selectionText = ttk.Label(self.footer, text='')
            self.selectionText.pack(side=LEFT)

            nameOfFirstSheet = list(self.dfList)[0]

            self.dataTable = Table(dataFrame, dataframe=self.dfList[nameOfFirstSheet], editable=False)
            self.dataTable.show()

            # Clear initial selection
            self.dataTable.clearSelected()
            self.dataTable.rowheader.clearSelected()
            self.dataTable.setSelectedCol(-1)
            self.dataTable.setSelectedRow(-1)
            
            self.dataTable.tablecolheader.bind('<Button-1>', self.selectCol)
            self.dataTable.tablecolheader.bind('<Control-Button-1>', self.handleColCtrlSelection)
            self.dataTable.tablecolheader.bind('<Shift-Button-1>', self.handleColDrag)
            self.dataTable.tablecolheader.bind('<B1-Motion>', self.handleColDrag)
            self.dataTable.tablecolheader.bind('<Button-3>', self.handleRightClick)

            self.dataTable.rowheader.bind('<ButtonRelease-1>', self.selectRow)
            self.dataTable.rowheader.bind('<Button-3>', self.handleRightClick)

            self.dataTable.rowindexheader.bind('<1>', lambda e: None)

            self.dataTable.bind('<B1-Motion>', lambda e: None)
            self.dataTable.bind('<Button-1>', lambda e: None)
            self.dataTable.bind('<Control-Button-1>', lambda e: None)
            self.dataTable.bind('<Shift-Button-1>', lambda e: None)
            self.dataTable.bind('<Button-3>', self.handleRightClick) 
            self.dataTable.bind('<MouseWheel>', self.handleMouseWheel)
            self.dataTable.bind('<Configure>', self.handleResize)

            def set_yviews(*args):
                """Set the xview of table and row header"""

                self.dataTable.yview(*args)
                self.dataTable.rowheader.yview(*args)
                self.dataTable.currentrow = -1
                self.dataTable.currentcol = -1
                self.dataTable.redrawVisible()
                for c in self.dataTable.multiplecollist:
                    self.dataTable.tablecolheader.drawRect(c, delete=False)
                
                for r in self.dataTable.multiplerowlist:
                    self.dataTable.rowheader.drawRect(r, delete=False)
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)

            def set_xviews(*args):
                """Set the xview of table and col header"""

                self.dataTable.xview(*args)
                self.dataTable.tablecolheader.xview(*args)
                self.dataTable.currentrow = -1
                self.dataTable.currentcol = -1
                self.dataTable.redrawVisible()
                for c in self.dataTable.multiplecollist:
                    self.dataTable.tablecolheader.drawRect(c, delete=False)
                
                for r in self.dataTable.multiplerowlist:
                    self.dataTable.rowheader.drawRect(r, delete=False)
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)

            self.dataTable.Yscrollbar['command'] = set_yviews
            self.dataTable.Xscrollbar['command'] = set_xviews
            
            self.nextButton = ttk.Button(self.footer, text='Next', command=self.getInput)
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=lambda: self.closeImporter(2))

            self.cancelButton.pack(side=RIGHT)
            self.nextButton.pack(side=RIGHT)
        else:
            notification.create('error', 'Error opening file', 5000)

    def handleResize(self, event):
        self.dataTable.currentrow = -1
        self.dataTable.currentcol = -1
        self.dataTable.redrawVisible()
        for c in self.dataTable.multiplecollist:
            self.dataTable.tablecolheader.drawRect(c, delete=False)
                
        for r in self.dataTable.multiplerowlist:
            self.dataTable.rowheader.drawRect(r, delete=False)
        self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)

    def handleMouseWheel(self, event):
        """Handle mouse wheel scroll for windows"""

        if event.num == 5 or event.delta == -120:
            event.widget.yview_scroll(1, UNITS)
            self.dataTable.rowheader.yview_scroll(1, UNITS)
        if event.num == 4 or event.delta == 120:
            if self.dataTable.canvasy(0) < 0:
                return
            event.widget.yview_scroll(-1, UNITS)
            self.dataTable.rowheader.yview_scroll(-1, UNITS)
        
        self.dataTable.currentrow = -1
        self.dataTable.currentcol = -1
        self.dataTable.redrawVisible()
        for c in self.dataTable.multiplecollist:
            self.dataTable.tablecolheader.drawRect(c, delete=False)
                
        for r in self.dataTable.multiplerowlist:
            self.dataTable.rowheader.drawRect(r, delete=False)
        self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)

    def setMassSel(self):
        selMode = self.strVar.get()
        start = self.varStart.get()
        end = self.varEnd.get()
        self.deselectAll()

        if selMode == 'row':
            if start-1 < 0:
                self.notif.configure(text='Start row index out of range', background='red', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            elif end > self.dataTable.rows:
                self.notif.configure(text='End row index out of range', background='red', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            else:
                for i in range(start-1, end):
                    self.dataTable.multiplerowlist.append(i)
                    self.dataTable.rowheader.drawRect(row=i, delete=False)
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
        else: # cols
            if start < 0:
                self.notif.configure(text='Start column index out of range', background='red', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            elif end > self.dataTable.cols:
                self.notif.configure(text='End column index out of range', background='red', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            else:
                for i in range(start, end):
                    self.dataTable.multiplecollist.append(i)
                self.dataTable.multiplecollist.append(end)

                for c in self.dataTable.multiplecollist:
                    self.dataTable.drawSelectedCol(c, delete=False)
                    self.dataTable.tablecolheader.drawRect(c, delete=False)

        self.updateSelectionText()
    
    def handleListboxSelect(self, e):
        index = self.progressionList.curselection()[0]
        if index == 3 or index == 6 or index == 8:
            self.progressionList.selection_clear(index)
        else:
            self.nextStage(to=index)

    def handleColCtrlSelection(self,e):
        col = self.dataTable.get_col_clicked(e)
        if col not in self.dataTable.multiplecollist:
            self.dataTable.multiplecollist.append(col)
            # Select column
            self.dataTable.drawSelectedCol(col=col, delete=False)
            self.dataTable.tablecolheader.drawRect(col=col, delete=False)
        else:
            self.dataTable.delete('colrect')
            self.dataTable.tablecolheader.delete('rect')
            for i, c in enumerate(self.dataTable.multiplecollist):
                if c == col:
                    del self.dataTable.multiplecollist[i]
            
            for c in self.dataTable.multiplecollist:
                self.dataTable.drawSelectedCol(col=c, delete=False)
                self.dataTable.tablecolheader.drawRect(col=c, delete=False)
        self.updateSelectionText()

    def updateDragText(self):
        rows = self.dataTable.multiplerowlist
        cols = self.dataTable.multiplecollist
        self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]}-{cols[-1]}')

    def drawMultipleCells(self):
        """Draw an outline box for multiple cell selection"""

        self.dataTable.delete('currentrect')
        self.dataTable.delete('multicellrect')
        
        rows = self.dataTable.multiplerowlist
        cols = self.dataTable.multiplecollist

        if len(rows) == 0 or len(cols) == 0:
            return
        w=2
        x1,y1,a,b = self.dataTable.getCellCoords(rows[0],cols[0])
        c,d,x2,y2 = self.dataTable.getCellCoords(rows[len(rows)-1],cols[len(cols)-1])
        rect = self.dataTable.create_rectangle(
            x1+w/2,y1+w/2,x2,y2,
            outline=self.dataTable.boxoutlinecolor, 
            width=w,
            tag='multicellrect',
            fill=self.dataTable.rowselectedcolor
        )
        for r in rows:
            for c in cols:
                self.dataTable.lift('celltext'+str(c)+'_'+str(r))

    def handleColDrag(self, e):
        self.dataTable.multiplecollist = []
        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        colover = self.dataTable.get_col_clicked(e)
        startcol = self.dataTable.getSelectedColumn()

        if colover == None:
            return

        #do columns
        if colover > self.dataTable.cols or startcol > self.dataTable.cols:
            return
        else:
            self.dataTable.endcol = colover
            if self.dataTable.endcol < startcol:
                self.dataTable.multiplecollist=list(range(self.dataTable.endcol, startcol+1))
            else:
                self.dataTable.multiplecollist=list(range(startcol, self.dataTable.endcol+1))

        for i, c in enumerate(self.dataTable.multiplecollist):
            if i == 0:
                self.dataTable.drawSelectedCol(c)
                self.dataTable.tablecolheader.drawRect(c)
            else:
                self.dataTable.drawSelectedCol(c, delete=False)
                self.dataTable.tablecolheader.drawRect(c, delete=False)

        self.updateSelectionText()

    def handleRightClick(self, e = None):
        self.deselectAll()
        self.selectionText.configure(text='')
            
    def selectCol(self, e):
        self.dataTable.multiplecollist = []
        col = self.dataTable.get_col_clicked(e)
        self.deselectAll()

        # Select column
        self.dataTable.setSelectedCol( col )
        self.dataTable.drawSelectedCol( col=col )
        self.dataTable.tablecolheader.drawRect(col=col)

        self.updateSelectionText()

    def updateSelectionText(self):
        cols = self.dataTable.multiplecollist
        rows = self.dataTable.multiplerowlist

        if len(rows) > 0 and len(cols) == 0: # only rows selected
            if len(rows) > 1:
                temp = rows[0]
                for i, r in enumerate(rows):
                    if i != 0:
                        if r == temp+1:
                            self.selectionText.configure(text=f'Selected rows {rows[0]+1}-{rows[-1]+1}')
                        else:
                            text = 'Selected rows '
                            for i, r in enumerate(rows):
                                if i != len(rows)-1:
                                    text += f'{r+1}, '
                                else:
                                    text += f'{r+1}'

                            self.selectionText.configure(text=text)
                        temp = r
            else:
                self.selectionText.configure(text=f'Selected row {rows[0]+1}')

        elif len(cols) >= 1 and len(rows) == 0: # only cols selected
            if len(cols) > 1:
                temp = cols[0]
                for i, c in enumerate(cols):
                    if i != 0:
                        if c == temp+1:
                            self.selectionText.configure(text=f'Selected columns {cols[0]}-{cols[-1]}')
                        else:
                            text = 'Selected cols '
                            for i, c in enumerate(cols):
                                if i != len(cols)-1:
                                    text += f'{c}, '
                                else:
                                    text += f'{c}'

                            self.selectionText.configure(text=text)
                        temp = c
            else:
                self.selectionText.configure(text=f'Selected column {self.dataTable.multiplecollist[0]}')
        else:
            self.selectionText.configure(text=f'')

    def selectRow(self, e):
        self.dataTable.multiplecollist = []
        self.dataTable.tablecolheader.drawRect(-1)
        self.dataTable.delete('colrect')
        self.dataTable.tablecolheader.delete('rect')
        self.dataTable.delete('multicellrect')
        self.updateSelectionText()

    def checkDataForm(self):
        if len(self.dataTable.multiplecollist) > 1 and len(self.dataTable.multiplerowlist) > 1:

            if self.dataTable.multiplecollist[0] == self.dataTable.multiplecollist[1]:
                self.dataMode = 'long'
            elif self.dataTable.multiplerowlist[0] == self.dataTable.multiplerowlist[1]:
                self.dataMode = 'wide'

        elif len(self.dataTable.multiplecollist) > 1 or (len(self.dataTable.multiplecollist) == 0 and len(self.dataTable.getSelectedRows()) > 0):
            self.dataMode = 'wide'
        else:
            self.dataMode = 'long'

    def nextOptions(self, value):
        colList = self.dataTable.multiplecollist
        rowList = self.dataTable.multiplerowlist

        if len(colList) > 0: # Column selected
            if value == 0: # Single id
                self.dataMode = 'wide'
            else: # Multiple id
                self.dataMode = 'long'
        if len(rowList) > 0: # Row selected
            if value == 0: # Single id
                self.dataMode = 'long'
            else: # Multiple id
                self.dataMode = 'wide'

        self.options.destroy()

    def closeOptions(self):
        self.closedByClick = True
        self.options.destroy()

    def getInput(self):
        col = self.dataTable.getSelectedColumn()
        row = self.dataTable.getSelectedRow()
        rows = self.dataTable.getSelectedRows()
        colList = self.dataTable.multiplecollist
        rowList = self.dataTable.multiplerowlist
        self.colValues = []
        self.columnNames = []
        self.rowValues = []
        self.rowNames= []
        success = False
        self.closedByClick = False

        if self.stage == 0 and (len(colList) == 1 or len(rowList) == 1 or len(rows) == 1):
            def move(e):
                optionsX = int(self.window.winfo_rootx()) + int(self.window.winfo_width()* 0.5) - int(self.options.winfo_width() * 0.5)
                optionsY = int(self.window.winfo_rooty()) + int(self.window.winfo_height()* 0.5) - int(self.options.winfo_height() * 0.5)
                self.options.geometry("+%d+%d" % ( optionsX, optionsY ))
                self.options.lift()

            self.options = Toplevel(bg='#4eb1ff', borderwidth=5)
            self.options.overrideredirect(True)
            self.options.update_idletasks()
            
            optionsX = int(self.window.winfo_rootx()) + int(self.window.winfo_width()* 0.5) - int(self.options.winfo_width() * 0.5)
            optionsY = int(self.window.winfo_rooty()) + int(self.window.winfo_height()* 0.5) - int(self.options.winfo_height() * 0.5)
            self.options.geometry("+%d+%d" % ( optionsX, optionsY ))
            self.options.lift()

            self.options.bind('<Configure>', move)

            container = Frame(self.options, bd=0, padx=10, pady=10)
            container.pack()            
            var = IntVar()
            ttk.Label(container, text='Selection contains single ID or multiple IDs?').pack()
            ttk.Radiobutton(container, variable=var, value=0, text='Single ID').pack()
            ttk.Radiobutton(container, variable=var, value=1, text='Multiple IDs').pack()
            buttons = Frame(container, bd=0)
            buttons.pack(fill=X, expand=1)

            ttk.Button(buttons, text='OK', command=lambda: self.nextOptions(var.get())).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(buttons, text='Cancel', command=self.closeOptions).pack(side=LEFT, fill=X, expand=True)

            self.window.wait_window(self.options)

        for ri in range(len(rows)):
            temp = []
            for i in range(self.dataTable.cols):
                if str(rows.iloc[ri,i]) == 'nan':
                    temp.append(0)
                else:
                    temp.append(rows.iloc[ri,i])
            self.rowValues.append(temp)        
            self.rowNames.append(rows.iloc[ri,0])

        for i, c in enumerate(self.customGetSelectionValues()):
            self.colValues.append(c[0:])
            self.columnNames.append(c[0])

        if (len(rowList) < 1 and len(colList) < 1): # nothing selected
            self.notif.configure(background='red', foreground="white", text=f'Nothing selected')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
        elif self.closedByClick == True:
            pass
        else: # something selected
            if len(rowList) > 0: # rows selected
                if self.stage == 0: # ids
                    # Reset subjects if returned
                    self.tests = {}

                    if len(rows) > 1 and col == -1: # multiple rows
                        # print('USEAMPI RIVI')
                        if self.stage == 0: # ids
                            for i, id in enumerate(self.rowNames):
                                test = Test()
                                test.id = id
                                test.workLoads = []
                                self.tests[rows.index[i]] = test

                            self.dataMode = 'long'
                            success = True

                    else: # single rows
                        if self.stage == 0: #ids
                            if self.dataMode == None:
                                self.checkDataForm()
                            if self.dataMode == 'long':
                                for i, id in enumerate(self.rowNames):
                                    test = Test()
                                    test.id = id
                                    test.workLoads = []
                                    self.tests[rows.index[i]] = test

                            elif self.dataMode == 'wide':
                                for i, id in enumerate(self.rowValues[0]):
                                    if i != 0:
                                        test = Test()
                                        test.id = id
                                        test.workLoads = []
                                        self.tests[i] = test

                            success = True

                elif self.stage == 1: # Loads
                    success = self.getLoadsFromRows()

                elif self.stage == 2: #VO2
                    success = self.getRowValues('VO2')

                elif self.stage == 4: #HR
                    success = self.getRowValues('HR')

                elif self.stage == 5: #SV
                    success = self.getRowValues('SV')

                elif self.stage == 7: #Q
                    success = self.getRowValues('Q')

                elif self.stage == 9: #Hb
                    success = self.getRowValues('[Hb]')

                elif self.stage == 10: #SaO2
                    success = self.getRowValues('SaO2')

                elif self.stage == 11: #CaO2
                    success = self.getRowValues('CaO2')

                elif self.stage == 12: #CvO2
                    success = self.getRowValues('CvO2')

                elif self.stage == 13: #CavO2
                    success = self.getRowValues('C(a-v)O2')

                elif self.stage == 14: #QaO2
                    success = self.getRowValues('QaO2')

                elif self.stage == 15: #SvO2
                    success = self.getRowValues('SvO2')

                elif self.stage == 16: #PvO2
                    success = self.getRowValues('PvO2')
                        
                elif self.stage == 17: #T
                    success = self.getRowValues('T')

                elif self.stage == 18: #pH
                    success = self.getRowValues('pH')

                if success:
                    self.addCheckMark(self.stage)
                    self.notif.configure(text='OK', background='green', foreground='white')
                    self.notif.after(1000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    self.nextStage(imported=self.stage)

            if len(colList) > 0: # cols selected
                if self.stage == 0: #ids
                    if len(colList) > 1: # multiple columns
                        # Reset tests if returned
                        self.tests = {}
                                
                        for i, id in enumerate(self.columnNames):
                            # Create test, set its id and reset workloads
                            test = Test()
                            test.id = id
                            test.workLoads = []
                            colIndex = colList[i]
                            self.tests[colIndex] = test

                        success = True
                        self.dataMode = 'wide'

                    else: # one column
                        if self.dataMode == None:
                            self.checkDataForm()
                        if self.dataMode == 'long':
                            for i, c in enumerate(self.colValues): #iterate cols as list
                                for ci, cv in enumerate(c): #iterate values
                                    if ci != 0: #skip header
                                        # Create test, set its id and reset workloads
                                        test = Test()
                                        test.id = cv
                                        test.workLoads = []
                                        colIndex = colList[i]
                                        self.tests[ci] = test
                        else:
                            for i, id in enumerate(self.columnNames):
                                # Create test, set its id and reset workloads
                                test = Test()
                                test.id = id
                                test.workLoads = []
                                colIndex = colList[i]
                                self.tests[colIndex] = test

                        success = True
                        
                elif self.stage == 1: # Loads
                    success = self.getLoadsFromCols()

                elif self.stage == 2: #VO2
                    success = self.getColumnValues('VO2')

                elif self.stage == 4: #HR
                    success = self.getColumnValues('HR')

                elif self.stage == 5: #SV
                    success = self.getColumnValues('SV')

                elif self.stage == 7: #Q
                    success = self.getColumnValues('Q')

                elif self.stage == 9: #Hb
                    success = self.getColumnValues('[Hb]')

                elif self.stage == 10: #SaO2
                    success = self.getColumnValues('SaO2')

                elif self.stage == 11: #CaO2
                    success = self.getColumnValues('CaO2')

                elif self.stage == 12: #CvO2
                    success = self.getColumnValues('CvO2')

                elif self.stage == 13: #CavO2
                    success = self.getColumnValues('C(a-v)O2')

                elif self.stage == 14: #QaO2
                    success = self.getColumnValues('QaO2')

                elif self.stage == 15: #SvO2
                    success = self.getColumnValues('SvO2')

                elif self.stage == 16: #PvO2
                    success = self.getColumnValues('PvO2')
                        
                elif self.stage == 17: #T
                    success = self.getColumnValues('T')

                elif self.stage == 18: #pH
                    success = self.getColumnValues('pH')

                if success:
                    self.addCheckMark(self.stage)
                    self.notif.configure(text='OK', background='green', foreground='white')
                    self.notif.after(1000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    self.nextStage(imported=self.stage)

    def closeImporter(self, mode):
        if mode == 0:
            """ Done button clicked """
        
            for loadIndex, details in self.importedData.items():
                for iid, values in details.items():
                    for key, value in values.items():
                        if key != 'imported':
                            self.test.workLoads[int(loadIndex)].details.setValue(key, value)

            # Add project
            if self.newProject:
                app.sidepanel_projectList.addToList(self.project.id)
                app.addProject(self.project)
                app.setActiveProject(self.project)

            # Add subject
            if self.newSubject:
                app.sidepanel_subjectList.addToList(self.subject)
                app.sidepanel_subjectList.updateSelection()
                self.project.addSubject(self.subject)
                app.setActiveSubject(self.subject)

            app.projectDetailModule.refreshDetails()
            app.testDetailModule.refreshTestDetails()

        elif mode == 1:
            """ Template used """

            # Add project
            if self.newProject:
                app.sidepanel_projectList.addToList(self.project.id)
                app.addProject(self.project)
                app.setActiveProject(self.project)

            # Add subject
            if self.newSubject:
                app.sidepanel_subjectList.addToList(self.subject)
                app.sidepanel_subjectList.updateSelection()
                self.project.addSubject(self.subject)
                app.setActiveSubject(self.subject)

            # Add test
            for t in self.testList:
                app.sidepanel_testList.addToList(t.id)
                self.subject.addTest(t)

            app.projectDetailModule.refreshDetails()
            app.testDetailModule.refreshTestDetails()

        try:
            self.window.destroy()
            self.options.destroy()
        except:
            pass

    def updateTable(self, table):
        self.dataTable.updateModel(TableModel(self.dfList[table]))
        self.dataTable.redraw()

    def deselectAll(self):
        self.dataTable.clearSelected()
        self.dataTable.multiplecollist = []
        self.dataTable.multiplerowlist = []
        self.dataTable.drawSelectedCol(-1)
        self.dataTable.tablecolheader.drawRect(-1)

        self.dataTable.rowheader.clearSelected()
        self.dataTable.delete('ctrlSel')
        self.dataTable.delete('currentrect')
        self.dataTable.delete('multicellrect')
        self.dataTable.delete('colrect')
        self.dataTable.delete('rowrect')
        self.dataTable.tablecolheader.delete('rect')
        self.updateSelectionText()

    def customGetSelectionValues(self):
        # Get values for current multiple cell selection
        rows = range(self.dataTable.rows)
        cols = self.dataTable.multiplecollist
        model = self.dataTable.model
        lists = []

        for c in cols:
            x=[]
            for r in rows:
                val = model.getValueAt(r,c)
                if val == '' or val == None:
                    x.append(0)
                else:
                    x.append(val)
            lists.append(x)
        return lists
    
    def getLoadsFromCols(self):
        if len(self.tests.items()) > 0:
            for rowIndex, t in self.tests.items():
                t.workLoads = [] # delete previous workloads, if re-fetching loads

                for i, v in enumerate(self.colValues): #iterate cols as list
                    for ci, cv in enumerate(v): #iterate values
                        if ci == rowIndex: #if row matches subject's row
                            columnName = self.columnNames[i]
                            load = t.createLoad()
                            load.setName(columnName) # column name
                            load.getDetails().setValue('Load', cv) # set value
                            load.getDetails().setImported(True)
                            continue
            
            return True
        else:
            self.notif.configure(text=f'No ID(s) detected. Please define ID(s) before loads.', background='red', foreground='white')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))

    def getLoadsFromRows(self):
        if len(self.tests.items()) > 0:
            for colIndex, t in self.tests.items():
                t.workLoads = [] # delete previous workloads, if re-fetching loads

                for i, v in enumerate(self.rowValues): #iterate rows as list
                    for ci, cv in enumerate(v): #iterate values
                        if ci == colIndex: #if col matches tests's col
                            rowName = self.rowNames[i]
                            load = t.createLoad()
                            load.setName(rowName) # row name
                            load.getDetails().setValue('Load', cv) # set value
                            load.getDetails().setImported(True)
                            continue

            return True
        else:
            self.notif.configure(text=f'No ID(s) detected. Please define ID(s) before loads.', background='red', foreground='white')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))

    def getColumnValues(self, label):
        flag = False

        if len(self.tests.items()) > 0:
            for rowIndex, t in self.tests.items():
                loads = t.getWorkLoads()
                
                if len(loads) == 0:
                    self.notif.configure(text=f'No loads detected. Please define loads before other values.', background='red', foreground='white')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    break
                elif len(self.colValues) < len(loads) and len(self.colValues) != 1:
                    self.notif.configure(text=f'You have imported {len(loads)} loads but only {len(self.colValues)} values given', background='red', foreground='white')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    break
                else:
                    if len(self.colValues) == 1:
                        for li, l in enumerate(loads):
                            details = l.getDetails()
                            value = self.colValues[0][rowIndex]
                            details.setValue(label, value)
                    else:
                        for li, l in enumerate(loads):
                            details = l.getDetails()
                            value = self.colValues[li][rowIndex]
                            details.setValue(label, value)
                    flag = True
            return flag
        else:
            self.notif.configure(text=f'No ID(s) detected. Please define ID(s) before other values.', background='red', foreground='white')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))

    def getRowValues(self, label):
        flag = False

        if len(self.tests.items()) > 0:
            for colIndex, t in self.tests.items():
                loads = t.getWorkLoads()

                if len(loads) == 0:
                    self.notif.configure(text=f'No loads detected. Please define loads before other values.', background='red', foreground='white')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    break
                elif len(self.rowValues) < len(loads) and len(self.rowValues) != 1:
                    self.notif.configure(text=f'You have imported {len(loads)} loads but only {len(self.rowValues)} values given', background='red', foreground='white')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    break
                else:
                    if len(self.rowValues) == 1:
                        for li, l in enumerate(loads):
                            details = l.getDetails()
                            value = self.rowValues[0][colIndex]
                            details.setValue(label, value)
                    else:
                        for li, l in enumerate(loads):
                            details = l.getDetails()
                            value = self.rowValues[li][colIndex]
                            details.setValue(label, value)
                    flag = True
            return flag
        else:
            self.notif.configure(text=f'No ID(s) detected. Please define ID(s) before other values.', background='red', foreground='white')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))

    def prevStage(self):
        self.deselectAll()
        to = self.stage - 1
        self.nextStage(to=to)

    def nextStage(self, to=None, imported=None, skipped=None):
        if imported != None:
            self.imported[imported] = True

        if to == None:
            to = self.stage + 1

        if to > 0:
            # Reset buttons
            self.nextButton.pack_forget()
            self.cancelButton.pack_forget()
            try:
                self.passBtn.pack_forget()
                self.doneBtn.pack_forget()
                self.prevBtn.pack_forget()
            except:
                pass

            # Pack in reversed order
            self.cancelButton.pack(side=RIGHT)
            self.doneBtn = ttk.Button(self.footer, text='Done', command=self.importData)
            self.doneBtn.pack(side=RIGHT)
            self.prevBtn = ttk.Button(self.footer, text='Prev', command=self.prevStage)
            self.prevBtn.pack(side=RIGHT)
            self.passBtn = ttk.Button(self.footer, text='Skip', command=lambda: self.nextStage(skipped=self.stage))
            self.passBtn.pack(side=RIGHT)
            self.nextButton.pack(side=RIGHT)
            
        if skipped == 17 or skipped == 18:
            self.addLinearDist = True

        self.deselectAll()

        # Reset mass selection tool entries
        self.varStart.set(0)
        self.varEnd.set(0)

        # Skip horizontal lines
        if to == 3 or to == 6 or to == 8:
            to += 1

        if to == 0:
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column/row containing test ID(s)')
        elif to == 1:
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing load(s)')
        elif to == 2: # -> VO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for VO\u2082')
        elif to== 4: # -> HR
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for HR')
        elif to == 5: # -> SV
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for SV')
        elif to == 7: # -> Q
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for Q')
        elif to == 9: # -> Hb
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for [Hb]')
        elif to == 10: # -> SaO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for SaO\u2082')
        elif to == 11: # -> CaO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for CaO\u2082')
        elif to == 12: # -> CvO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for CvO\u2082')
        elif to == 13: # -> CavO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for C(a-v)O\u2082')
        elif to == 14: # -> QaO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for QaO\u2082')
        elif to == 15: # -> SvO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for SvO\u2082')
        elif to == 16: # -> PvO2
            self.moveArrow(self.stage, to=to)
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for PvO\u2082')
        elif to == 17: # -> T
            self.moveArrow(self.stage, to=to)
            self.passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for T')
        elif to == 18: # -> pH
            self.moveArrow(self.stage, to=to)
            self.passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define column(s)/row(s) containing value(s) for pH')
        elif to == 19: # Finish
            if askokcancel('Quit data import?', 'Have you imported everything?', parent=self.window):
                if len(self.tests.items()) > 0:
                    self.importData()
                else:
                    self.notif.configure(text=f'No ID(s) detected. Please define ID(s) before other values.', background='red', foreground='white')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                    to = 18
            else:
                to = 18

        self.stage = to

    def moveArrow(self, from_, to):
        value = self.progressionList.get(from_)
        if '\U0001F878' in value:
            value = value.replace('\U0001F878','')
            value = value.strip()
        self.progressionList.delete(from_)
        self.progressionList.insert(from_, value)

        value = self.progressionList.get(to)
        if '\U0001F878' not in value:
            value = f'{value} \U0001F878'
        self.progressionList.delete(to)
        self.progressionList.insert(to, value)

    def addCheckMark(self, to):
        value = self.progressionList.get(to)
        if '\u2713' not in value:
            value = f'{value} \u2713'
        self.progressionList.delete(to)
        self.progressionList.insert(to, value)

    def importData(self):
        # Create a project if none set as active project
        if app.activeProject == None:
            project = Project()
            app.activeProject = project
            app.addProject(project)
        else:
            project = app.activeProject

        app.activeSubject = self.subject
        app.setActiveTest(None)

        for t in self.tests.values():
            self.subject.addTest(t)
        
        # Update app state
        app.sidepanel_projectList.refreshList(index=len(app.projects)-1)
        app.sidepanel_subjectList.refreshList(index=len(project.subjects)-1)
        app.sidepanel_testList.refreshList()
        app.projectDetailModule.refreshDetails()

        # If pH and T are not imported, distribute defaults linearly
        # (in case user is done importing before pH and T)
        if self.imported[17] == False:
            for s in project.subjects:
                for t in s.tests:
                    self.addLinearDistT(t)

        if self.imported[18] == False:
            for s in project.subjects:
                for t in s.tests:
                    self.addLinearDistPH(t)

        self.window.destroy()
        del self

    def addLinearDistPH(self, test):
        pHrest = float(app.settings.testDefaults['pH @ rest'])
        pHpeak = float(app.settings.testDefaults['pH\u209A\u2091\u2090\u2096'])
        pHDif = float(pHrest) - float(pHpeak)

        # Filter possible empty loads
        nFilteredLoads = 0
        filteredLoads = []
        for i, l in enumerate(test.workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
                        
            if i == 0 or detailsDict['Load'] != 0:
                nFilteredLoads += 1
                filteredLoads.append(l)

        if nFilteredLoads > 1:
            if pHrest != pHpeak:
                test.getWorkLoads()[-1].getDetails().setValue('pH', pHpeak)

            pHstep = pHDif / (nFilteredLoads-1)
        else:
            pHstep = 0
        
        # Add linear distribution
        for i, w in enumerate(filteredLoads):
            details = w.getDetails()
            pHValue = pHrest - (i * pHstep)
            details.setValue('pH', f'{"{0:.2f}".format(pHValue)}')
    
    def addLinearDistT(self, test):
        Trest = float(app.settings.testDefaults['Tc @ rest'])
        Tpeak = float(app.settings.testDefaults['Tc\u209A\u2091\u2090\u2096'])
        Tdif = float(Tpeak) - float(Trest)

        # Filter possible empty loads
        nFilteredLoads = 0
        filteredLoads = []
        for i, l in enumerate(test.workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
                        
            if i == 0 or detailsDict['Load'] != 0:
                nFilteredLoads += 1
                filteredLoads.append(l)

        if nFilteredLoads > 1:
            if Trest != Tpeak:
                test.getWorkLoads()[-1].getDetails().setValue('T', Tpeak)

            Tstep = Tdif / (nFilteredLoads-1)
        else:
            Tstep = 0

        # Add linear distribution
        for i, w in enumerate(filteredLoads):
            details = w.getDetails()

            Tvalue = Trest + (i * Tstep)
            details.setValue('T', f'{"{0:.1f}".format(Tvalue)}')

class DataMenuElem(object):
    def __init__(self, importer, menu, menuButton, option, isExporter = False):
        self.importer = importer
        self.menuButton = menuButton
        self.option = option
        self.isExporter = isExporter
        menu.add_command(label=option, command=lambda: self.handleMenuSelect())

    def handleMenuSelect(self):
        self.menuButton.config(text=self.option)
        if self.isExporter == False:
            self.importer.updateTable(self.option)