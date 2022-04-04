from cmath import exp
from csv import excel_tab
import ctypes
import math
from re import sub
import sys
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from numpy import NaN
import pandas as pd
from pandastable import Table, TableModel
from modules.notification import notification
from objects.app import app
from objects.project import Project
from objects.subject import Subject

# Stage 0: id
# Stage 1: loads
# Stage 2: vo2
# Stage 3: hr
# Stage 4: sv
# Stage 5: q
# Stage 6: hb
# Stage 7: sao2
# Stage 8: CaO2
# Stage 9: CvO2
# Stage 10: CavO2
# Stage 11: QaO2
# Stage 12: SvO2
# Stage 13: PvO2
# Stage 14: Tc @ rest
# Stage 15: Tc\u209A\u2091\u2090\u2096
# Stage 16: pH0
# Stage 17: pH

# Luo vaihtoehdot tuo projekti, tuo käyttäjä, tuo testi
# tuodessa testiä lisätään aktiivisen käyttäjän alle jnejne.

##
## - Lisää tsekkaus, jos esim. len(collist) = 0, iske sarakkeen tiedot
## kaikkiin kuormiin
##
## - Virheilmoitus jos tulee indexerror
##

class DataImporter(object):
    def __init__(self):
        #print('IMPORTING YOU SAY')
        self.multiplecollist = []
        self.multiplerowlist = []
        self.multiplecells = []
        self.stage = 0
        self.atdivider = None
        self.tests = []
        self.subjects = {}
        self.currentDf = None
        self.tempLocData = {}

        file = askopenfile(mode ='r')
        if file is not None:
            self.data = pd.ExcelFile(file.name)
            self.dfList= {}

            for sheet in self.data.sheet_names:
                self.dfList[sheet] = pd.read_excel(self.data, sheet, header=None)

            self.window = Toplevel()
            self.window.title('Import')
            self.window.geometry('750x500')

            windowX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/2)
            windowY = app.root.winfo_rooty() + (app.root.winfo_reqheight()/10)
            self.window.geometry("+%d+%d" % ( windowX, windowY ))

            # Left panel
            self.leftPanel = ttk.Frame(self.window)
            self.leftPanel.pack(side=LEFT, fill=Y)

            # Progression
            ttk.Label(self.leftPanel, text='Data import steps').pack()
            self.progressionList = Listbox(self.leftPanel) #, font=('TkDefaultFont', 20)
            self.progressionList.insert('end', 'ID \U0001F878') # \U0001F878
            self.progressionList.insert('end', 'Load')
            self.progressionList.insert('end', 'VO\u2082')
            self.progressionList.insert('end', 'HR')
            self.progressionList.insert('end', 'SV')
            self.progressionList.insert('end', 'Q')
            self.progressionList.insert('end', 'Hb')
            self.progressionList.insert('end', 'SaO\u2082')
            self.progressionList.insert('end', 'CaO\u2082')
            self.progressionList.insert('end', 'CvO\u2082')
            self.progressionList.insert('end', 'CavO\u2082')
            self.progressionList.insert('end', 'QaO\u2082')
            self.progressionList.insert('end', 'SvO\u2082')
            self.progressionList.insert('end', 'PvO\u2082')
            self.progressionList.insert('end', 'T')
            self.progressionList.insert('end', 'pH')
            # self.progressionList.insert('end', 'Tc@rest')
            # self.progressionList.insert('end', 'Tc\u209A\u2091\u2090\u2096')
            # self.progressionList.insert('end', 'pH@rest')
            # self.progressionList.insert('end', 'pH\u209A\u2091\u2090\u2096')
            self.progressionList.pack(expand=1, fill=BOTH)
            self.progressionList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect(e) )

            # Right panel
            self.rightPanel = ttk.Frame(self.window)
            self.rightPanel.pack(side=RIGHT, fill=BOTH, expand=1)

            # Notification bar
            notifFrame = ttk.Frame(self.rightPanel)
            notifFrame.pack(fill=X)
            self.notif = ttk.Label(notifFrame, text='')
            self.notif.pack(fill=X)

            # Instructions
            headerFrame = ttk.Frame(self.rightPanel)
            headerFrame.pack(fill=X)
            self.instructionText = ttk.Label(headerFrame, text='Define column/row containing ID')
            self.instructionText.pack()
            self.selectionText = ttk.Label(headerFrame, text='')
            self.selectionText.pack(side=RIGHT, fill=BOTH)

            # Create menubutton for selection of excel sheet
            self.menuButton = ttk.Menubutton(headerFrame, text=list(self.data.sheet_names)[0])
            menu = Menu(self.menuButton, tearoff=False)

            for s in self.data.sheet_names:
                DataMenuElem(self, menu,self.menuButton, s)

            self.menuButton['menu'] = menu
            self.menuButton.pack(side=LEFT)

            # Data frame
            dataFrame = ttk.Frame(self.rightPanel)
            dataFrame.pack(fill=BOTH, expand=True)

            # Footer
            self.footer = ttk.Frame(self.rightPanel)
            self.footer.pack(side=BOTTOM, anchor='ne')

            nameOfFirstSheet = list(self.dfList)[0]

            self.dataTable = Table(dataFrame, dataframe=self.dfList[nameOfFirstSheet], editable=False)
            self.dataTable.show()

            # Make initial selection
            self.dataTable.selectNone()
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

            self.dataTable.bind('<B1-Motion>', self.handleDragSelection)
            self.dataTable.bind('<Button-1>', self.handleTableClick)
            self.dataTable.bind('<Control-Button-1>', self.handleTableCtrlClick)
            self.dataTable.bind('<Shift-Button-1>', self.handleDragSelection)
            self.dataTable.bind('<Button-3>', self.handleRightClick) 

            self.nextButton = ttk.Button(self.footer, text='Next', command=lambda: self.getInput())
            self.nextButton.grid(column=1, row=0)
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=lambda: self.closeImporter())
            self.cancelButton.grid(column=2, row=0)
        else:
            notification.create('error', 'Error opening file', 5000)

    def handleTableClick(self, e=None):
        pass
        """ print('handle LEFT click')
        col = self.dataTable.get_col_clicked(e)
        row = self.dataTable.get_row_clicked(e)
        self.multiplecollist = []
        self.multiplerowlist = []
        self.multiplecells = []
        self.dataTable.delete('ctrlSel')

        self.dataTable.delete('rect')
        self.dataTable.delete('multicellrect')
        self.deselectAll()

        ##
        self.multiplecells.append(self.dataTable.model.getValueAt(row, col))
        self.multiplecollist.append(col)
        self.multiplerowlist.append(row)

        self.dataTable.setSelectedRow(row)
        self.dataTable.setSelectedCol(col)
        self.dataTable.drawSelectedRect(row=row, col=col)
        self.dataTable.rowheader.drawRect(row)
        self.dataTable.tablecolheader.drawRect(col)

        self.updateSelectionText(e) """

    def handleTableCtrlClick(self,e):
        pass
        """ print('handle CTRL click')
        
        row = self.dataTable.get_row_clicked(e)
        col = self.dataTable.get_col_clicked(e)
        isSelected = False

        for i, r in enumerate(self.multiplerowlist):
            if r == row and self.multiplecollist[i] == col:
                isSelected = True
                self.dataTable.drawRect(row=row, col=col, delete=1)
                del self.multiplerowlist[i]
                del self.multiplecollist[i]

        if isSelected == False:
            self.multiplecells.append(self.dataTable.model.getValueAt(row, col))
            self.multiplecollist.append(col)
            self.multiplerowlist.append(row)

            for i, c in enumerate(self.multiplecollist):
                self.dataTable.drawRect(row=self.multiplerowlist[i], col=c, color='#E4DED4', tag='ctrlSel', delete=1)

        self.dataTable.drawSelectedRect(row=row, col=col)
        self.dataTable.rowheader.drawRect(row)
        self.dataTable.tablecolheader.drawRect(col)

        self.updateSelectionText(e) """
    
    def handleListboxSelect(self, e):
        index = self.progressionList.curselection()[0]
        self.nextStage(to=index)

    def handleColCtrlSelection(self,e):
        col = self.dataTable.get_col_clicked(e)
        if col not in self.multiplecollist:
            self.multiplecollist.append(col)
            # Select column
            self.dataTable.drawSelectedCol(col=col, delete=False)
            self.dataTable.tablecolheader.drawRect(col=col, delete=False)
        else:
            self.dataTable.delete('colrect')
            self.dataTable.tablecolheader.delete('rect')
            for i, c in enumerate(self.multiplecollist):
                if c == col:
                    del self.multiplecollist[i]
            
            for c in self.multiplecollist:
                self.dataTable.drawSelectedCol(col=c, delete=False)
                self.dataTable.tablecolheader.drawRect(col=c, delete=False)
        self.updateSelectionText(e)

    def handleDragSelection(self, e):
        pass
        """ self.multiplecollist = []
        self.multiplerowlist = []
        # self.dataTable.clearSelected()

        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        rowover = self.dataTable.get_row_clicked(e)
        colover = self.dataTable.get_col_clicked(e)
        startcol = self.dataTable.getSelectedColumn()
        startrow = self.dataTable.getSelectedRows().index[0]

        # print(f'STARTCOL {startcol}, COLOVER {colover}, STARTROW {startrow}, ROWOVER {rowover}')

        if colover == None or rowover == None:
            return

        if rowover >= self.dataTable.rows or startrow > self.dataTable.rows:
            return
        else:
            self.endrow = rowover

        #do columns
        if colover > self.dataTable.cols or startcol > self.dataTable.cols:
            return
        else:
            self.dataTable.endcol = colover
            if self.dataTable.endcol < startcol:
                self.multiplecollist=list(range(self.dataTable.endcol, startcol+1))
            else:
                self.multiplecollist=list(range(startcol, self.dataTable.endcol+1))

        for c in self.multiplecollist:
            #self.dataTable.drawSelectedCol(c, delete=False)
            self.dataTable.tablecolheader.drawRect(c, delete=False)

        #draw the selected rows
        if self.endrow != startrow:
            if self.endrow < startrow:
                self.multiplerowlist=list(range(self.endrow, startrow+1))
            else:
                self.multiplerowlist=list(range(startrow, self.endrow+1))
            #self.dataTable.drawMultipleRows(self.multiplerowlist)
            self.dataTable.rowheader.drawSelectedRows(self.multiplerowlist)
            #draw selected cells outline using row and col lists
            self.drawMultipleCells()
        else:
            self.multiplerowlist = []
            self.multiplerowlist.append(self.dataTable.currentrow)
            if len(self.multiplecollist) >= 1:
                self.drawMultipleCells()
            self.dataTable.delete('multiplesel')

        self.updateSelectionText(e) """

    def updateDragText(self):
        rows = self.multiplerowlist
        cols = self.multiplecollist
        #print(f'ROWS: {rows}')
        #print(f'COLS: {cols}')
        self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]}-{cols[-1]}')
        pass

    def drawMultipleCells(self):
        """Draw an outline box for multiple cell selection"""

        self.dataTable.delete('currentrect')
        self.dataTable.delete('multicellrect')
        
        rows = self.multiplerowlist
        cols = self.multiplecollist
        #print(f'ROWS: {rows}')
        #print(f'COLS: {cols}')
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
        self.multiplecollist = []
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
                self.multiplecollist=list(range(self.dataTable.endcol, startcol+1))
            else:
                self.multiplecollist=list(range(startcol, self.dataTable.endcol+1))

        for c in self.multiplecollist:
            self.dataTable.drawSelectedCol(c, delete=False)
            self.dataTable.tablecolheader.drawRect(c, delete=False)

        # self.updateColumnText()
        self.updateSelectionText(e)

    def handleRightClick(self, e):
        self.deselectAll()
        self.multiplecollist = []
        self.multiplerowlist = []
        self.multiplecells = []
        self.dataTable.delete('ctrlSel')
        self.dataTable.delete('currentrect')
        self.dataTable.delete('multicellrect')
        self.dataTable.delete('colrect')
        self.dataTable.tablecolheader.delete('rect')

        """ self.dataTable.selectNone()
        # Deselect column
        self.dataTable.setSelectedCol( -1 )
        self.dataTable.drawSelectedCol(-1)
        self.dataTable.tablecolheader.drawRect(-1)
        # Deselect row
        self.dataTable.setSelectedRow( -1 )
        self.dataTable.drawSelectedRow()
        self.dataTable.rowheader.clearSelected() """

        # self.dataTable.drawSelectedRect(row=-1, col=-1, color='red')
        self.selectionText.configure(text='')
            
    def selectCol(self, e):
        self.multiplecollist = []
        col = self.dataTable.get_col_clicked(e)
        self.deselectAll()

        # Select column
        self.dataTable.setSelectedCol( col )
        self.dataTable.drawSelectedCol( col=col )
        self.dataTable.tablecolheader.drawRect(col=col)
        self.multiplecollist.append(col)

        # self.updateColumnText()
        self.updateSelectionText(e)

    """ def updateColumnText(self):
        cols = self.multiplecollist
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
            self.selectionText.configure(text=f'Selected column {self.multiplecollist[0]}') """

    def updateSelectionText(self, e=None):
        # print('UPDATED CALLED')
        cols = self.multiplecollist
        rows = self.multiplerowlist
        cellX = self.dataTable.get_col_clicked(e)
        cellY = self.dataTable.get_row_clicked(e)
        # print(f'COLS: {cols}, ROWS: {rows}')

        if len(rows) > 0 and len(cols) == 0: # only rows selected
            # print('ONLY ROWS SELECTED')
            if len(rows) > 1:
                temp = rows[0]
                for i, r in enumerate(rows):
                    # print(r)
                    if i != 0:
                        if r == temp+1:
                            self.selectionText.configure(text=f'Selected cells {rows[0]+1}-{rows[-1]+1}')
                        else:
                            text = 'Selected cells '
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
            # print('ONLY COLS SELECTED')
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
                self.selectionText.configure(text=f'Selected column {self.multiplecollist[0]}')
     
        elif len(cols) == 1 and len(rows) == 1: # single cell selected
            # print('SINGEL CELL SELECTED')
            self.selectionText.configure(text=f'Selected cell row {cellY+1} - col {cellX}')
        else: # multiple cells selected
            # print('MULTIPLE CELLS SELECTED')
            text = ''
            if all(cols[0] == col for col in cols): # if all the selections in same col
                for r in rows:
                    text += f'{r+1},'
                self.selectionText.configure(text=f'Selected rows: {text} col: {cols[0]}')
            elif all(rows[0] == row for row in rows):  # if all the selections in same row
                for c in cols:
                    text += f'{c},'
                text = text[0:-1]
                self.selectionText.configure(text=f'Selected row: {rows[0]+1} cols: {text}')
            else:
                self.selectionText.configure(text=f'Multiple selections')

            # self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]}-{cols[-1]}')

    def selectRow(self, e):
        row = self.dataTable.get_row_clicked(e)
        rows = self.dataTable.getSelectedRows()
        #print(f'Selected rows {rows}')

        if len(rows.index) == 1: # if single row selected
            row = self.dataTable.get_row_clicked(e)

            self.deselectAll()
            
            # Select row
            self.dataTable.setSelectedRow( row )
            self.dataTable.drawSelectedRow()
            self.dataTable.rowheader.drawRect(row=row)

            self.selectionText.configure(text=f'Selected row {row+1}')
        else: # if multiple rows selected
            temp = rows.index[0]
            for i, r in enumerate(rows.index):
                if i != 0:
                    if r == temp+1:
                        self.selectionText.configure(text=f'Selected rows {rows.index[0]+1}-{rows.index[-1]+1}')
                    else:
                        text = 'Selected rows '
                        for i, r in enumerate(rows.index):
                            if i != len(rows.index)-1:
                                text += f'{r+1}, '
                            else:
                                text += f'{r+1}'

                        self.selectionText.configure(text=text)
                    temp = r

    def checkDataForm(self):
        # print(f'len collist: {len(self.multiplecollist)}')
        # print(f'len rowlist: {len(self.multiplerowlist)}')
        # print(f'selected rows: {len(self.dataTable.getSelectedRows())}')
        if len(self.multiplecollist) > 1 and len(self.multiplerowlist) > 1:

            if self.multiplecollist[0] == self.multiplecollist[1]:
                print('PITKÄ MUOTO')
                self.dataMode = 'long'
            elif self.multiplerowlist[0] == self.multiplerowlist[1]:
                print('LEVEÄ MUOTO')
                self.dataMode = 'wide'

        elif len(self.multiplecollist) > 1 or (len(self.multiplecollist) == 0 and len(self.dataTable.getSelectedRows()) > 0):
            print('LEVEÄ MUOTO')
            self.dataMode = 'wide'
        else:
            print('PITKÄ MUOTO')
            self.dataMode = 'long'

    def closeOptions(self, value):
        col = self.dataTable.getSelectedColumn()
        row = self.dataTable.getSelectedRow()
        if col >= 0:
            if value == 0:
                self.dataMode = 'wide'
            else:
                self.dataMode = 'long'
        if row >= 0:
            if value == 0:
                self.dataMode = 'long'
            else:
                self.dataMode = 'wide'
        self.options.destroy()

    def getInput(self):
        # print('GETTING INPUT')

        col = self.dataTable.getSelectedColumn()
        row = self.dataTable.getSelectedRow()
        rows = self.dataTable.getSelectedRows()
        nRows = self.dataTable.rows
        self.colValues = []
        self.columnNames = []
        self.rowValues = []
        self.rowNames= []
        success = False

        if self.stage == 0 and (len(self.multiplecollist) == 1 or len(rows) == 1 and row != -1):
            def move(e):
                editOptionsX = self.nextButton.winfo_rootx()-self.nextButton.winfo_reqwidth() - 10
                editOptionsY = self.nextButton.winfo_rooty()-(self.nextButton.winfo_reqheight()*4)
                self.options.geometry("+%d+%d" % ( editOptionsX, editOptionsY ))
                self.options.lift()

            self.options = Toplevel(bg='#38B3FF', borderwidth=5)
            self.options.overrideredirect(True)
            editOptionsX = self.nextButton.winfo_rootx()-self.nextButton.winfo_reqwidth() - 10
            editOptionsY = self.nextButton.winfo_rooty()-(self.nextButton.winfo_reqheight()*4)
            self.options.geometry("+%d+%d" % ( editOptionsX, editOptionsY ))
            self.options.lift()

            self.options.bind('<Configure>', move)

            container = Frame(self.options, bd=0)
            container.pack()            
            var = IntVar()
            ttk.Label(container, text='Selection contains single ID or multiple ID?').pack()
            ttk.Radiobutton(container, variable=var, value=0, text='Single ID').pack()
            ttk.Radiobutton(container, variable=var, value=1, text='Multiple IDs').pack()
            ttk.Button(container, text='OK', command=lambda: self.closeOptions(var.get())).pack()

            self.window.wait_window(self.options)

        if len(self.multiplecollist) > 0 and len(self.multiplerowlist) > 0: # set up values lists if multicell
            for i, c in enumerate(self.customGetSelectionValues()):
                # self.dataTable.setSelectedCol(c)
                # self.colValues.append(self.customGetSelectionValues()[0][0:])
                # self.columnNames.append(self.customGetSelectionValues()[0][0])
                self.colValues.append(c[0:])
                self.columnNames.append(c[0])

            for r in self.multiplerowlist:
                self.dataTable.setSelectedRow(r)
                self.rowValues.append(self.dataTable.getSelectedRows())
                self.rowNames.append(self.dataTable.getSelectedRows().iloc[0,0])
        else: # set up values lists if whole rows/cols selected
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
                # self.dataTable.setSelectedCol(c)
                # print(f'JEPPISJEE: {self.customGetSelectionValues()}')
                self.colValues.append(c[0:])
                self.columnNames.append(c[0])
            # self.colValues = self.customGetSelectionValues()
            # self.columnNames = self.customGetSelectionValues()[0][0]

        # print(f'col names: {self.columnNames}')
        # print(f'col values: {self.colValues}')
        # print(f'row names: {self.rowNames}')
        # print(f'row values: {self.rowValues}')
        # print(rows)
        # print(nRows)
        
        # print(f'Current selections: R{row}, C{col} - ROWS{rows.index}')
        # print(f'Current list selections: R{self.multiplerowlist}, C{self.multiplecollist}')

        if col == -1 and row == -1: # nothing selected
            #print('NOTHING SELECTED')
            s = ttk.Style()
            s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
            self.notif.configure(style='error.TLabel', text=f'Nothing selected')
            self.notif.after(5000, lambda: self.notif.configure(text='', style='TLabel'))
        else: # something selected

            if col == -1: # rows selected
                if self.stage == 0: # ids
                    if len(rows) > 1 and col == -1: # multiple rows
                        print('USEAMPI RIVI')
                        if self.stage == 0: # ids
                            # self.checkDataForm()
                            for i, id in enumerate(self.rowNames):
                                # Create subject, set its id, add a test, reset workloads
                                subject = Subject()
                                subject.setId(id)
                                subject.addTest()
                                subject.getTests()[0].workLoads = []
                                self.subjects[rows.index[i]] = subject

                            self.tempLocData['id'] = self.rowNames
                            print(self.subjects)
                            success = True

                    else: # single rows
                        print('YKSI RIVI')
                        if self.stage == 0: #ids
                            if self.dataMode == 'long':
                                for i, id in enumerate(self.rowNames):
                                    # Create subject, set its id, add a test, reset workloads
                                    subject = Subject()
                                    subject.setId(id)
                                    subject.addTest()
                                    subject.getTests()[0].workLoads = []
                                    self.subjects[rows.index[i]] = subject

                                # self.tempLocData['id'] = self.rowNames[0]

                            elif self.dataMode == 'wide':
                                for i, id in enumerate(self.rowValues[0]):
                                    if i != 0:
                                        # Create subject, set its id, add a test, reset workloads
                                        subject = Subject()
                                        subject.setId(id)
                                        subject.addTest()
                                        subject.getTests()[0].workLoads = []
                                        self.subjects[i] = subject

                            # self.tempLocData['id'] = self.rowNames
                            print(self.subjects)
                            success = True

                elif self.stage == 1: # Loads
                    #print('**LOADS**')
                    success = self.getLoadsFromRows()

                elif self.stage == 2: #VO2
                    #print('**VO2**')
                    success = self.getRowValues('VO2')

                elif self.stage == 3: #HR
                    #print('**HR**')
                    success = self.getRowValues('HR')

                elif self.stage == 4: #SV
                    #print('**SV**')
                    success = self.getRowValues('SV')

                elif self.stage == 5: #Q
                    #print('**Q**')
                    success = self.getRowValues('Q')

                elif self.stage == 6: #Hb
                    #print('**Hb**')
                    success = self.getRowValues('Hb')

                elif self.stage == 7: #SaO2
                    #print('**SaO2**')
                    success = self.getRowValues('SaO2')

                elif self.stage == 8: #CaO2
                    #print('**CaO2**')
                    success = self.getRowValues('CaO2')

                elif self.stage == 9: #CvO2
                    #print('**CvO2**')
                    success = self.getRowValues('CvO2')

                elif self.stage == 10: #CavO2
                    #print('**CavO2**')
                    success = self.getRowValues('CavO2')

                elif self.stage == 11: #QaO2
                    #print('**QaO2**')
                    success = self.getRowValues('QaO2')

                elif self.stage == 12: #SvO2
                    #print('**SvO2**')
                    success = self.getRowValues('SvO2')

                elif self.stage == 13: #PvO2
                    #print('**PvO2**')
                    success = self.getRowValues('PvO2')
                    
                elif self.stage == 14: #T
                    success = self.getRowValues('T')

                elif self.stage == 15: #pH
                    success = self.getRowValues('pH')

                if success:
                    self.addCheckMark(self.stage)
                    self.nextStage()

            if row == -1: # cols selected
                if self.stage == 0: #ids
                    if len(self.multiplecollist) > 1: # multiple columns
                        #print('USEAMPI SARAKE')
                        
                        if self.stage == 0: # ids
                            # self.checkDataForm()
                            for i, id in enumerate(self.columnNames):
                                # Create subject, set its id, add a test, reset workloads
                                subject = Subject()
                                subject.setId(id)
                                subject.addTest()
                                subject.getTests()[0].workLoads = []
                                # self.subjects.append(subject)
                                colIndex = self.multiplecollist[i]
                                self.subjects[colIndex] = subject

                            print(self.subjects)
                            success = True
                            # self.tempLocData['id'] = self.columnNames

                    else: # one column
                        if self.stage == 0: # ids
                            # self.checkDataForm()
                            if self.dataMode == 'long':
                                for i, c in enumerate(self.colValues): #iterate cols as list
                                    for ci, cv in enumerate(c): #iterate values
                                        if ci != 0: #skip header
                                            # Create subject, set its id, add a test, reset workloads
                                            subject = Subject()
                                            subject.setId(cv)
                                            subject.addTest()
                                            subject.getTests()[0].workLoads = []
                                            self.subjects[ci] = subject
                            else:
                                for i, id in enumerate(self.columnNames):
                                    # Create subject, set its id, add a test, reset workloads
                                    subject = Subject()
                                    subject.setId(id)
                                    subject.addTest()
                                    subject.getTests()[0].workLoads = []
                                    colIndex = self.multiplecollist[i]
                                    self.subjects[colIndex] = subject

                            print(self.subjects)
                            success = True
                            # self.tempLocData['id'] = self.colValues[0][1:]
                    
                elif self.stage == 1: # Loads
                    # print('**LOADS**')
                    success = self.getLoadsFromCols()

                elif self.stage == 2: #VO2
                    #print('**VO2**')
                    success = self.getColumnValues('VO2')

                elif self.stage == 3: #HR
                    #print('**HR**')
                    success = self.getColumnValues('HR')

                elif self.stage == 4: #SV
                    #print('**SV**')
                    success = self.getColumnValues('SV')

                elif self.stage == 5: #Q
                    #print('**Q**')
                    success = self.getColumnValues('Q')

                elif self.stage == 6: #Hb
                    #print('**Hb**')
                    success = self.getColumnValues('Hb')

                elif self.stage == 7: #SaO2
                    #print('**SaO2**')
                    success = self.getColumnValues('SaO2')

                elif self.stage == 8: #CaO2
                    #print('**CaO2**')
                    success = self.getColumnValues('CaO2')

                elif self.stage == 9: #CvO2
                    #print('**CvO2**')
                    success = self.getColumnValues('CvO2')

                elif self.stage == 10: #CavO2
                    #print('**CavO2**')
                    success = self.getColumnValues('CavO2')

                elif self.stage == 11: #QaO2
                    #print('**QaO2**')
                    success = self.getColumnValues('QaO2')

                elif self.stage == 12: #SvO2
                    #print('**SvO2**')
                    success = self.getColumnValues('SvO2')

                elif self.stage == 13: #PvO2
                    #print('**PvO2**')
                    success = self.getColumnValues('PvO2')
                    
                elif self.stage == 14: #T
                    success = self.getColumnValues('T')

                elif self.stage == 15: #pH
                    success = self.getColumnValues('pH')

                if success:
                    self.addCheckMark(self.stage)
                    self.nextStage()

            if row >= 0 and col >= 0: # cells selected
                if len(self.multiplerowlist) > 1 or len(self.multiplecollist) > 1: # multiple cells
                    print('MULTIPLE CELLS SELECTED')

                    if self.stage == 0: # ids
                        # self.checkDataForm()
                        self.subjects = {}

                        if self.dataMode == 'wide':
                            for i, c in enumerate(self.multiplecollist):
                                if len(self.multiplerowlist) == 1:
                                    for r in self.multiplerowlist:
                                        # Create subject, set its id, add a test, reset workloads
                                        subject = Subject()
                                        subject.setId(self.columnNames[i])
                                        subject.addTest()
                                        subject.getTests()[0].workLoads = []
                                        # self.subjects.append(subject)
                                        self.subjects[c] = subject
                                else:
                                    subject = Subject()
                                    subject.setId(self.columnNames[i])
                                    subject.addTest()
                                    subject.getTests()[0].workLoads = []
                                    # self.subjects.append(subject)
                                    self.subjects[c] = subject

                            self.tempLocData['id'] = self.columnNames

                        elif self.dataMode == 'long':
                            for i, r in enumerate(self.multiplerowlist):
                                if len(self.multiplecollist) == 1:
                                    for c in self.multiplecollist:
                                        # Create subject, set its id, add a test, reset workloads
                                        subject = Subject()
                                        subject.setId(self.rowNames[i])
                                        subject.addTest()
                                        subject.getTests()[0].workLoads = []
                                        # self.subjects.append(subject)
                                        self.subjects[r] = subject
                                else:
                                    subject = Subject()
                                    subject.setId(self.rowNames[i])
                                    subject.addTest()
                                    subject.getTests()[0].workLoads = []
                                    # self.subjects.append(subject)
                                    self.subjects[r] = subject
                            
                            self.tempLocData['id'] = self.rowNames
                        
                        print(self.subjects)
                        success = True
                    
                    elif self.stage == 1: # loads
                        #print('**LOADS**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        self.getMultiCellLoads()
                        success = True

                    elif self.stage == 2: # VO2
                        #print('**VO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('VO2')

                    elif self.stage == 3: # HR
                        #print('**HR**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('HR')
                    
                    elif self.stage == 4: # SV
                        #print('**SV**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('SV')

                    elif self.stage == 5: # Q
                        #print('**Q**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('Q')

                    elif self.stage == 6: # Hb
                        #print('**Hb**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('Hb')

                    elif self.stage == 7: # SaO2
                        #print('**SaO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('SaO2')

                    elif self.stage == 8: # CaO2
                        #print('**CaO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('CaO2')

                    elif self.stage == 9: # CvO2
                        #print('**CvO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('CvO2')

                    elif self.stage == 10: # CavO2
                        #print('**CavO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('CavO2')

                    elif self.stage == 11: # QaO2
                        #print('**QaO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('QaO2')

                    elif self.stage == 12: # SvO2
                        #print('**SvO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('SvO2')

                    elif self.stage == 13: # PvO2
                        #print('**PvO2**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('PVO2')
                    
                    elif self.stage == 14: # Tc @ rest
                        #print('**Tc @ rest**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('Tc@rest')

                    elif self.stage == 15: # Tc\u209A\u2091\u2090\u2096
                        #print('**Tc\u209A\u2091\u2090\u2096**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('Tc\u209A\u2091\u2090\u2096')

                    elif self.stage == 16: # pH @ rest
                        #print('**pH @ rest**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('pH@rest')

                    elif self.stage == 17: # pH\u209A\u2091\u2090\u2096
                        #print('**pH\u209A\u2091\u2090\u2096**')
                        #print(f'**DATA FORM** {self.dataMode}')
                        success = self.getMultiCellValues('pH\u209A\u2091\u2090\u2096')

                else: # single cell
                    print('SINGLE CELL SELECTED')
                    value = self.dataTable.model.getValueAt(row, col)
                    columnName = self.dataTable.getSelectionValues()[0][0]
                    rowName = self.dataTable.getSelectedRows().iloc[0,0]

                    if self.stage == 0: # ids
                        # Create subject, set its id, add a test, reset workloads
                        self.subjects = {}
                        subject = Subject()
                        subject.setId(value)
                        subject.addTest()
                        subject.getTests()[0].workLoads = []
                        # self.subjects.append(subject)
                        i = f'{row}-{col}'
                        self.subjects[i] = subject
                        self.dataMode = None
                        success = True
                        self.tempLocData['id'] = value

                    elif self.stage == 1: # loads
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.createLoad()
                        """ if self.dataMode == 'long':
                            load.setName(rowName) # row name
                        elif self.dataMode == 'wide':
                            load.setName(columnName) # column name """
                        load.setName(columnName) # column name
                        load.getDetails().setValue('Load', value) # set value
                        load.getDetails().setImported(True) # set as imported
                        success = True

                    elif self.stage == 2: # VO2
                        success = self.getSingleCellValue('VO2', value)

                    elif self.stage == 3: # HR
                        success = self.getSingleCellValue('HR', value)

                    elif self.stage == 4: # SV
                        success = self.getSingleCellValue('SV', value)

                    elif self.stage == 5: # Q
                        success = self.getSingleCellValue('Q', value)

                    elif self.stage == 6: # Hb
                        success = self.getSingleCellValue('Hb', value)

                    elif self.stage == 7: # SaO2
                        success = self.getSingleCellValue('SaO2', value)

                    elif self.stage == 8: # CaO2
                        success = self.getSingleCellValue('CaO2', value)

                    elif self.stage == 9: # CvO2
                        success = self.getSingleCellValue('CvO2', value)

                    elif self.stage == 10: # CavO2
                        success = self.getSingleCellValue('CavO2', value)

                    elif self.stage == 11: # QaO2
                        success = self.getSingleCellValue('QaO2', value)

                    elif self.stage == 12: # SvO2
                        success = self.getSingleCellValue('SvO2', value)

                    elif self.stage == 13: # PvO2
                        success = self.getSingleCellValue('PvO2', value)
                    
                    elif self.stage == 14: # Tc @ rest
                        success = self.getSingleCellValue('Tc@rest', value)

                    elif self.stage == 15: # Tc\u209A\u2091\u2090\u2096
                        success = self.getSingleCellValue('Tc\u209A\u2091\u2090\u2096', value)

                    elif self.stage == 16: # pH @ rest
                        success = self.getSingleCellValue('pH@rest', value)

                    elif self.stage == 17: # pH\u209A\u2091\u2090\u2096
                        success = self.getSingleCellValue('pH\u209A\u2091\u2090\u2096', value)

                if success:
                    self.addCheckMark(self.stage)
                    self.nextStage()

    def closeImporter(self):
        if hasattr(self, 'test'):
            del self.test
        self.window.destroy()
        self.options.destroy()
        del self

    def updateTable(self, table):
        self.dataTable.updateModel(TableModel(self.dfList[table]))
        self.dataTable.redraw()

    def deselectAll(self):
        self.dataTable.selectNone()
        # Deselect column
        self.dataTable.setSelectedCol( -1 )
        self.dataTable.drawSelectedCol(-1)
        self.dataTable.tablecolheader.drawRect(-1)
        # Deselect row
        self.dataTable.setSelectedRow( -1 )
        self.dataTable.drawSelectedRow()
        self.dataTable.rowheader.clearSelected()

    def customGetSelectionValues(self):
        """Get values for current multiple cell selection"""
        rows = range(self.dataTable.rows)
        cols = self.multiplecollist
        model = self.dataTable.model
        lists = []

        # print('CUSTOM')

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
        for rowIndex, s in self.subjects.items():
            test = s.getTests()[0]
            test.workLoads = [] # delete previous workloads, if re-fetching loads

            for i, v in enumerate(self.colValues): #iterate cols as list
                for ci, cv in enumerate(v): #iterate values
                    if ci == rowIndex: #if row matches subject's row
                        columnName = self.columnNames[i]
                        load = test.createLoad()
                        
                        load.setName(columnName) # column name
                        load.getDetails().setValue('Load', cv) # set value
                        load.getDetails().setImported(True)
                        continue
        
        self.tempLocData['Load'] = self.columnNames
        return True

    def getLoadsFromRows(self):
        for colIndex, s in self.subjects.items():
            test = s.getTests()[0]
            test.workLoads = [] # delete previous workloads, if re-fetching loads

            for i, v in enumerate(self.rowValues): #iterate rows as list
                for ci, cv in enumerate(v): #iterate values
                    if ci == colIndex: #if col matches subject's col
                        rowName = self.rowNames[i]
                        load = test.createLoad()
                        load.setName(rowName) # row name
                        load.getDetails().setValue('Load', cv) # set value
                        load.getDetails().setImported(True)
                        continue
        
        self.tempLocData['Load'] = self.rowNames
        return True

    def getColumnValues(self, label):
        flag = False

        for rowIndex, s in self.subjects.items():
            test = s.getTests()[0]
            loads = test.getWorkLoads()
            
            if len(self.colValues) < len(loads) and len(self.colValues) != 1:
                    s = ttk.Style()
                    s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(style='error.TLabel', text=f'You have {len(loads)} loads but only {len(self.colValues)} values given')
                    self.notif.after(5000, lambda: self.notif.configure(text='', style='TLabel'))
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
        # self.tempLocData[label] = self.columnNames

    def getRowValues(self, label):
        flag = False

        for colIndex, s in self.subjects.items():
            test = s.getTests()[0]
            loads = test.getWorkLoads()
            
            if len(self.rowValues) < len(loads) and len(self.rowValues) != 1:
                    s = ttk.Style()
                    s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(style='error.TLabel', text=f'You have {len(loads)} loads but only {len(self.rowValues)} values given')
                    self.notif.after(5000, lambda: self.notif.configure(text='', style='TLabel'))
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
        # self.tempLocData[label] = self.rowNames

    def getMultiCellLoads(self):
        colList = self.multiplecollist
        rowList = self.multiplerowlist

        if self.dataMode == None:
            if all(colList[0] == col for col in colList):
                self.dataMode = 'wide'
            elif all(rowList[0] == col for col in rowList):
                self.dataMode = 'long'
            elif len(colList) > len(rowList):
                self.dataMode = 'long'
            else:
                self.dataMode = 'wide'

        if self.dataMode == 'long':
            print('LONG')

            # iterate cols
            # get value by subject row

            if len(self.subjects) == 1:
                i = list(self.subjects) 
                i = i[0].split('-')[0]

                for s in self.subjects.values():
                    test = s.tests[0]
                    test.workLoads = [] # delete previous workloads, if re-fetching loads

                for ri, r in enumerate(rowList):
                    print(f'r {r}, i {i}')
                    if r == i:
                        columnName = self.columnNames[ri]
                        load = test.createLoad()
                        load.setName(columnName) # column name
                        print(self.colValues[ri][i])
                        load.getDetails().setValue('Load', self.colValues[ri][i]) # set value
                        load.getDetails().setImported(True)

            else:
                for rowIndex, s in self.subjects.items():
                    test = s.tests[0]
                    test.workLoads = [] # delete previous workloads, if re-fetching loads
                    self.colValues = list(dict.fromkeys(self.colValues))
                    print(f'debug len {len(self.colValues)}')
                    for v in self.colValues:
                        for ci, cv in enumerate(v):
                            if ci == rowIndex:
                                columnName = v[0]
                                load = test.createLoad()
                                load.setName(columnName) # column name
                                load.getDetails().setValue('Load', cv) # set value
                                load.getDetails().setImported(True)
                                continue

                """ for ri, r in enumerate(rowList):
                if len(self.subjects) > 1:
                    test = self.subjects[ri].getTests()[0]
                else:
                    test = self.subjects[0].getTests()[0]
                test.workLoads = [] # delete previous workloads, if re-fetching loads

                for ci, c in enumerate(colList):
                    columnName = self.columnNames[ci]
                    load = test.createLoad()
                    load.setName(columnName) # column name
                    load.getDetails().setValue('Load', self.colValues[ci][r]) # set value
                    load.getDetails().setImported(True) """

                """ if len(rowList) == 1 or all(rowList[0] == col for col in rowList): # single row
                    print('single row')
                    for ci, c in enumerate(colList):
                        columnName = self.columnNames[ci]
                        load = test.createLoad()
                        load.setName(columnName) # column name
                        load.getDetails().setValue('Load', self.colValues[ci][r]) # set value
                        load.getDetails().setImported(True)
                else: # multiple rows
                    print('multiple rows')
                    columnName = self.columnNames[ri]
                    load = test.createLoad()
                    load.setName(columnName) # column name
                    load.getDetails().setValue('Load', self.colValues[ri][r]) # set value
                    load.getDetails().setImported(True)
                    continue """

            self.tempLocData['Load'] = self.colValues

        elif self.dataMode == 'wide':
            print('WIDE')
            for i, s in self.subjects.items():
                test = s.tests[0]

                for ci, c in enumerate(colList):
                    if c == i:
                        rowName = self.rowNames[ci]
                        load = test.createLoad()
                        load.setName(rowName) # row name
                        load.getDetails().setValue('Load', self.colValues[ci][rowList[ci]]) # set value
                        load.getDetails().setImported(True)
                """ for ci, c in enumerate(colList):
                if len(self.subjects) > 1:
                    test = self.subjects[ci].getTests()[0]
                else:
                    test = self.subjects[0].getTests()[0]
                test.workLoads = [] # delete previous workloads, if re-fetching loads

                for ri, r in enumerate(rowList):
                    rowName = self.rowNames[ri]
                    load = test.createLoad()
                    load.setName(rowName) # column name
                    load.getDetails().setValue('Load', self.colValues[ci][r]) # set value
                    load.getDetails().setImported(True) """

                """ if len(rowList) == 1: # if selected by dragging or shift
                    print('SHIFT/DRAG')
                    for ri, r in enumerate(rowList):
                        rowName = self.rowNames[ri]
                        load = test.createLoad()
                        load.setName(rowName) # column name
                        load.getDetails().setValue('Load', self.colValues[ci][r]) # set value
                        load.getDetails().setImported(True)
                else: # if selected with ctrl
                    print('CTRL')
                    rowName = self.rowNames[ci]
                    load = test.createLoad()
                    load.setName(rowName) # column name
                    load.getDetails().setValue('Load', self.colValues[ci][rowList[ci]]) # set value
                    load.getDetails().setImported(True)
                    continue """

            self.tempLocData['Load'] = self.colValues

    def getMultiCellValues(self, label):
        colList = self.multiplecollist
        rowList = self.multiplerowlist
        nLoads = len(self.tempLocData['Load'])
        flag = False

        if self.dataMode == 'long':
            for si, s in enumerate(self.subjects):
                test = s.getTests()[0]
                loads = test.getWorkLoads()
                    
                if len(colList) < nLoads and len(colList) != 1:
                    s = ttk.Style()
                    s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(style='error.TLabel', text=f'You have {nLoads} loads but only {len(colList)} values given')
                    self.notif.after(5000, lambda: self.notif.configure(text='', style='TLabel'))
                else:
                    for li, l in enumerate(loads):
                        details = l.getDetails()
                        if len(colList) == 1:
                            value = self.dataTable.model.getValueAt(rowList[si], colList[0])
                        else:
                            value = self.dataTable.model.getValueAt(rowList[si], colList[li])
                        details.setValue(label, value)   
                        flag = True

        elif self.dataMode == 'wide':
            for si, s in enumerate(self.subjects):
                test = s.getTests()[0]
                loads = test.getWorkLoads()

                if len(rowList) < nLoads and len(rowList) != 1:
                    s = ttk.Style()
                    s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(style='error.TLabel', text=f'You have {nLoads} loads but only {len(rowList)} values given')
                    self.notif.after(5000, lambda: self.notif.configure(text='', style='TLabel'))
                else:
                    for li, l in enumerate(loads):
                        details = l.getDetails()
                        if len(rowList) == 1:
                            value = self.dataTable.model.getValueAt(rowList[0], colList[si])
                        else:
                            value = self.dataTable.model.getValueAt(rowList[li], colList[si])
                        details.setValue(label, value)
                        flag = True
        return flag

    def getSingleCellValue(self, label, value):
        s = self.subjects[0]
        test = s.getTests()[0]
        load = test.getWorkLoads()[0]
        load.getDetails().setValue(label, value) # set value
        return True

    def prevStage(self):
        to = self.stage - 1
        self.nextStage(to=to)

    def nextStage(self, to=None):
        if to == None:
            # self.stage += 1 
            to = self.stage + 1

        #print(f'tällä hetkellä stage: {to}')

        if to > 0:
            ttk.Button(self.footer, text='Prev', command=lambda: self.prevStage()).grid(column=0, row=0)
            passBtn = ttk.Button(self.footer, text='Skip', command=lambda: self.nextStage())
            passBtn.grid(column=2, row=0)
            ttk.Button(self.footer, text='Done', command=lambda: self.importData()).grid(column=3, row=0)
            self.cancelButton.grid(column=4, row=0)
        
        self.deselectAll()

        if to == 0:
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define ID column/row')
        elif to == 1:
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define loads row/column')
        elif to == 2: # -> VO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define VO\u2082 row/column')
        elif to== 3: # -> HR
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define HR row/column')
        elif to == 4: # -> SV
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define SV row/column')
        elif to == 5: # -> Q
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define Q row/column')
        elif to == 6: # -> Hb
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define Hb row/column')
        elif to == 7: # -> SaO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define SaO\u2082 row/column')
        elif to == 8: # -> CaO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define CaO\u2082 row/column')
        elif to == 9: # -> CvO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define CvO\u2082 row/column')
        elif to == 10: # -> CavO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define CavO\u2082 row/column')
        elif to == 11: # -> QaO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define QaO\u2082 row/column')
        elif to == 12: # -> SvO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define SvO\u2082 row/column')
        elif to == 13: # -> PvO2
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define PvO\u2082 row/column')
        elif to == 14: # -> T
            self.moveArrow(self.stage, to)
            passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define T row/column')
        elif to == 15: # -> pH
            self.moveArrow(self.stage, to)
            passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define pH row/column')
        elif to == 16: # Finish
            self.importData()

        self.stage = to

    def moveArrow(self, from_, to):
        value = self.progressionList.get(from_)
        """ if self.stage == 14 or self.stage == 16: # if pH or T @ rest
            value = value.split(' ')[0:3]
            value = f'{value[0]} {value[1]} {value[2]}'
        else:
            value = value.split(' ')
            value = f'{value[0]} {value[1]}' """
        # value = value.split(' ')[0]
        # value = f'{value} \u2713'
        if '\U0001F878' in value:
            value = value.replace('\U0001F878','')
        self.progressionList.delete(from_)
        self.progressionList.insert(from_, value)

        value = self.progressionList.get(to)
        if '\U0001F878' not in value:
            value = f'{value} \U0001F878'
        self.progressionList.delete(to)
        self.progressionList.insert(to, value)

    def addCheckMark(self, to):
        # print(f'adding mark to {to}')
        value = self.progressionList.get(to)
        value = f'{value.split(" ")[0]} \u2713'
        # print(value)
        self.progressionList.delete(to)
        self.progressionList.insert(to, value)

    def importData(self):
        # print(f'SUBJECTS {self.subjects}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()[0].getDetails().getWorkLoadDetails()}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()[1].getDetails().getWorkLoadDetails()}')
        project = Project()
        app.setActiveProject(project)
        app.setActiveSubject(None)
        app.setActiveTest(None)

        project.data = self.dfList

        # Add dataloc information
        # project.dataMode = self.dataMode
        project.idLoc = self.tempLocData.get('id', None)
        project.loadLoc = self.tempLocData.get('Load', None)
        project.vo2Loc = self.tempLocData.get('VO2', None)
        project.hrLoc = self.tempLocData.get('HR', None)
        project.svLoc = self.tempLocData.get('SV', None)

        project.qLoc = self.tempLocData.get('Q', None)
        project.hbLoc = self.tempLocData.get('Hb', None)
        project.sao2Loc = self.tempLocData.get('SaO2', None)
        project.cao2Loc = self.tempLocData.get('CaO2', None)
        project.cvo2Loc = self.tempLocData.get('CvO2', None)

        project.cavo2Loc = self.tempLocData.get('CavO2', None)
        project.qao2Loc = self.tempLocData.get('QaO2', None)
        project.svo2Loc = self.tempLocData.get('SvO2', None)
        project.pvo2Loc = self.tempLocData.get('PvO2', None)

        project.tcRestLoc = self.tempLocData.get('Tc @ rest', None)
        project.tcLoc = self.tempLocData.get('Tc\u209A\u2091\u2090\u2096', None)
        project.phRestLoc = self.tempLocData.get('pH @ rest', None) 
        project.phLoc = self.tempLocData.get('pH\u209A\u2091\u2090\u2096', None)
        
        # for key, value in self.dfList.items():
        #     print(key)
        #     print(value)

        """ print(project.idLoc)
        print(project.loadLoc)
        print(project.vo2Loc)
        print(project.hrLoc)
        print(project.svLoc)

        print(project.qLoc)
        print(project.hbLoc)
        print(project.sao2Loc)
        print(project.cao2Loc)
        print(project.cvo2Loc)

        print(project.cavo2Loc)
        print(project.qao2Loc)
        print(project.svo2Loc)
        print(project.pvo2Loc)

        print(project.tcRestLoc)
        print(project.tcLoc)
        print(project.phRestLoc)
        print(project.phLoc) """

        if type(self.subjects) is dict:
            for s in self.subjects.values():
                project.addSubject(s)
        else:
            for s in self.subjects:
                project.addSubject(s)

        app.sidepanel_projectList.refreshList()
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()

        app.projectDetailModule.refreshDetails()
        # app.testDetailModule

        # Update app state
        app.sidepanel_projectList.addToList(project.id)
        app.addProject(project)

        self.window.destroy()
        del self

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