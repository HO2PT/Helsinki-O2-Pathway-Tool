from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.filedialog import askopenfile
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
# Stage 14: T
# Stage 15: pH

# Luo vaihtoehdot tuo projekti, tuo käyttäjä, tuo testi
# tuodessa testiä lisätään aktiivisen käyttäjän alle jnejne.

class DataImporter(object):
    def __init__(self):
        self.multiplecells = []
        self.stage = 0
        self.atdivider = None
        self.tests = []
        self.subjects = {}
        self.currentDf = None
        self.tempLocData = {}
        self.dataMode = None
        self.addLinearDist = False
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
            15: False
        }

        file = askopenfile(mode ='r')
        if file is not None:
            self.data = pd.ExcelFile(file.name)
            self.dfList= {}

            for sheet in self.data.sheet_names:
                self.dfList[sheet] = pd.read_excel(self.data, sheet, header=None)

            self.window = Toplevel()
            self.window.title('Import')
            self.window.geometry('750x500')
            self.window.update_idletasks()
            windowX = int(self.window.winfo_screenwidth()) * 0.5 - int(self.window.winfo_width()) * 0.5
            windowY = int(self.window.winfo_screenheight()) * 0.5 - int(self.window.winfo_height()) * 0.5
            self.window.geometry("+%d+%d" % ( windowX, windowY ))

            ####
            self.window.bind('a', lambda e: print(self.dataTable.multiplerowlist, self.dataTable.multiplecollist))
            ####

            # Left panel
            self.leftPanel = ttk.Frame(self.window, padding=(5,5))
            self.leftPanel.pack(side=LEFT, fill=Y)

            # Scrollbar
            self.yScroll = ttk.Scrollbar(self.leftPanel, orient=VERTICAL)
            self.yScroll.pack(side=RIGHT, fill=Y)

            ## Font
            bolded = font.Font(weight='bold')

            # Progression
            ttk.Label(self.leftPanel, text='Data import steps').pack()
            self.progressionList = Listbox(self.leftPanel, yscrollcommand=self.yScroll.set)
            self.progressionList.insert('end', 'ID * \U0001F878')
            self.progressionList.insert('end', 'Load *')
            self.progressionList.insert('end', 'VO\u2082 *')
            self.progressionList.insert('end', 'HR *')
            self.progressionList.insert('end', 'SV *')
            self.progressionList.insert('end', 'Q *')
            self.progressionList.insert('end', '[Hb] *')
            self.progressionList.insert('end', 'SaO\u2082 *')
            self.progressionList.insert('end', 'CaO\u2082')
            self.progressionList.insert('end', 'CvO\u2082')
            self.progressionList.insert('end', 'CavO\u2082')
            self.progressionList.insert('end', 'QaO\u2082')
            self.progressionList.insert('end', 'SvO\u2082')
            self.progressionList.insert('end', 'PvO\u2082')
            self.progressionList.insert('end', 'T')
            self.progressionList.insert('end', 'pH')
            self.progressionList.pack(expand=1, fill=BOTH)
            self.progressionList.bind( '<<ListboxSelect>>', lambda e: self.handleListboxSelect(e) )

            self.yScroll['command'] = self.progressionList.yview

            # Right panel
            self.rightPanel = ttk.Frame(self.window, padding=(5,5))
            self.rightPanel.pack(side=RIGHT, fill=BOTH, expand=1)

            # Notification bar
            notifFrame = ttk.Frame(self.rightPanel)
            notifFrame.pack(fill=X)
            self.notif = ttk.Label(notifFrame, text='', anchor='center', foreground='white')
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
            # self.dataTable.currentcol = None
            # self.dataTable.currentrow = None
            self.dataTable.setSelectedCol(-1)
            self.dataTable.setSelectedRow(-1)
            self.dataTable.multiplerowlist = []
            self.dataTable.multiplecollist = []
            
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
            self.dataTable.bind('<MouseWheel>', self.handleMouseWheel)

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

            ##
            self.dataTable.Yscrollbar['command'] = set_yviews
            self.dataTable.Xscrollbar['command'] = set_xviews
            # self.Yscrollbar = AutoScrollbar(self.parentframe,orient=VERTICAL,command=self.set_yviews)
            # self.Yscrollbar.grid(row=1,column=2,rowspan=1,sticky='news',pady=0,ipady=0)
            # self.Xscrollbar = AutoScrollbar(self.parentframe,orient=HORIZONTAL,command=self.set_xviews)
            # self.Xscrollbar.grid(row=2,column=1,columnspan=1,sticky='news')
            ##

            self.nextButton = ttk.Button(self.footer, text='Next', command=lambda: self.getInput())
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=lambda: self.closeImporter())

            self.cancelButton.pack(side=RIGHT)
            self.nextButton.pack(side=RIGHT)
        else:
            notification.create('error', 'Error opening file', 5000)

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
        # self.handleRightClick() # deselect all
        self.deselectAll()

        if selMode == 'row':
            if start-1 < 0:
                self.notif.configure(text='Start row index out of range', background='red', foreground='#333333')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            elif end > self.dataTable.rows:
                self.notif.configure(text='End row index out of range', background='red', foreground='#333333')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            else:
                for i in range(start-1, end):
                    self.dataTable.multiplerowlist.append(i)
                    self.dataTable.rowheader.drawRect(row=i, delete=False)
                self.dataTable.drawMultipleRows(self.dataTable.multiplerowlist)
        else: # cols
            if start < 0:
                self.notif.configure(text='Start column index out of range', background='red', foreground='#333333')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            elif end > self.dataTable.cols:
                self.notif.configure(text='End column index out of range', background='red', foreground='#333333')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
            else:
                for i in range(start, end):
                    self.dataTable.multiplecollist.append(i)
                self.dataTable.multiplecollist.append(end)

                for c in self.dataTable.multiplecollist:
                    self.dataTable.drawSelectedCol(c, delete=False)
                    self.dataTable.tablecolheader.drawRect(c, delete=False)

        # print(f'MASS SELECTION R{self.dataTable.multiplerowlist}, C{self.dataTable.multiplecollist}')
        self.updateSelectionText()

    def handleTableClick(self, e=None):
        pass
        """ print('handle LEFT click')
        col = self.dataTable.get_col_clicked(e)
        row = self.dataTable.get_row_clicked(e)
        self.dataTable.multiplecollist = []
        self.multiplerowlist = []
        self.multiplecells = []
        self.dataTable.delete('ctrlSel')

        self.dataTable.delete('rect')
        self.dataTable.delete('multicellrect')
        self.deselectAll()

        ##
        self.multiplecells.append(self.dataTable.model.getValueAt(row, col))
        self.dataTable.multiplecollist.append(col)
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
            if r == row and self.dataTable.multiplecollist[i] == col:
                isSelected = True
                self.dataTable.drawRect(row=row, col=col, delete=1)
                del self.multiplerowlist[i]
                del self.dataTable.multiplecollist[i]

        if isSelected == False:
            self.multiplecells.append(self.dataTable.model.getValueAt(row, col))
            self.dataTable.multiplecollist.append(col)
            self.multiplerowlist.append(row)

            for i, c in enumerate(self.dataTable.multiplecollist):
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

    def handleDragSelection(self, e):
        pass
        """ self.dataTable.multiplecollist = []
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
                self.dataTable.multiplecollist=list(range(self.dataTable.endcol, startcol+1))
            else:
                self.dataTable.multiplecollist=list(range(startcol, self.dataTable.endcol+1))

        for c in self.dataTable.multiplecollist:
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
            if len(self.dataTable.multiplecollist) >= 1:
                self.drawMultipleCells()
            self.dataTable.delete('multiplesel')

        self.updateSelectionText(e) """

    def updateDragText(self):
        rows = self.dataTable.multiplerowlist
        cols = self.dataTable.multiplecollist
        #print(f'ROWS: {rows}')
        #print(f'COLS: {cols}')
        self.selectionText.configure(text=f'Selected rows: {rows[0]+1}-{rows[-1]+1} cols: {cols[0]}-{cols[-1]}')
        pass

    def drawMultipleCells(self):
        """Draw an outline box for multiple cell selection"""

        self.dataTable.delete('currentrect')
        self.dataTable.delete('multicellrect')
        
        rows = self.dataTable.multiplerowlist
        cols = self.dataTable.multiplecollist
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

        for c in self.dataTable.multiplecollist:
            self.dataTable.drawSelectedCol(c, delete=False)
            self.dataTable.tablecolheader.drawRect(c, delete=False)

        # self.updateColumnText()
        self.updateSelectionText()

    def handleRightClick(self, e = None):
        self.deselectAll()
        # self.dataTable.multiplecollist = []
        # self.dataTable.multiplerowlist = []
        # self.multiplecells = []
        # self.dataTable.delete('ctrlSel')
        # self.dataTable.delete('currentrect')
        # self.dataTable.delete('multicellrect')
        # self.dataTable.delete('colrect')
        # self.dataTable.tablecolheader.delete('rect')

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
        self.dataTable.multiplecollist = []
        col = self.dataTable.get_col_clicked(e)
        self.deselectAll()

        # Select column
        self.dataTable.setSelectedCol( col )
        self.dataTable.drawSelectedCol( col=col )
        self.dataTable.tablecolheader.drawRect(col=col)
        # self.dataTable.multiplecollist.append(col)

        self.updateSelectionText()

    def updateSelectionText(self):
        cols = self.dataTable.multiplecollist
        rows = self.dataTable.multiplerowlist
        # print(f'COLS: {cols}, ROWS: {rows}')

        if len(rows) > 0 and len(cols) == 0: # only rows selected
            if len(rows) > 1:
                temp = rows[0]
                for i, r in enumerate(rows):
                    # print(r)
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
        """ self.deselectAll()
        row = self.dataTable.get_row_clicked(e)
        rows = self.dataTable.getSelectedRows()
        # self.handleRightClick()
        #print(f'Selected rows {rows}')

        if len(rows.index) == 1: # if single row selected
            row = self.dataTable.get_row_clicked(e)

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
                    temp = r """

    def checkDataForm(self):
        # print(f'len collist: {len(self.dataTable.multiplecollist)}')
        # print(f'len rowlist: {len(self.dataTable.multiplerowlist)}')
        # print(f'selected rows: {len(self.dataTable.getSelectedRows())}')
        if len(self.dataTable.multiplecollist) > 1 and len(self.dataTable.multiplerowlist) > 1:

            if self.dataTable.multiplecollist[0] == self.dataTable.multiplecollist[1]:
                print('PITKÄ MUOTO')
                self.dataMode = 'long'
            elif self.dataTable.multiplerowlist[0] == self.dataTable.multiplerowlist[1]:
                print('LEVEÄ MUOTO')
                self.dataMode = 'wide'

        elif len(self.dataTable.multiplecollist) > 1 or (len(self.dataTable.multiplecollist) == 0 and len(self.dataTable.getSelectedRows()) > 0):
            print('LEVEÄ MUOTO')
            self.dataMode = 'wide'
        else:
            print('PITKÄ MUOTO')
            self.dataMode = 'long'

    def nextOptions(self, value):
        # col = self.dataTable.getSelectedColumn()
        # row = self.dataTable.getSelectedRow()
        colList = self.dataTable.multiplecollist
        rowList = self.dataTable.multiplerowlist

        print(f'nextOptions {colList, rowList}')
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
        # print(f'nextOptions datamode: {self.dataMode}')
        self.options.destroy()

    def closeOptions(self):
        self.closedByClick = True
        self.options.destroy()

    def getInput(self):
        # print('GETTING INPUT')

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

        if self.stage == 0 and (len(colList) == 1 or len(rowList) == 1 or len(rows) == 1):# and row != -1):
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
        
        # print(f'Current selections: R{row}, C{col} - ROWS{rows.index}')
        # print(f'Current list selections: R{rowList}, C{colList}')
        # print(f'STAGE {self.stage}')
        # print(f'DATAMODE: {self.dataMode}')

        if (len(rowList) < 1 and len(colList) < 1): # nothing selected
            #print('NOTHING SELECTED')
            # s = ttk.Style()
            # s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
            self.notif.configure(background='red', foreground="#333333", text=f'Nothing selected')
            self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
        elif self.closedByClick == True:
            pass
        else: # something selected
            print('SOMETHING SELECTED')
            try:
                if len(rowList) > 0: # rows selected
                    if self.stage == 0: # ids
                        # Reset subjects if returned
                        self.subjects = {}

                        if len(rows) > 1 and col == -1: # multiple rows
                            # print('USEAMPI RIVI')
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
                                self.dataMode = 'long'
                                success = True

                        else: # single rows
                            # print('YKSI RIVI')
                            # print(rows)
                            # print(self.rowNames)
                            if self.stage == 0: #ids
                                if self.dataMode == None:
                                    self.checkDataForm()
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
                        # print('**LOADS**')
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
                        success = self.getRowValues('[Hb]')

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
                        success = self.getRowValues('C(a-v)O2')

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
                        # print(f'dataMode: {self.dataMode}')
                        self.addCheckMark(self.stage)
                        self.notif.configure(text='OK', background='green', foreground='white')
                        self.notif.after(1000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                        self.nextStage(imported=self.stage)

                if len(colList) > 0: # cols selected
                    if self.stage == 0: #ids
                        if len(colList) > 1: # multiple columns
                            # print('USEAMPI SARAKE')

                            # Reset subjects if returned
                            self.subjects = {}
                                
                            # self.checkDataForm()
                            for i, id in enumerate(self.columnNames):
                                # Create subject, set its id, add a test, reset workloads
                                subject = Subject()
                                subject.setId(id)
                                subject.addTest()
                                subject.getTests()[0].workLoads = []
                                # self.subjects.append(subject)
                                colIndex = colList[i]
                                self.subjects[colIndex] = subject

                            # print(self.subjects)
                            success = True
                            self.dataMode = 'wide'
                            # self.tempLocData['id'] = self.columnNames

                        else: # one column
                            # print('YKSI SARAKE')

                            if self.dataMode == None:
                                self.checkDataForm()
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
                                    colIndex = colList[i]
                                    self.subjects[colIndex] = subject

                            # print(self.subjects)
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
                        success = self.getColumnValues('[Hb]')

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
                        success = self.getColumnValues('C(a-v)O2')

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
                        print(f'dataMode: {self.dataMode}')
                        self.addCheckMark(self.stage)
                        self.notif.configure(text='OK', background='green', foreground='white')
                        self.notif.after(1000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
                        self.nextStage(imported=self.stage)

            except Exception as e:
                print(f'EXCEPTION {e}')
                # s = ttk.Style()
                # s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                self.notif.configure(text=f'ID information needed to import data', background='red', foreground='#333333')
                self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))

    def closeImporter(self):
        if hasattr(self, 'test'):
            del self.test
        self.window.destroy()
        try:
            self.options.destroy()
        except:
            pass
        del self

    def updateTable(self, table):
        self.dataTable.updateModel(TableModel(self.dfList[table]))
        self.dataTable.redraw()

    def deselectAll(self):
        self.dataTable.clearSelected()
        self.dataTable.multiplecollist = []
        self.dataTable.multiplerowlist = []
        # self.dataTable.setSelectedCol( -1 )
        self.dataTable.drawSelectedCol(-1)
        self.dataTable.tablecolheader.drawRect(-1)
        # self.dataTable.setSelectedRow( -1 )
        
        # self.dataTable.drawSelectedRow()
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
                    # s = ttk.Style()
                    # s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(text=f'You have {len(loads)} loads but only {len(self.colValues)} values given', background='red', foreground='#333333')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
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
                    # s = ttk.Style()
                    # s.configure('error.TLabel', background='red', foreground="white", anchor="CENTER")
                    self.notif.configure(text=f'You have {len(loads)} loads but only {len(self.rowValues)} values given', background='red', foreground='#333333')
                    self.notif.after(5000, lambda: self.notif.configure(text='', background=self.window.cget('background')))
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

    def prevStage(self):
        self.deselectAll()
        to = self.stage - 1
        self.nextStage(to=to)

    def nextStage(self, to=None, imported=None, skipped=None):
        if imported != None:
            self.imported[imported] = True
            print(f'IMPORTED SUCCESSFULLY: {self.imported}')

        if to == None:
            # self.stage += 1 
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
            self.doneBtn = ttk.Button(self.footer, text='Done', command=lambda: self.importData())
            self.doneBtn.pack(side=RIGHT)
            self.prevBtn = ttk.Button(self.footer, text='Prev', command=lambda: self.prevStage())
            self.prevBtn.pack(side=RIGHT)
            self.passBtn = ttk.Button(self.footer, text='Skip', command=lambda: self.nextStage(skipped=self.stage))
            self.passBtn.pack(side=RIGHT)
            self.nextButton.pack(side=RIGHT)
            
        if skipped == 14 or skipped == 15:
            self.addLinearDist = True

        self.deselectAll()

        if to == 0:
            self.moveArrow(self.stage, to)
            self.instructionText.configure(text='Define ID(s) column/row')
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
            self.instructionText.configure(text='Define [Hb] row/column')
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
            self.passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define T row/column')
        elif to == 15: # -> pH
            self.moveArrow(self.stage, to)
            self.passBtn.configure(text='Use Default Values')
            self.instructionText.configure(text='Define pH row/column')
        elif to == 16: # Finish
            self.importData()

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
        # print(f'adding mark to {to}')
        value = self.progressionList.get(to)
        if '\u2713' not in value:
            value = f'{value} \u2713'
        # print(value)
        self.progressionList.delete(to)
        self.progressionList.insert(to, value)

    def importData(self):
        project = Project()
        app.setActiveProject(project)
        app.setActiveSubject(None)
        app.setActiveTest(None)

        project.data = self.dfList

        # Add dataloc information
        project.dataMode = self.dataMode
        project.idLoc = self.tempLocData.get('id', None)
        project.loadLoc = self.tempLocData.get('Load', None)
        # project.vo2Loc = self.tempLocData.get('VO2', None)
        # project.hrLoc = self.tempLocData.get('HR', None)
        # project.svLoc = self.tempLocData.get('SV', None)

        # project.qLoc = self.tempLocData.get('Q', None)
        # project.hbLoc = self.tempLocData.get('[Hb]', None)
        # project.sao2Loc = self.tempLocData.get('SaO2', None)
        # project.cao2Loc = self.tempLocData.get('CaO2', None)
        # project.cvo2Loc = self.tempLocData.get('CvO2', None)

        # project.cavo2Loc = self.tempLocData.get('C(a-v)O2', None)
        # project.qao2Loc = self.tempLocData.get('QaO2', None)
        # project.svo2Loc = self.tempLocData.get('SvO2', None)
        # project.pvo2Loc = self.tempLocData.get('PvO2', None)

        # project.tcRestLoc = self.tempLocData.get('Tc @ rest', None)
        # project.tcLoc = self.tempLocData.get('Tc\u209A\u2091\u2090\u2096', None)
        # project.phRestLoc = self.tempLocData.get('pH @ rest', None) 
        # project.phLoc = self.tempLocData.get('pH\u209A\u2091\u2090\u2096', None)
        
        # for key, value in self.dfList.items():
        #     print(key)
        #     print(value)

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

        if self.imported[14] == False or self.imported[15] == False:
            self.addLinearDist = True

        # Add linear distribution of pH and T
        if self.addLinearDist:
            for s in project.subjects:
                for t in s.tests:
                    self.updatePhAndTemp(t)

        self.window.destroy()
        del self

    def updatePhAndTemp(self, test):
        # Add linear change in pH and T
        pHrest = float(app.settings.testDefaults['pH @ rest'])
        Trest = float(app.settings.testDefaults['Tc @ rest'])
        pHpeak = float(app.settings.testDefaults['pH\u209A\u2091\u2090\u2096'])
        Tpeak = float(app.settings.testDefaults['Tc\u209A\u2091\u2090\u2096'])
        pHDif = float(pHrest) - float(pHpeak)
        Tdif = float(Tpeak) - float(Trest)

        # Filter possible empty loads
        nFilteredLoads = 0
        for i, l in enumerate(test.workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
                        
            if i == 0 or detailsDict['Load'] != 0:
                nFilteredLoads += 1

        if nFilteredLoads > 1:
            if pHrest != pHpeak:
                test.getWorkLoads()[-1].getDetails().setValue('pH', pHpeak)

            if Trest != Tpeak:
                test.getWorkLoads()[-1].getDetails().setValue('T', Tpeak)

            pHstep = pHDif / (nFilteredLoads-1)
            Tstep = Tdif / (nFilteredLoads-1)
        else:
            pHstep = 0
            Tstep = 0

        # Add linear change
        for i, w in enumerate(test.getWorkLoads()):
            details = w.getDetails()
            pHValue = pHrest - (i * pHstep)
            details.setValue('pH', f'{"{0:.2f}".format(pHValue)}')

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

""" if row >= 0 and col >= 0: # cells selected
                if len(self.multiplerowlist) > 1 or len(self.dataTable.multiplecollist) > 1: # multiple cells
                    print('MULTIPLE CELLS SELECTED')

                    if self.stage == 0: # ids
                        # self.checkDataForm()
                        self.subjects = {}

                        if self.dataMode == 'wide':
                            for i, c in enumerate(self.dataTable.multiplecollist):
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
                                if len(self.dataTable.multiplecollist) == 1:
                                    for c in self.dataTable.multiplecollist:
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
                        if self.dataMode == 'long':
                            load.setName(rowName) # row name
                        elif self.dataMode == 'wide':
                            load.setName(columnName) # column name
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
                    self.nextStage() """

""" def getMultiCellLoads(self):
        colList = self.dataTable.multiplecollist
        rowList = self.dataTable.multiplerowlist

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

                for ri, r in enumerate(rowList):
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
                    load.getDetails().setImported(True)

                if len(rowList) == 1 or all(rowList[0] == col for col in rowList): # single row
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
                    continue

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
                for ci, c in enumerate(colList):
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
                    load.getDetails().setImported(True)

                if len(rowList) == 1: # if selected by dragging or shift
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
                    continue

            self.tempLocData['Load'] = self.colValues

    def getMultiCellValues(self, label):
        colList = self.dataTable.multiplecollist
        rowList = self.dataTable.multiplerowlist
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
        return True """