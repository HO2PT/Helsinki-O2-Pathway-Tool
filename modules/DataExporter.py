import os
from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.notification import notification
from modules.DataImporter import DataMenuElem
from tkinter.filedialog import asksaveasfile
import pandas as pd

##
## TO-DO: 
# wide data?
# select sheet or create new sheet
# add plot images?
# finalize exporttonew
##

class DataExporter(object):
    def __init__(self, mode):
        # 0 = create new file
        # 1 = save to existing file
        if mode == 0:
            self.exportToNew()
        else:
            self.showOptions()

    def exportToNew(self):
        print('exporting to new')
        data = []
        temp= []
        imgs = []
        
        for i, p in enumerate(app.getPlottingPanel().plots):
            #print(f'PLOT: {p.plot}')
            #print(f'TEST: {p.activeTest}')
            #print(f'LOADS: {p.workLoads}')
            #print(f'DETAILS: {p.workLoads[0].getDetails().getWorkLoadDetails()}')
            details = p.workLoads[0].getDetails().getWorkLoadDetails()
            img = p.plot[0].savefig(f'plot{i}.png')
            imgs.append( img )

            for d in p.workLoads:
                details = d.getDetails().getWorkLoadDetails()
                i = 0

                hints = [
                    'id',
                    'Load',
                    'VO2',
                    'HR',
                    'Sv',
                    'Q',
                    'Hb',
                    'SaO2',
                    'CaO2',
                    'CvO2',
                    'CavO2',
                    'QaO2',
                    'SvO2',
                    'PvO2',
                    'Tc @ rest',
                    'Tc\u209A\u2091\u2090\u2096',
                    'pH @ rest',
                    'pH\u209A\u2091\u2090\u2096',
                    'DO2',
                    ]
                
                for h in hints:
                    label = None
                    val = None
                    unit = None
                    mc = None

                    try:
                        label = h
                        val = details[h]
                        unit = details[f'{h}_unit']
                        mc = details[f'{h}_MC']

                        data.append([ label, val, unit, mc ])
                        
                    except KeyError:
                        if unit == None and mc == None:
                            data.append([ label, val, '', '' ])
                        elif mc == None:
                            data.append([ label, val, unit, '' ])


                # Iterate through load details and print to Details module
                
                data.append(['','','',''])
        
        # Create the pandas DataFrame
        df = pd.DataFrame(data, columns = ['','Value', 'Unit', 'Meas(0)/Calc(1)'])
        # Create excel
        saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
        fileName = saveFile.name.split('/')[-1]
        writer = pd.ExcelWriter(f'{fileName}.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        asd = ['F1', 'K1', 'Q1']
        # Add plot images
        for i, im in enumerate(imgs):
            imgDest = f'{os.getcwd()}/plot{i}.png'
            worksheet.insert_image(asd[i], imgDest)
        
        writer.save()
        notification.create('info', 'Data successfully exported', 5000)

    def showOptions(self):

        # try:
            excel = app.getActiveProject().data
        
            self.exportOptions = Toplevel()
            self.exportOptions.title("Export options")
            self.exportOptions.geometry("500x500")

            settingsX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/1.5)
            settingsY = app.root.winfo_rooty() + (app.root.winfo_reqheight()*0.1)
            self.exportOptions.geometry("+%d+%d" % ( settingsX, settingsY ))

            ttk.Label(self.exportOptions, text='Choose values to be exported').pack()
            container = ttk.Frame(self.exportOptions)
            container.pack(anchor='center')

            self.vars = []

            vo2Var = IntVar(value=1, name="VO2")
            self.vars.append(vo2Var)
            ttk.Checkbutton(container, text='VO2', variable=vo2Var).grid(column=0, row=0, sticky='nw')

            qVar = IntVar(value=1, name="Q")
            self.vars.append(qVar)
            ttk.Checkbutton(container, text='Q', variable=qVar).grid(column=0, row=1, sticky='nw')

            cao2Var = IntVar(value=1, name="CaO2")
            self.vars.append(cao2Var)
            ttk.Checkbutton(container, text='CaO2', variable=cao2Var).grid(column=0, row=2, sticky='nw')

            cvo2Var = IntVar(value=1, name="CvO2")
            self.vars.append(cvo2Var)
            ttk.Checkbutton(container, text='CvO2', variable=cvo2Var).grid(column=0, row=3, sticky='nw')

            cavo2Var = IntVar(value=1, name="CavO2")
            self.vars.append(cavo2Var)
            ttk.Checkbutton(container, text='CavO2', variable=cavo2Var).grid(column=0, row=4, sticky='nw')

            qao2Var = IntVar(value=1, name="QaO2")
            self.vars.append(qao2Var)
            ttk.Checkbutton(container, text='QaO2', variable=qao2Var).grid(column=0, row=5, sticky='nw')

            svo2Var = IntVar(value=1, name="SvO2")
            self.vars.append(svo2Var)
            ttk.Checkbutton(container, text='SvO2', variable=svo2Var).grid(column=0, row=6, sticky='nw')

            pvo2Var = IntVar(value=1, name="PvO2")
            self.vars.append(pvo2Var)
            ttk.Checkbutton(container, text='PvO2', variable=pvo2Var).grid(column=0, row=7, sticky='nw')

            do2Var = IntVar(value=1, name="DO2")
            self.vars.append(do2Var)
            ttk.Checkbutton(container, text='DO2', variable=do2Var).grid(column=0, row=8, sticky='nw')

            ttk.Button(container, text='asd', command=lambda: getSelected()).grid(column=1, row=9)

            self.sheetNames = []
            for key, value in excel.items():
                self.sheetNames.append(key)

            # Create menubutton for selection of excel sheet
            self.menuButton = ttk.Menubutton(container, text=self.sheetNames[0])
            menu = Menu(self.menuButton, tearoff=False)

            for s in self.sheetNames:
                DataMenuElem(self, menu, self.menuButton, s, isExporter=True)

            self.menuButton['menu'] = menu
            self.menuButton.grid(column=0, row=10)

            self.varTemp = []
            def getSelected():
                for v in self.vars:
                    if v.get() == 1:
                        self.varTemp.append(str(v))
                self.vars = self.varTemp
                self.selectedSheet = self.menuButton.cget('text')
                self.exportToSelected()
        # except:
        #     notification.create('error', 'No imported file detected. Data input by hand?', 5000)

    def exportToSelected(self):
        print('exporting to existing')
        temp= {}
        imgs = []

        excel = app.getActiveProject().data

        # Get number of loads in project
        p = app.getActiveProject()
        try:
            nLoads = len(p.loadLoc)
        except:
            n = []
            subjects = p.getSubjects()
            for s in subjects:
                tests = s.getTests()
                for t in tests:
                    n.append(len(t.getWorkLoads()))
            nLoads = max(n)

        # Initialize lists that hold the values and are to be
        # saved as columns
        for i in range(nLoads):
            for v in self.vars:
                temp[f'{v}-{i+1}'] = []

        units = {}

        subjects = p.getSubjects()
        for s in subjects:
            tests = s.getTests()
            for t in tests:
                loads = t.getWorkLoads()
                for i in range(nLoads):
                    try:
                        details = loads[i].getDetails().getWorkLoadDetails()
                        app.getPlottingPanel().calc(loads[i], details)
                        updatedDetails = loads[i].getDetails().getWorkLoadDetails()

                        for v in self.vars:
                            value = updatedDetails[v]
                            unit = updatedDetails[f'{v}_unit']
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit
                    except:
                        for v in self.vars:
                            value = 0
                            unit = updatedDetails[f'{v}_unit']
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit

        # Sort values
        ordered = {}
        for v in self.vars:
            for key, value in temp.items():
                if key.startswith(v):
                    ordered[key] = value

        for key, value in ordered.items():
            unit = units[f'{key.split("-")[0]}']
            value.insert(0, f'{key} ({unit})')
            excel[self.selectedSheet][key] = value

        # for i, p in enumerate(app.getPlottingPanel().plots):
        #     # img = p.plot[0].savefig(f'plot{i}.png')
        #     # imgs.append( img )

        #     for l in p.workLoads:
        #         details = l.getDetails().getWorkLoadDetails()
        #         i = 0

        #         # Iterate through load details and print to Details module
        #         for key, value in details.items():
        #             if i == 3:
        #                 label = temp[0][0]
        #                 val = temp[0][1]
        #                 unit = temp[1][1]
        #                 mc = temp[2][1]
        #                 data.append( [label, val, unit, mc] )
        #                 temp=[]
        #                 i = 0
                        
        #             temp.append([key,value])
        #             i = i + 1

        saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
        # workbook  = writer.book
        # worksheet = writer.sheets[self.selectedSheet]

        with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
            for sheet in self.sheetNames:
                df = pd.DataFrame.from_dict(excel[sheet])
                df.to_excel(writer, sheet_name=sheet, index=False, header=False)

        """ asd = ['F1', 'K1', 'Q1']
        # Add plot images
        for i, im in enumerate(imgs):
            imgDest = f'{os.getcwd()}/plot{i}.png'
            worksheet.insert_image(asd[i], imgDest) """
            
        writer.save()
        notification.create('info', 'Data successfully exported', 5000)
        self.exportOptions.destroy()