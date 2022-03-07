from re import I
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from numpy import empty
import pandas as pd
from pandastable import Table, TableModel
from modules.notification import notification
from objects.app import app
from objects.project import Project
from objects.subject import Subject
from objects.test import Test

# Stage 0: id
# Stage 1: loads
# Stage 2: vo2
# Stage 3: hr
# Stage 4: sv
# Stage 5: q
# Stage 6: hb
# Stage 7: sao2

class DataImporter(object):
    def __init__(self):
        print('IMPORTING YOU SAY')
        self.multiplecollist = []
        self.multiplerowlist = []
        self.multiplecells = []
        self.stage = 0
        self.tests = []
        self.subjects = []
        self.currentDf = None

        file = askopenfile(mode ='r')
        if file is not None:
            data = pd.ExcelFile(file.name)
            self.dfList= {}

            for sheet in data.sheet_names:
                self.dfList[sheet] = pd.read_excel(data, sheet)

            self.window = Toplevel()
            self.window.title('Import')
            self.window.geometry('500x500')

            windowX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/2)
            windowY = app.root.winfo_rooty() + (app.root.winfo_reqheight()/10)
            self.window.geometry("+%d+%d" % ( windowX, windowY ))

            # Instructions
            headerFrame = ttk.Frame(self.window)
            headerFrame.pack()
            self.instructionText = ttk.Label(headerFrame, text='Define ID column/row')
            self.instructionText.pack()
            self.selectionText = ttk.Label(headerFrame, text='')
            self.selectionText.pack(side=RIGHT)

            # Create menubutton for selection of excel sheet
            self.menuButton = ttk.Menubutton(headerFrame, text=list(data.sheet_names)[0])
            menu = Menu(self.menuButton, tearoff=False)

            for s in data.sheet_names:
                DataMenuElem(self, menu,self.menuButton, s)

            self.menuButton['menu'] = menu
            self.menuButton.pack()

            # Data frame
            dataFrame = ttk.Frame(self.window)
            dataFrame.pack(fill=BOTH, expand=True)

            # Footer
            self.footer = ttk.Frame(self.window)
            self.footer.pack(side=BOTTOM, anchor='ne')

            nameOfFirstSheet = list(self.dfList)[0]

            self.dataTable = Table(dataFrame, dataframe=self.dfList[nameOfFirstSheet])
            self.dataTable.show()

            # Make initial selection
            self.dataTable.selectNone()
            self.dataTable.setSelectedCol(-1)
            self.dataTable.setSelectedRow(-1)
            
            self.dataTable.tablecolheader.bind('<Button-1>', self.selectCol)
            self.dataTable.tablecolheader.bind('<ButtonRelease-1>', self.handleColCtrlSelection)
            self.dataTable.tablecolheader.bind('<B1-Motion>', self.handleColDrag)
            self.dataTable.tablecolheader.bind('<Button-3>', self.handleRightClick)

            self.dataTable.rowheader.bind('<ButtonRelease-1>', self.selectRow)
            self.dataTable.rowheader.bind('<Button-3>', self.handleRightClick)
            
            #self.dataTable.bind('<Button-1>', self.handleLeftClick)
            self.dataTable.bind('<B1-Motion>', self.handleDragSelection)
            self.dataTable.bind('<Button-1>', self.handleTableClick)
            self.dataTable.bind('<Button-3>', self.handleRightClick) 

            self.nextButton = ttk.Button(self.footer, text='Next', command=lambda: self.getInput())
            self.nextButton.grid(column=1, row=0)
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=lambda: self.closeImporter())
            self.cancelButton.grid(column=2, row=0)
        else:
            notification.create('error', 'Error opening file', 5000)
    
    def handleColCtrlSelection(self,e):
        col = self.dataTable.get_col_clicked(e)
        if col not in self.multiplecollist:
            self.multiplecollist.append(col)
        self.updateColumnText()

    def handleDragSelection(self, e):
        self.multiplecollist = []
        self.multiplerowlist = []
        # self.dataTable.clearSelected()

        if hasattr(self, 'cellentry'):
            self.dataTable.cellentry.destroy()
        rowover = self.dataTable.get_row_clicked(e)
        colover = self.dataTable.get_col_clicked(e)
        startcol = self.dataTable.getSelectedColumn()
        startrow = self.dataTable.getSelectedRows().index[0]

        print(f'STARTCOL {startcol}, COLOVER {colover}, STARTROW {startrow}, ROWOVER {rowover}')

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

        self.updateSelectionText(e)

    def updateDragText(self):
        rows = self.multiplerowlist
        cols = self.multiplecollist
        #print(f'ROWS: {rows}')
        #print(f'COLS: {cols}')
        self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]+1}-{cols[-1]+1}')
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

        self.updateColumnText()

    def handleRightClick(self, e):
        self.deselectAll()
        self.multiplecollist = []
        """ self.dataTable.selectNone()
        # Deselect column
        self.dataTable.setSelectedCol( -1 )
        self.dataTable.drawSelectedCol(-1)
        self.dataTable.tablecolheader.drawRect(-1)
        # Deselect row
        self.dataTable.setSelectedRow( -1 )
        self.dataTable.drawSelectedRow()
        self.dataTable.rowheader.clearSelected() """

        self.dataTable.drawSelectedRect(row=-1, col=-1, color='red')
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

        self.updateColumnText()

    def handleTableClick(self, e=None):
        col = self.dataTable.get_col_clicked(e)
        row = self.dataTable.get_row_clicked(e)
        self.multiplecollist = []
        self.multiplerowlist = []

        self.dataTable.delete('rect')
        self.dataTable.delete('multicellrect')
        self.deselectAll()

        self.dataTable.setSelectedRow(row)
        self.dataTable.setSelectedCol(col)
        self.dataTable.drawSelectedRect(row=row, col=col)
        self.dataTable.rowheader.drawRect(row)
        self.dataTable.tablecolheader.drawRect(col)

        self.updateSelectionText(e)

    def updateColumnText(self):
        cols = self.multiplecollist
        if len(cols) > 1:
            temp = cols[0]
            for i, c in enumerate(cols):
                if i != 0:
                    if c == temp+1:
                        self.selectionText.configure(text=f'Selected columns {cols[0]+1}-{cols[-1]+1}')
                    else:
                        text = 'Selected cols '
                        for i, c in enumerate(cols):
                            if i != len(cols)-1:
                                text += f'{c+1}, '
                            else:
                                text += f'{c+1}'

                        self.selectionText.configure(text=text)
                    temp = c
        else:
            self.selectionText.configure(text=f'Selected column {self.multiplecollist[0]+1}')

    def updateSelectionText(self, e=None):
        print('UPDATED CALLED')
        cols = self.multiplecollist
        rows = self.multiplerowlist
        cellX = self.dataTable.get_col_clicked(e)
        cellY = self.dataTable.get_row_clicked(e)
        print(f'COLS: {cols}, ROWS: {rows}')

        if len(rows) > 0 and len(cols) == 0: # only rows selected
            print('ONLY ROWS SELECTED')
            if len(rows) > 1:
                temp = rows[0]
                for i, r in enumerate(rows):
                    print(r)
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
            print('ONLY COLS SELECTED')
            if len(cols) > 1:
                temp = cols[0]
                for i, c in enumerate(cols):
                    if i != 0:
                        if c == temp+1:
                            self.selectionText.configure(text=f'Selected columns {cols[0]+1}-{cols[-1]+1}')
                        else:
                            text = 'Selected cols '
                            for i, c in enumerate(cols):
                                if i != len(cols)-1:
                                    text += f'{c+1}, '
                                else:
                                    text += f'{c+1}'

                            self.selectionText.configure(text=text)
                        temp = c
            else:
                self.selectionText.configure(text=f'Selected column {self.multiplecollist[0]+1}')
        elif len(cols) >= 1 and len(rows) >= 1: # multiple cells selected
            print('MULTIPLE CELLS SELECTED')
            self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]+1}-{cols[-1]+1}')
        else:
            print('SINGEL CELL SELECTED')
            self.selectionText.configure(text=f'Selected cell row {cellY+1} - col {cellX+1}')

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

    def getInput(self):
        print('GETTING INPUT')
        rowValues = self.dataTable.getSelectionValues()
        col = self.dataTable.getSelectedColumn()
        row = self.dataTable.getSelectedRow()
        rows = self.dataTable.getSelectedRows()
        nRows = self.dataTable.rows
        colValues = []
        columnNames = []

        for c in self.multiplecollist:
            self.dataTable.setSelectedCol(c)
            colValues.append(self.dataTable.getSelectionValues()[0])
            columnNames.append(self.dataTable.model.getColumnName(c))

        print(columnNames)
        print(colValues)
        print(rowValues)
        print(self.multiplerowlist)
        for i, c in enumerate(self.multiplecollist):
            for r in self.multiplerowlist:
                print(f'VALITUT: {colValues[i][r]}')
        
        print(f'Current selections: R{row}, C{col} - ROWS{rows.index}')
        print(f'Current list selections: R{self.multiplerowlist}, C{self.multiplecollist}')

        if col == -1 and row == -1: # nothing selected
            print('NOTHING SELECTED')
        else: # something selected
            if col == -1: # rows selected
                if len(rows) > 1 and col == -1:
                    print('USEAMPI RIVI')
                    print(rows)
                else:
                    print('YKSI RIVI')
                    print(rows)

            if row == -1: # cols selected
                if len(self.multiplecollist) > 1: # multiple columns
                    print('USEAMPI SARAKE')
                    print(colValues)
                    
                    if self.stage == 0: # ids
                        pass

                    elif self.stage == 1: # Loads
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            for j, l in enumerate(colValues):
                                load = test.createLoad()
                                load.setName(list(columnNames)[j]) # column name
                                load.getDetails().setValue('Load', l[i]) # set value
                    
                    elif self.stage == 2: # VO2
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('VO2', colValues[j][i])

                    elif self.stage == 3: # HR
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('HR', colValues[j][i])

                    elif self.stage == 4: # SV
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Sv', colValues[j][i])

                    elif self.stage == 5: # Q
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Q', colValues[j][i])

                    elif self.stage == 6: # Hb
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Hb', colValues[j][i])

                    elif self.stage == 7: # SaO2
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('SaO2', colValues[j][i])

                else: # one column
                    print('YKSI SARAKE')
                    print( colValues )

                    if self.stage == 0: # ids
                        for id in colValues[0]:
                            # Create subject, set its id, add a test, reset workloads
                            subject = Subject()
                            subject.setId(id)
                            subject.addTest()
                            subject.getTests()[0].workLoads = []
                            self.subjects.append(subject)
                    
                    elif self.stage == 1: # loads
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            for j, l in enumerate(colValues):
                                load = test.createLoad()
                                load.setName(list(columnNames)[j]) # column name
                                load.getDetails().setValue('Load', l[i]) # set value
                    
                    elif self.stage == 2: # VO2
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('VO2', colValues[0][i])
                    
                    elif self.stage == 3: # HR
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('HR', colValues[0][i])
                    
                    elif self.stage == 4: # SV
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Sv', colValues[0][i])
                    
                    elif self.stage == 5: # Q
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Q', colValues[0][i])

                    elif self.stage == 6: # Hb
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('Hb', colValues[0][i])

                    elif self.stage == 7: # SaO2
                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                details.setValue('SaO2', colValues[0][i])

                self.nextStage()

            if row >= 0 and col >= 0: # cells selected
                if len(self.multiplerowlist) > 1 or len(self.multiplecollist) > 1:
                    print('MULTIPLE CELLS SELECTED')
                    #print(values[0])
                    colList = self.multiplecollist
                    rowList = self.multiplerowlist

                    if self.stage == 0: # ids
                        for i, c in enumerate(self.multiplecollist):
                            for r in self.multiplerowlist:
                                # Create subject, set its id, add a test, reset workloads
                                subject = Subject()
                                subject.setId(colValues[i][r])
                                subject.addTest()
                                subject.getTests()[0].workLoads = []
                                self.subjects.append(subject)
                    
                    elif self.stage == 1: # loads

                        for s in self.subjects:
                            test = s.getTests()[0]

                            for i, r in enumerate(rowList):
                                columnName = self.dataTable.model.getColumnName(colList[i])
                                load = test.createLoad()
                                load.setName(columnName) # column name
                                load.getDetails().setValue('Load', colValues[i][r]) # set value
                    
                    elif self.stage == 2: # VO2

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[j])
                                details.setValue('VO2', value)

                    elif self.stage == 3: # HR

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[j])
                                details.setValue('HR', value)
                    
                    elif self.stage == 4: # SV

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[j])
                                details.setValue('Sv', value)

                    elif self.stage == 5: # Q

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[j])
                                details.setValue('Q', value)

                    elif self.stage == 6: # Hb

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[0])
                                details.setValue('Hb', value)

                    elif self.stage == 7: # SaO2

                        for i, s in enumerate(self.subjects):
                            test = s.getTests()[0]
                            loads = test.getWorkLoads()

                            for j, l in enumerate(loads):
                                details = l.getDetails()
                                value = self.dataTable.model.getValueAt(rowList[i], colList[j])
                                details.setValue('SaO2', value)

                                    
                else:
                    print('SINGLE CELL SELECTED')
                    value = self.dataTable.model.getValueAt(row, col)
                    columnName = self.dataTable.model.getColumnName(col)
                    print(f'SINGLE CELL VALUE: {value}')

                    if self.stage == 0: # ids
                        # Create subject, set its id, add a test, reset workloads
                        subject = Subject()
                        subject.setId(value)
                        subject.addTest()
                        subject.getTests()[0].workLoads = []
                        self.subjects.append(subject)

                    elif self.stage == 1: # loads
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.createLoad()
                        print(f'SINGLE CELL - COLUMNNAMES: {columnName}')
                        load.setName(columnName) # column name
                        load.getDetails().setValue('Load', value) # set value

                    elif self.stage == 2: # VO2
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('VO2', value) # set value

                    elif self.stage == 3: # HR
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('HR', value) # set value

                    elif self.stage == 4: # SV
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('Sv', value) # set value

                    elif self.stage == 5: # Q
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('Q', value) # set value

                    elif self.stage == 6: # Hb
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('Hb', value) # set value

                    elif self.stage == 7: # SaO2
                        s = self.subjects[0]
                        test = s.getTests()[0]
                        load = test.getWorkLoads()[0]
                        print(value)
                        load.getDetails().setValue('SaO2', value) # set value

                self.nextStage()

    def closeImporter(self):
        if hasattr(self, 'test'):
            del self.test
        self.window.destroy()

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

    def prevStage(self):
        self.stage -= 1

        if self.stage > 0:
                ttk.Button(self.footer, text='Prev', command=lambda: self.prevStage()).grid(column=0, row=0)
                ttk.Button(self.footer, text='Pass', command=lambda: print('PASS')).grid(column=2, row=0)
                self.cancelButton.grid(column=3, row=0)

        print(f'Backing up to stage: {self.stage}')
        for t in self.tests:
            print(t.getTestDetails())
        self.deselectAll()

        if self.stage == 0:
            self.instructionText.configure(text='Define ID column/row')
        elif self.stage == 1:
            self.instructionText.configure(text='Define loads row/column/cell')
        elif self.stage == 2: # -> VO2
            self.instructionText.configure(text='Define VO2 row/column/cell')
            """ print(self.tests[0].getWorkLoads()[0].getName())
            print(self.tests[0].getWorkLoads()[0].getDetails().Load)
            print(self.tests[0].getWorkLoads()[1].getName())
            print(self.tests[0].getWorkLoads()[1].getDetails().Load) """
        elif self.stage == 3: # -> HR
            print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            #print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define HR row/column/cell')
        elif self.stage == 4: # -> SV
            print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            #print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())

        elif self.stage == 5: # -> Q
            print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            #print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())

    def nextStage(self):
        self.stage += 1

        if self.stage > 0:
                ttk.Button(self.footer, text='Prev', command=lambda: self.prevStage()).grid(column=0, row=0)
                ttk.Button(self.footer, text='Pass', command=lambda: self.nextStage()).grid(column=2, row=0)
                self.cancelButton.grid(column=3, row=0)

        print(f'Advancing to stage: {self.stage}')
        
        for s in self.subjects:
            print(f'SUBJECT {s.id}')
            t = s.getTests()[0]
            print(t.getTestDetails())
        self.deselectAll()

        if self.stage == 1:
            self.instructionText.configure(text='Define loads row/column/cell')
        elif self.stage == 2: # -> VO2
            self.instructionText.configure(text='Define VO2 row/column/cell')
            #print(self.subjects[0].getTests()[0].getWorkLoads()[0].getName())
            #print(self.subjects[0].getTests()[0].getWorkLoads()[0].getDetails().Load)
            # print(self.subjects[0].getTests()[0].getWorkLoads()[1].getName())
            # print(self.subjects[0].getTests()[0].getWorkLoads()[1].getDetails().Load)

            #print(self.subjects[1].getTests()[0].getWorkLoads()[0].getName())
            #print(self.subjects[1].getTests()[0].getWorkLoads()[0].getDetails().Load)
            # print(self.subjects[1].getTests()[0].getWorkLoads()[1].getName())
            # print(self.subjects[1].getTests()[0].getWorkLoads()[1].getDetails().Load)
        elif self.stage == 3: # -> HR
            #print(self.subjects.getTests()[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.subjects.getTests()[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define HR row/column/cell')

        elif self.stage == 4: # -> SV
            # print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define SV row/column/cell')

        elif self.stage == 5: # -> Q
            # print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define Q row/column/cell')

        elif self.stage == 6: # -> Hb
            # print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define Hb row/column/cell')

        elif self.stage == 7: # -> SaO2
            # print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.instructionText.configure(text='Define SaO2 row/column/cell')

        elif self.stage == 8: # Finish
            print('FINALLY')
            # print(self.tests[0].getWorkLoads()[0].getDetails().getWorkLoadDetails())
            # print(self.tests[0].getWorkLoads()[1].getDetails().getWorkLoadDetails())
            self.importData()

    def importData(self):
        # print(f'SUBJECTS {self.subjects}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()[0].getDetails().getWorkLoadDetails()}')
        # print(f'LAST SUBJECT LOADS {self.subjects[0].getTests()[0].getWorkLoads()[1].getDetails().getWorkLoadDetails()}')
        project = Project()
        app.setActiveProject(project)
        app.setActiveSubject(None)
        app.setActiveTest(None)

        for s in self.subjects:
            project.addSubject(s)

        app.sidepanel_projectList.refreshList()
        app.sidepanel_subjectList.refreshList()
        app.sidepanel_testList.refreshList()

        # Update app state
        app.sidepanel_projectList.addToList(project.id)
        app.addProject(project)

        self.window.destroy()

class DataMenuElem(object):
    def __init__(self, importer, menu, menuButton, option):
        self.importer = importer
        self.menuButton = menuButton
        self.option = option
        menu.add_command(label=option, command=lambda: self.handleMenuSelect())

    def handleMenuSelect(self):
        self.menuButton.config(text=self.option)
        self.importer.updateTable(self.option)