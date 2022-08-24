import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.messagebox import askokcancel
from pandastable import Table, TableModel, util
from objects.project import Project
from objects.subject import Subject
from objects.test import Test
from objects.app import app
from modules.notification import notification

##
# This class is used to import data for a single test.
# The class is initialized from the menubar (menubar.py) or from the 
# sidepanel's testlist (sidepanel_testList.py)
##

class TestDataImporter():
    def __init__(self, test=None):
        self.importedData = {}
        self.newProject = False
        self.newSubject = False
        self.newTest = False
        self.testList = []

        # Create a project if any project is not set active
        if app.activeProject == None:
            self.project = Project()
            self.newProject = True
        else:
            self.project = app.activeProject

        # Create a subject if any subject is not set active
        if app.activeSubject == None:
            self.subject = Subject(0, parentProject=self.project)
            self.newSubject = True
        else:
            self.subject = app.activeSubject

        if test == None:
            # Create a test if none is set active
            testId = f'{self.subject.id}-Test-{len(self.subject.getTests())+1}'
            self.test = Test(id=testId, parentSubject=self.subject)
            self.newTest = True
        else:
            self.test = test

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

            if self.newTest == True:
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
                    if sheet.loc[0,0] == 'Test-template':
                        self.cols = []

                        testId = f'{self.subject.id}-Test-{len(self.subject.getTests())+1}'
                        self.test = Test(id=testId, parentSubject=self.subject)
                        self.testList.append(self.test)

                        self.test.workLoads = []
                        self.test.id = self.dfList[sheetName].loc[2,1]

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
            self.window.title('Test import')
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
            self.treeView = ttk.Treeview(self.leftPanel, selectmode='browse')

            # Create initial treeview
            for i, l in enumerate(self.test.workLoads):
                treeId = 0
                if i == 0:
                    self.treeView.insert('', END, text=l.name, iid=i, open=True)
                else:
                    self.treeView.insert('', END, text=l.name, iid=i, open=False)

                self.treeView.insert('', END, text='VO\u2082 *', iid=f'{i}{treeId}', open=False)
                self.treeView.move(f'{i}{treeId}', i, treeId)

                self.treeView.insert('', END, text='\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+1}', open=False, tags='hrLine')
                self.treeView.move(f'{i}{treeId+1}', i, treeId+1)

                self.treeView.insert('', END, text='HR *', iid=f'{i}{treeId+2}', open=False)
                self.treeView.move(f'{i}{treeId+2}', i, treeId+2)

                self.treeView.insert('', END, text='SV *', iid=f'{i}{treeId+3}', open=False)
                self.treeView.move(f'{i}{treeId+3}', i, treeId+3)

                self.treeView.insert('', END, text='\u2015 or \u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+4}', open=False, tags='hrLine')
                self.treeView.move(f'{i}{treeId+4}', i, treeId+4)

                self.treeView.insert('', END, text='Q *', iid=f'{i}{treeId+5}', open=False)
                self.treeView.move(f'{i}{treeId+5}', i, treeId+5)

                self.treeView.insert('', END, text='\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+6}', open=False, tags='hrLine')
                self.treeView.move(f'{i}{treeId+6}', i, treeId+6)

                self.treeView.insert('', END, text='[Hb] *', iid=f'{i}{treeId+7}', open=False)
                self.treeView.move(f'{i}{treeId+7}', i, treeId+7)

                self.treeView.insert('', END, text='SaO\u2082 *', iid=f'{i}{treeId+8}', open=False)
                self.treeView.move(f'{i}{treeId+8}', i, treeId+8)

                self.treeView.insert('', END, text='CaO\u2082', iid=f'{i}{treeId+9}', open=False)
                self.treeView.move(f'{i}{treeId+9}', i, treeId+9)

                self.treeView.insert('', END, text='CvO\u2082', iid=f'{i}{treeId+10}', open=False)
                self.treeView.move(f'{i}{treeId+10}', i, treeId+10)

                self.treeView.insert('', END, text='C(a-v)O\u2082', iid=f'{i}{treeId+11}', open=False)
                self.treeView.move(f'{i}{treeId+11}', i, treeId+11)

                self.treeView.insert('', END, text='QaO\u2082', iid=f'{i}{treeId+12}', open=False)
                self.treeView.move(f'{i}{treeId+12}', i, treeId+12)

                self.treeView.insert('', END, text='SvO\u2082', iid=f'{i}{treeId+13}', open=False)
                self.treeView.move(f'{i}{treeId+13}', i, treeId+13)

                self.treeView.insert('', END, text='PvO\u2082', iid=f'{i}{treeId+14}', open=False)
                self.treeView.move(f'{i}{treeId+14}', i, treeId+14)

                self.treeView.insert('', END, text='T', iid=f'{i}{treeId+15}', open=False)
                self.treeView.move(f'{i}{treeId+15}', i, treeId+15)

                self.treeView.insert('', END, text='pH', iid=f'{i}{treeId+16}', open=False)
                self.treeView.move(f'{i}{treeId+16}', i, treeId+16)

            self.treeView.pack(fill=Y, expand=True)
            self.treeView.selection_set(('00'))

            # Add / Delete load buttons
            buttonWrap = ttk.Frame(self.leftPanel)
            buttonWrap.pack(side=BOTTOM, fill=X)
            ttk.Button(buttonWrap, text='Add load', command=self.addLoadToTree).pack(side=LEFT, fill=X, expand=True)
            ttk.Button(buttonWrap, text='Delete load', command=self.deleteLoadFromTree).pack(side=LEFT, fill=X, expand=True)

            self.yScroll['command'] = self.treeView.yview

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
            self.instructionText = ttk.Label(headerFrame, text='Define cell(s) containing value(s) for VO\u2082 on 1. load.')
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

            # Footer information
            self.infoWrap = ttk.Frame(self.footer)
            self.infoWrap.pack(side=LEFT)

            self.selectionText = ttk.Label(self.infoWrap, text='')
            self.selectionText.pack(anchor='w')
            self.meanText = ttk.Label(self.infoWrap, text='')
            self.meanText.pack(anchor='w')
            self.nCellsText = ttk.Label(self.infoWrap, text='')
            self.nCellsText.pack(anchor='w')

            nameOfFirstSheet = list(self.dfList)[0]
            self.dataTable = Table(dataFrame, dataframe=self.dfList[nameOfFirstSheet], editable=False)
            self.dataTable.show()

            # Clear initial selection
            self.dataTable.clearSelected()
            self.dataTable.rowheader.clearSelected()

            # Override original bindings
            self.dataTable.tablecolheader.bind('<1>', self.handle_col_left_click)
            self.dataTable.tablecolheader.bind('<Double-Button-1>', self.collapseCol)
            self.dataTable.tablecolheader.bind('<Control-Button-1>', self.handle_col_ctrl_click)
            self.dataTable.tablecolheader.bind('<Shift-Button-1>', self.handle_col_drag)
            self.dataTable.tablecolheader.bind('<B1-Motion>', self.handle_col_drag)
            self.dataTable.tablecolheader.bind('<Button-3>', self.handleRightClick)

            self.dataTable.rowheader.bind('<1>', self.selectRow)
            self.dataTable.rowheader.bind('<B1-Motion>', self.handle_row_drag)
            self.dataTable.rowheader.bind('<Control-Button-1>', self.handle_row_left_ctrl_click)
            self.dataTable.rowheader.bind('<Shift-Button-1>', self.handle_row_left_shift_click)
            self.dataTable.rowheader.bind('<Button-3>', self.handleRightClick)

            self.dataTable.rowindexheader.bind('<1>', lambda e: None)

            self.dataTable.bind('<1>', self.handle_left_click)
            self.dataTable.bind('<B1-Motion>', self.handle_table_mouse_drag)
            self.dataTable.bind('<Control-Button-1>', lambda e: None)
            self.dataTable.bind('<Shift-Button-1>', lambda e: None)
            self.dataTable.bind('<Button-3>', self.handleRightClick)
            self.dataTable.bind('<MouseWheel>', self.handleMouseWheel)
            self.dataTable.bind('<Configure>', self.handleResize)

            self.treeView.bind('<<TreeviewSelect>>', self.updateInstructions)

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
            self.doneButton = ttk.Button(self.footer, text='Done', command=lambda: self.closeImporter(0))
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=lambda: self.closeImporter(2))

            self.cancelButton.pack(side=RIGHT, anchor='s')
            self.doneButton.pack(side=RIGHT, anchor='s')
            self.nextButton.pack(side=RIGHT, anchor='s')

        else:
            notification.create('error', 'Error opening file', 5000)

    def handle_left_click(self, event):
        """Respond to a single press"""

        self.dataTable.clearSelected()
        self.dataTable.allrows = False
        #which row and column is the click inside?
        rowclicked = self.dataTable.get_row_clicked(event)
        colclicked = self.dataTable.get_col_clicked(event)
        if colclicked == None:
            return
        self.dataTable.focus_set()

        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        #ensure popup menus are removed if present
        if hasattr(self, 'rightmenu'):
            self.dataTable.rightmenu.destroy()
        if hasattr(self.dataTable.tablecolheader, 'rightmenu'):
            self.dataTable.tablecolheader.rightmenu.destroy()

        self.dataTable.startrow = rowclicked
        self.dataTable.endrow = rowclicked
        self.dataTable.startcol = colclicked
        self.dataTable.endcol = colclicked
        #reset multiple selection list
        self.dataTable.multiplerowlist=[]
        self.dataTable.multiplerowlist.append(rowclicked)
        if 0 <= rowclicked < self.dataTable.rows and 0 <= colclicked < self.dataTable.cols:
            self.dataTable.setSelectedRow(rowclicked)
            self.dataTable.setSelectedCol(colclicked)
            self.dataTable.drawSelectedRect(self.dataTable.currentrow, self.dataTable.currentcol)
            self.dataTable.drawSelectedRow()
            self.dataTable.rowheader.drawSelectedRows(rowclicked)
            self.dataTable.tablecolheader.delete('rect')
            
        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()

        self.updateSelectionText()
    
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

    def handle_table_shift_click(self, event):
        self.handle_table_mouse_drag(event)

    def handle_table_mouse_drag(self, event):
        """Handle mouse moved with button held down, multiple selections"""

        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        rowover = self.dataTable.get_row_clicked(event)
        colover = self.dataTable.get_col_clicked(event)
        if colover == None or rowover == None:
            return

        if rowover >= self.dataTable.rows or self.dataTable.startrow > self.dataTable.rows:
            return
        else:
            self.dataTable.endrow = rowover
        #do columns
        if colover > self.dataTable.cols or self.dataTable.startcol > self.dataTable.cols:
            return
        else:
            self.dataTable.endcol = colover
            if self.dataTable.endcol < self.dataTable.startcol:
                # Prevent choosing cells on multiple columns
                if len(self.dataTable.multiplerowlist) < 2:
                    self.dataTable.multiplecollist=list(range(self.dataTable.endcol, self.dataTable.startcol+1))
            else:
                if len(self.dataTable.multiplerowlist) < 2:
                    self.dataTable.multiplecollist=list(range(self.dataTable.startcol, self.dataTable.endcol+1))

        #draw the selected rows
        if self.dataTable.endrow != self.dataTable.startrow:
            if self.dataTable.endrow < self.dataTable.startrow:
                if len(self.dataTable.multiplecollist) < 2:
                    self.dataTable.multiplerowlist=list(range(self.dataTable.endrow, self.dataTable.startrow+1))
            else:
                if len(self.dataTable.multiplecollist) < 2:
                    self.dataTable.multiplerowlist=list(range(self.dataTable.startrow, self.dataTable.endrow+1))
            self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
            self.dataTable.rowheader.drawSelectedRows(self.dataTable.multiplerowlist)
            self.dataTable.drawMultipleCells()
        else:
            self.dataTable.multiplerowlist = []
            self.dataTable.multiplerowlist.append(self.dataTable.currentrow)
            if len(self.dataTable.multiplecollist) >= 1:
                self.dataTable.drawMultipleCells()
            self.dataTable.delete('multiplesel')
        
        self.updateSelectionText()

    def handle_col_left_click(self,event):
        """Does cell selection when left mouse button is clicked"""

        self.dataTable.tablecolheader.delete('rect')
        self.dataTable.delete('entry')
        self.dataTable.delete('multicellrect')
        colclicked = self.dataTable.get_col_clicked(event)
        if colclicked == None:
            return
        #set all rows for plotting if no multi selection
        if len(self.dataTable.multiplerowlist) <= 1:
            self.dataTable.allrows = True

        self.dataTable.setSelectedCol(colclicked)
        if self.dataTable.tablecolheader.atdivider == 1:
            return
        self.dataTable.tablecolheader.drawRect(self.dataTable.currentcol)
        self.dataTable.tablecolheader.draggedcol = None
        #finally, draw the selected col on the table
        self.dataTable.drawSelectedCol()
        self.dataTable.drawMultipleCells()
        self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
        
        self.updateSelectionText()

    def selectRow(self, event):
        """Handle left click"""

        rowclicked = self.dataTable.get_row_clicked(event)
        self.startrow = rowclicked
        if 0 <= rowclicked < self.dataTable.rows:
            self.dataTable.rowheader.delete('rect')
            self.dataTable.delete('entry')
            self.dataTable.delete('multicellrect')
            #set row selected
            self.dataTable.setSelectedRow(rowclicked)
            self.dataTable.drawSelectedRow()
            self.dataTable.rowheader.drawSelectedRows(self.dataTable.currentrow)
        
            self.dataTable.drawMultipleCells()

        self.updateSelectionText()

    def handle_row_left_shift_click(self, event):
        """Handle shift click"""
        if len(self.dataTable.multiplecollist) < 2:
            if self.dataTable.startrow == None:
                self.dataTable.startrow = self.dataTable.currentrow
            self.handle_row_drag(event)
        
        self.updateSelectionText()

    def handle_row_left_ctrl_click(self, event):
        """Handle ctrl clicks - for multiple row selections"""

        if len(self.dataTable.multiplecollist) < 2:
            rowclicked = self.dataTable.get_row_clicked(event)
            if 0 <= rowclicked < self.dataTable.rows:
                if rowclicked not in self.dataTable.multiplerowlist:
                    self.dataTable.multiplerowlist.append(rowclicked)
                else:
                    self.dataTable.multiplerowlist.remove(rowclicked)
                    self.dataTable.rowheader.drawRect(row=rowclicked, delete=True)
                    self.dataTable.delete('rect')
                    self.dataTable.delete('rowrect') 
                
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
                self.dataTable.rowheader.drawSelectedRows(self.dataTable.multiplerowlist)

        self.dataTable.multiplerowlist.sort()
        self.dataTable.drawMultipleCells()
        self.updateSelectionText()

    def handle_row_drag(self, event):
        """Handle mouse moved with button held down, multiple selections"""

        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        rowover = self.dataTable.get_row_clicked(event)
        colover = self.dataTable.get_col_clicked(event)
        if rowover == None:
            return
        if rowover >= self.dataTable.rows or self.dataTable.startrow > self.dataTable.rows:
            return
        else:
            self.endrow = rowover

        if len(self.dataTable.multiplecollist) < 2:
            #draw the selected rows
            if self.endrow != self.dataTable.startrow:
                if self.endrow < self.dataTable.startrow:
                    rowlist=list(range(self.endrow, self.dataTable.startrow+1))
                else:
                    rowlist=list(range(self.dataTable.startrow, self.endrow+1))
                self.dataTable.rowheader.drawSelectedRows(rowlist)
                self.dataTable.multiplerowlist = rowlist
                self.dataTable.drawMultipleRows(rowlist)
                self.dataTable.drawMultipleCells()
                self.dataTable.allrows = False
            else:
                self.dataTable.multiplerowlist = []
                self.dataTable.multiplerowlist.append(rowover)
                self.dataTable.rowheader.drawSelectedRows(rowover)
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
        else:
            self.dataTable.setSelectedRow(rowover)
            self.dataTable.rowheader.drawSelectedRows(rowover)
            self.dataTable.drawSelectedRow()
            self.dataTable.drawMultipleCells()
        
        self.updateSelectionText()

    def handle_col_ctrl_click(self,e):
        col = self.dataTable.get_col_clicked(e)

        if len(self.dataTable.multiplerowlist) > 1:
            self.dataTable.setSelectedCol(col)
        else:
            if col not in self.dataTable.multiplecollist:
                self.dataTable.multiplecollist.append(col)
                # Select column
                self.dataTable.drawSelectedCol(col=col, delete=False)
                self.dataTable.tablecolheader.drawRect(col=col, delete=False)
        
        self.updateSelectionText()

    def handle_col_drag(self, e):
        self.dataTable.tablecolheader.delete('dragrect')
        # self.dataTable.multiplecollist = []
        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        colover = self.dataTable.get_col_clicked(e)
        startcol = self.dataTable.getSelectedColumn()

        if colover == None:
            return

        # Draw resize line
        x=int(self.dataTable.tablecolheader.canvasx(e.x))
        if self.dataTable.tablecolheader.atdivider == 1:
            self.dataTable.delete('resizeline')
            self.dataTable.tablecolheader.delete('resizeline')
            self.dataTable.create_line(x, 0, x, self.dataTable.rowheight*self.dataTable.rows,
                                width=2, fill='gray', tag='resizeline')
            self.dataTable.tablecolheader.create_line(x, 0, x, self.dataTable.tablecolheader.height,
                                width=2, fill='gray', tag='resizeline')

        if len(self.dataTable.multiplerowlist) < 2:
            # Do columns
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
        else:
            self.dataTable.setSelectedCol(startcol)
        
        self.dataTable.drawMultipleCells()
        self.updateSelectionText()

    def updateInstructions(self, event):
        try:
            iid = self.treeView.selection()[0]
            index = self.treeView.index(self.treeView.selection()[0])

            if len(iid) > 1 and (index == 1 or index == 4 or index == 6):
                self.instructionText.configure(text='')
                self.treeView.selection_remove(self.treeView.selection()[0])
                return
            if len(self.treeView.selection()[0]) > 1:
                text =  self.treeView.item(self.treeView.selection()[0])['text']
                text = text.split(' ')[0]
                self.instructionText.configure(text=f'Define cell(s) containing value(s) for {text} on {int(self.treeView.selection()[0][0])+1}. load.')
            else:
                self.instructionText.configure(text='')
        except IndexError:
            pass

    def collapseCol(self, event):
        col = self.dataTable.get_col_clicked(event)
        colName = self.dataTable.model.getColumnName(col)
        colWidth = self.dataTable.columnwidths[colName]
        if colWidth <= 50:
            l = self.dataTable.model.getlongestEntry(col)
            txt = ''.join(['X' for i in range(l+1)])
            tw,tl = util.getTextLength(txt, self.dataTable.maxcellwidth, font=self.dataTable.thefont)
            self.dataTable.columnwidths[colName] = tw
        else:
            self.dataTable.columnwidths[colName] = 50
        
        self.dataTable.redraw()
        
    def addLoadToTree(self):
        load = self.test.createLoad()
        load.details.isImported = True
        self.updateTreeview()

    def deleteLoadFromTree(self):
        if askokcancel('Delete load', 'Are you sure you want to delete the load?', parent=self.window):
            tindex = int(self.treeView.selection()[0])
            if not self.treeView.parent(tindex):
                self.test.removeLoad(tindex)
                self.updateTreeview()

    def updateTreeview(self):
        # Clear treeview
        for i in range(len(self.treeView.get_children())):
            try:
                self.treeView.delete(i)
            except:
                pass
        
        # Create treeview
        for i, l in enumerate(self.test.workLoads):
            treeId = 0
            if i == 0:
                self.treeView.insert('', END, text=l.name, iid=i, open=True)
            else:
                self.treeView.insert('', END, text=l.name, iid=i, open=False)
            self.treeView.insert('', END, text='VO\u2082 *', iid=f'{i}{treeId}', open=False)
            self.treeView.move(f'{i}{treeId}', i, treeId)

            self.treeView.insert('', END, text='\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+1}', open=False)
            self.treeView.move(f'{i}{treeId+1}', i, treeId+1)

            self.treeView.insert('', END, text='HR *', iid=f'{i}{treeId+2}', open=False)
            self.treeView.move(f'{i}{treeId+2}', i, treeId+2)

            self.treeView.insert('', END, text='SV *', iid=f'{i}{treeId+3}', open=False)
            self.treeView.move(f'{i}{treeId+3}', i, treeId+3)

            self.treeView.insert('', END, text='\u2015 or \u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+4}', open=False)
            self.treeView.move(f'{i}{treeId+4}', i, treeId+4)

            self.treeView.insert('', END, text='Q *', iid=f'{i}{treeId+5}', open=False)
            self.treeView.move(f'{i}{treeId+5}', i, treeId+5)

            self.treeView.insert('', END, text='\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015', iid=f'{i}{treeId+6}', open=False)
            self.treeView.move(f'{i}{treeId+6}', i, treeId+6)

            self.treeView.insert('', END, text='[Hb] *', iid=f'{i}{treeId+7}', open=False)
            self.treeView.move(f'{i}{treeId+7}', i, treeId+7)

            self.treeView.insert('', END, text='SaO\u2082 *', iid=f'{i}{treeId+8}', open=False)
            self.treeView.move(f'{i}{treeId+8}', i, treeId+8)

            self.treeView.insert('', END, text='CaO\u2082', iid=f'{i}{treeId+9}', open=False)
            self.treeView.move(f'{i}{treeId+9}', i, treeId+9)

            self.treeView.insert('', END, text='CvO\u2082', iid=f'{i}{treeId+10}', open=False)
            self.treeView.move(f'{i}{treeId+10}', i, treeId+10)

            self.treeView.insert('', END, text='C(a-v)O\u2082', iid=f'{i}{treeId+11}', open=False)
            self.treeView.move(f'{i}{treeId+11}', i, treeId+11)

            self.treeView.insert('', END, text='QaO\u2082', iid=f'{i}{treeId+12}', open=False)
            self.treeView.move(f'{i}{treeId+12}', i, treeId+12)

            self.treeView.insert('', END, text='SvO\u2082', iid=f'{i}{treeId+13}', open=False)
            self.treeView.move(f'{i}{treeId+13}', i, treeId+13)

            self.treeView.insert('', END, text='PvO\u2082', iid=f'{i}{treeId+14}', open=False)
            self.treeView.move(f'{i}{treeId+14}', i, treeId+14)

            self.treeView.insert('', END, text='T', iid=f'{i}{treeId+15}', open=False)
            self.treeView.move(f'{i}{treeId+15}', i, treeId+15)

            self.treeView.insert('', END, text='pH', iid=f'{i}{treeId+16}', open=False)
            self.treeView.move(f'{i}{treeId+16}', i, treeId+16)

    def updateTable(self, table):
        self.dataTable.updateModel(TableModel(self.dfList[table]))
        self.dataTable.redraw()

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

    def handleRightClick(self, e = None):
        self.deselectAll()
        self.selectionText.configure(text='')

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
        self.updateMeanText()

    def updateSelectionText(self, e=None):
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
            if len(cols) > 1:
                tempC = cols[0]
                for i, c in enumerate(cols):
                    if i != 0:
                        if c == tempC+1:
                            textC = f'col {cols[0]}-{cols[-1]}'
                            pass
                        else:
                            textC = ''
                            for i, c in enumerate(cols):
                                if i != len(cols)-1:
                                    textC += f'{c}, '
                                else:
                                    textC += f'{c}'
                        tempC = c
            elif len(cols) == 1:
                textC = f'col {cols[0]}'
            else:
                textC = ''

            if len(rows) > 1:
                tempR = rows[0]
                for i, r in enumerate(rows):
                    if i != 0:
                        if r == tempR+1:
                            textR = f'row {rows[0]+1}-{rows[-1]+1}'
                        else:
                            textR = ''
                            for i, r in enumerate(rows):
                                if i != len(rows)-1:
                                    textR += f'{r+1}, '
                                else:
                                    textR += f'{r+1}'
                        tempR = r
            elif len(rows) == 1:
                textR = f'row {rows[0]+1}'
            else:
                textR = ''

            if len(rows) > 1 or len(cols) > 1:
                self.selectionText.configure(text=f'Cells from {textR} {textC}')
            else:
                self.selectionText.configure(text=f'Cell from {textR} {textC}')
        
        self.updateMeanText()

    def updateMeanText(self):
        value = self.getValues(self.dataTable.getSelectionValues())
        if value is not None:
            self.meanText.configure(text=f'Mean: {"{0:.2f}".format(value)}')
            self.nCellsText.configure(text=f'Number of cells: {len(self.dataTable.multiplerowlist)*len(self.dataTable.multiplecollist)}')
        else:
            self.meanText.configure(text='')
            self.nCellsText.configure(text='')

    def getInput(self):
        if self.treeView.selection() and len(self.treeView.selection()[0]) > 1 :
            loadIndex = self.treeView.selection()[0][0]
            varIndex = self.treeView.index(self.treeView.selection()[0])
            value = self.getValues(self.dataTable.getSelectionValues())

            try:
                self.importedData[loadIndex]
            except:
                self.importedData[loadIndex] = {}

            if value == None:
                self.notif.configure(text='Can not calculate mean of the given values.', background='red', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            else:
                iid = f'{loadIndex}{varIndex}'
                if varIndex == 0: # VO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('VO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{2}'))

                elif varIndex == 2: # HR
                    self.importedData[loadIndex].update( dict([(iid, dict([('HR', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{3}'))

                elif varIndex == 3: # SV
                    self.importedData[loadIndex].update( dict([(iid, dict([('SV', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{5}'))

                elif varIndex == 5: # Q
                    self.importedData[loadIndex].update( dict([(iid, dict([('Q', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{7}'))

                elif varIndex == 7: # [Hb]
                    self.importedData[loadIndex].update( dict([(iid, dict([('[Hb]', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{8}'))

                elif varIndex == 8: # SaO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('SaO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{9}'))

                elif varIndex == 9: # CaO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('CaO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{10}'))

                elif varIndex == 10: # CvO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('CvO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{11}'))

                elif varIndex == 11: # C(a-v)O2
                    self.importedData[loadIndex].update( dict([(iid, dict([('C(a-v)O2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{12}'))

                elif varIndex == 12: # QaO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('QaO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{13}'))

                elif varIndex == 13: # SvO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('SvO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{14}'))

                elif varIndex == 14: # PvO2
                    self.importedData[loadIndex].update( dict([(iid, dict([('PvO2', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{15}'))

                elif varIndex == 15: # T
                    self.importedData[loadIndex].update( dict([(iid, dict([('T', value), ('imported', True)]) )]))
                    self.treeView.selection_set((f'{loadIndex}{16}'))

                elif varIndex == 16: # pH
                    self.importedData[loadIndex].update( dict([(iid, dict([('pH', value), ('imported', True)]) )]))

                self.addCheckMarks()
                self.notif.configure(text='OK', background='green', foreground='white')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
    
    def addCheckMarks(self):
        for loadIndex, details in self.importedData.items():
            for iid, values in details.items():
                for key, value in values.items():
                    if key == 'imported':
                        if value == True:
                            text = self.treeView.item(iid)['text']
                            if '\u2713' not in text:
                                text = f'{text} \u2713'
                            self.treeView.item(iid, text=text)

    def getValues(self, input):
        if len(self.dataTable.multiplecollist) == 1 and len(self.dataTable.multiplerowlist) == 1:
            row = self.dataTable.multiplerowlist[0]
            col = self.dataTable.multiplecollist[0]
            try:
                value = float(self.dataTable.model.getValueAt(row,col))
            except:
                return None
        else:
            try:
                if len(input) < 2: # Vertical selection
                    value = np.mean(input[0])
                else: # Horizontal selection
                    temp = []
                    for c in self.dataTable.multiplecollist:
                        temp.append(float(self.dataTable.model.getValueAt(self.dataTable.multiplerowlist[0],c)))

                    value = np.mean(temp)
            except:
                return None

        return value
        
    def closeImporter(self, mode):
        if mode == 0:
            """ Done button clicked """
            
            self.window.destroy()

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

            # Add test
            if self.newTest:
                app.sidepanel_testList.addToList(self.test.id)
                self.subject.addTest(self.test)
                app.setActiveTest(self.test)
            else:
                app.setActiveTest(self.test)

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
                app.setActiveTest(t)

            app.projectDetailModule.refreshDetails()
            app.testDetailModule.refreshTestDetails()
        else: 
            """ Cancel button clicked """

            self.window.destroy()

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