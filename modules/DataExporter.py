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
# select sheet or create new sheet
# add plot images?
#
##

class DataExporter(object):
    def __init__(self, toNew, onlyPlots=False):
        # 0 = save to existing file
        # 1 = create new file
        self.toNew = toNew
        self.onlyPlots = onlyPlots
        self.showOptions()

    def showOptions(self):
        try:
            if self.toNew == False:
                self.importDataMode = app.getActiveProject().dataMode
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

            hbVar = IntVar(value=1, name="Hb")
            self.vars.append(hbVar)
            ttk.Checkbutton(container, text='Hb', variable=hbVar).grid(column=0, row=1, sticky='nw')

            sao2Var = IntVar(value=1, name="SaO2")
            self.vars.append(sao2Var)
            ttk.Checkbutton(container, text='SaO2', variable=sao2Var).grid(column=0, row=2, sticky='nw')

            qVar = IntVar(value=1, name="Q")
            self.vars.append(qVar)
            ttk.Checkbutton(container, text='Q', variable=qVar).grid(column=0, row=3, sticky='nw')

            cao2Var = IntVar(value=1, name="CaO2")
            self.vars.append(cao2Var)
            ttk.Checkbutton(container, text='CaO2', variable=cao2Var).grid(column=0, row=4, sticky='nw')

            cvo2Var = IntVar(value=1, name="CvO2")
            self.vars.append(cvo2Var)
            ttk.Checkbutton(container, text='CvO2', variable=cvo2Var).grid(column=0, row=5, sticky='nw')

            cavo2Var = IntVar(value=1, name="CavO2")
            self.vars.append(cavo2Var)
            ttk.Checkbutton(container, text='CavO2', variable=cavo2Var).grid(column=0, row=6, sticky='nw')

            qao2Var = IntVar(value=1, name="QaO2")
            self.vars.append(qao2Var)
            ttk.Checkbutton(container, text='QaO2', variable=qao2Var).grid(column=0, row=7, sticky='nw')

            svo2Var = IntVar(value=1, name="SvO2")
            self.vars.append(svo2Var)
            ttk.Checkbutton(container, text='SvO2', variable=svo2Var).grid(column=0, row=8, sticky='nw')

            pvo2Var = IntVar(value=1, name="PvO2")
            self.vars.append(pvo2Var)
            ttk.Checkbutton(container, text='PvO2', variable=pvo2Var).grid(column=0, row=9, sticky='nw')

            do2Var = IntVar(value=1, name="DO2")
            self.vars.append(do2Var)
            ttk.Checkbutton(container, text='DO2', variable=do2Var).grid(column=0, row=10, sticky='nw')

            tcRestVar = IntVar(value=1, name="Tc @ rest")
            self.vars.append(tcRestVar)
            ttk.Checkbutton(container, text='Tc @ rest', variable=tcRestVar).grid(column=0, row=11, sticky='nw')

            tcVar = IntVar(value=1, name="Tc\u209A\u2091\u2090\u2096")
            self.vars.append(tcVar)
            ttk.Checkbutton(container, text='Tc\u209A\u2091\u2090\u2096', variable=tcVar).grid(column=0, row=12, sticky='nw')

            phRestVar = IntVar(value=1, name="pH @ rest")
            self.vars.append(phRestVar)
            ttk.Checkbutton(container, text='pH @ rest', variable=phRestVar).grid(column=0, row=13, sticky='nw')

            phVar = IntVar(value=1, name="pH\u209A\u2091\u2090\u2096")
            self.vars.append(phVar)
            ttk.Checkbutton(container, text='pH\u209A\u2091\u2090\u2096', variable=phVar).grid(column=0, row=14, sticky='nw')

            ttk.Button(container, text='asd', command=lambda: getSelected()).grid(column=1, row=15)

            if self.toNew == False:
                self.sheetNames = []
                for key, value in excel.items():
                    self.sheetNames.append(key)

                # Create menubutton for selection of excel sheet
                self.menuButton = ttk.Menubutton(container, text=self.sheetNames[0])
                menu = Menu(self.menuButton, tearoff=False)

                for s in self.sheetNames:
                    DataMenuElem(self, menu, self.menuButton, s, isExporter=True)

                self.menuButton['menu'] = menu
                self.menuButton.grid(column=0, row=16)

            self.varTemp = []

            def getSelected():
                for v in self.vars:
                    if v.get() == 1:
                        self.varTemp.append(str(v))
                self.vars = self.varTemp
                if self.toNew == False:
                    self.selectedSheet = self.menuButton.cget('text')
                    self.exportToSelected()
                else:
                    self.exportToNew()
        except:
            notification.create('error', 'No imported file detected. Data input by hand?', 5000)

    def exportToNew(self):
        print('exporting to new')
        dfs= {}
        imgs = []
        
        temp = {}
        units = {}
        mcs = {}
        columns = []
        
        if self.onlyPlots == True:
            for i, p in enumerate(app.getPlottingPanel().plots):
                img = p.plot[0].savefig(f'plot{i}.png')
                imgs.append( img )
                # data = []
                columns = []
                for l in p.workLoads:
                    name = l.name
                    columns.append(name)

                df = pd.DataFrame()
                id = p.activeTestId
                idRow = pd.Series(['id', id])
                df = pd.concat([df, idRow.to_frame().T], axis=0, ignore_index=True)
                emptyRow = pd.Series([''])
                df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)
                
                columns.insert(0, '')
                columns.insert(len(columns), 'Unit')
                columns.insert(len(columns), 'Meas/Calc')

                cols = pd.Series(columns)
                df = pd.concat([df, cols.to_frame().T], axis=0, ignore_index=True)

                for i in range(len(p.workLoads)):
                    for v in self.vars:
                        # temp[f'{v}-{i+1}'] = []
                        temp[f'{v}'] = []
                
                # print(f'temp: {temp}')

                for li, l in enumerate(p.workLoads):
                    # name = l.name
                    # columns.append(name)
                    # print(f'NAME {name}')
                    details = l.getDetails().getWorkLoadDetails()

                    for v in self.vars:
                        value = details[v]
                        unit = details[f'{v}_unit']
                        mc = details[f'{v}_MC']
                        # temp[f'{v}-{li+1}'].append(value)
                        temp[f'{v}'].append(value)
                        if v.startswith('pH'):
                            units[v] = ''
                        else:
                            units[v] = unit
                        mcs[v] = mc

                    # Sort values
                    ordered = {}
                    for v in self.vars:
                        for key, value in temp.items():
                            if key.split('-')[0] == v:
                                ordered[key] = value
                            # if key.startswith(v):
                            #     ordered[key] = value

                    # print(ordered)
                
                for key, value in ordered.items():
                    unit = units[f'{key.split("-")[0]}']
                    mc = mcs[f'{key.split("-")[0]}']
                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'
                    # value.insert(0, f'{key} ({unit})-{mc}')
                    # df[key] = value
                    value.insert(0, f'{key}')
                    value.insert(len(value), f'{unit}')
                    value.insert(len(value), f'{mc}')
                    value = pd.Series(value)
                    # print(f'series {value}')
                    df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

                # print(f'df: {df}')

                """ hints = [
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

                    data.append(['','','','']) """

                """ df = pd.DataFrame()

                for l in p.workLoads:
                    temp = []
                    name = l.name
                    details = l.getDetails().getWorkLoadDetails()
                    
                    for v in self.vars:
                        label = None
                        val = None
                        unit = None
                        mc = None

                        label = v
                        val = details[v]
                        unit = details[f'{v}_unit']
                        mc = details[f'{v}_MC']

                        # temp.append([ label, val, unit, mc ])
                        temp.append(val)

                    df[name] = temp

                print(df) """

                # df = pd.DataFrame(data, columns = ['','Value', 'Unit', 'Meas(0)/Calc(1)'])
                dfs[id] = df

            # Create excel
            saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
            with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                for i, (key, value) in enumerate(dfs.items()):
                    value.to_excel(writer, sheet_name=str(key)[0:30], index=False, header=False)
                    worksheet = writer.sheets[str(key)[0:30]]
                    imgDest = f'{os.getcwd()}\plot{i}.png'
                    worksheet.insert_image('N1', imgDest)

            # Delete images
            for i, img in enumerate(imgs):
                os.remove(f'{os.getcwd()}\plot{i}.png')

            writer.save()
            notification.create('info', 'Data successfully exported', 5000)
            self.exportOptions.destroy()
        else:

            pass

    """ def showOptions(self):
        try:
            self.importDataMode = app.getActiveProject().dataMode
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

            hbVar = IntVar(value=1, name="Hb")
            self.vars.append(hbVar)
            ttk.Checkbutton(container, text='Hb', variable=hbVar).grid(column=0, row=1, sticky='nw')

            sao2Var = IntVar(value=1, name="SaO2")
            self.vars.append(sao2Var)
            ttk.Checkbutton(container, text='SaO2', variable=sao2Var).grid(column=0, row=2, sticky='nw')

            qVar = IntVar(value=1, name="Q")
            self.vars.append(qVar)
            ttk.Checkbutton(container, text='Q', variable=qVar).grid(column=0, row=3, sticky='nw')

            cao2Var = IntVar(value=1, name="CaO2")
            self.vars.append(cao2Var)
            ttk.Checkbutton(container, text='CaO2', variable=cao2Var).grid(column=0, row=4, sticky='nw')

            cvo2Var = IntVar(value=1, name="CvO2")
            self.vars.append(cvo2Var)
            ttk.Checkbutton(container, text='CvO2', variable=cvo2Var).grid(column=0, row=5, sticky='nw')

            cavo2Var = IntVar(value=1, name="CavO2")
            self.vars.append(cavo2Var)
            ttk.Checkbutton(container, text='CavO2', variable=cavo2Var).grid(column=0, row=6, sticky='nw')

            qao2Var = IntVar(value=1, name="QaO2")
            self.vars.append(qao2Var)
            ttk.Checkbutton(container, text='QaO2', variable=qao2Var).grid(column=0, row=7, sticky='nw')

            svo2Var = IntVar(value=1, name="SvO2")
            self.vars.append(svo2Var)
            ttk.Checkbutton(container, text='SvO2', variable=svo2Var).grid(column=0, row=8, sticky='nw')

            pvo2Var = IntVar(value=1, name="PvO2")
            self.vars.append(pvo2Var)
            ttk.Checkbutton(container, text='PvO2', variable=pvo2Var).grid(column=0, row=9, sticky='nw')

            do2Var = IntVar(value=1, name="DO2")
            self.vars.append(do2Var)
            ttk.Checkbutton(container, text='DO2', variable=do2Var).grid(column=0, row=10, sticky='nw')

            tcRestVar = IntVar(value=1, name="Tc @ rest")
            self.vars.append(tcRestVar)
            ttk.Checkbutton(container, text='Tc @ rest', variable=tcRestVar).grid(column=0, row=11, sticky='nw')

            tcVar = IntVar(value=1, name="Tc\u209A\u2091\u2090\u2096")
            self.vars.append(tcVar)
            ttk.Checkbutton(container, text='Tc\u209A\u2091\u2090\u2096', variable=tcVar).grid(column=0, row=12, sticky='nw')

            phRestVar = IntVar(value=1, name="pH @ rest")
            self.vars.append(phRestVar)
            ttk.Checkbutton(container, text='pH @ rest', variable=phRestVar).grid(column=0, row=13, sticky='nw')

            phVar = IntVar(value=1, name="pH\u209A\u2091\u2090\u2096")
            self.vars.append(phVar)
            ttk.Checkbutton(container, text='pH\u209A\u2091\u2090\u2096', variable=phVar).grid(column=0, row=14, sticky='nw')

            ttk.Button(container, text='asd', command=lambda: getSelected()).grid(column=1, row=15)

            self.sheetNames = []
            for key, value in excel.items():
                self.sheetNames.append(key)

            # Create menubutton for selection of excel sheet
            self.menuButton = ttk.Menubutton(container, text=self.sheetNames[0])
            menu = Menu(self.menuButton, tearoff=False)

            for s in self.sheetNames:
                DataMenuElem(self, menu, self.menuButton, s, isExporter=True)

            self.menuButton['menu'] = menu
            self.menuButton.grid(column=0, row=16)

            self.varTemp = []
            def getSelected():
                for v in self.vars:
                    if v.get() == 1:
                        self.varTemp.append(str(v))
                self.vars = self.varTemp
                self.selectedSheet = self.menuButton.cget('text')
                self.exportToSelected()
        except:
            notification.create('error', 'No imported file detected. Data input by hand?', 5000)
        """
    
    def exportToSelected(self):
        print('exporting to existing')

        excel = app.getActiveProject().data
        ordered, units, mcs = self.getSortedData()

        # Export values to excel file
        if self.importDataMode == 'long':
            for key, value in ordered.items():
                unit = units[f'{key.split("-")[0]}']
                mc = mcs[f'{key.split("-")[0]}']
                if mc == 1:
                    mc = 'Calculated'
                else:
                    mc = 'Measured'
                value.insert(0, f'{key} ({unit})-{mc}')
                excel[self.selectedSheet][key] = value
        else: # 'wide'
            excelTemp = pd.DataFrame.from_dict(excel[self.selectedSheet])

            for key, value in ordered.items():
                unit = units[f'{key.split("-")[0]}']
                mc = mcs[f'{key.split("-")[0]}']
                if mc == 1:
                    mc = 'Calculated'
                else:
                    mc = 'Measured'
                value.insert(0, f'{key} ({unit})-{mc}')
                value = pd.Series(value, index=range(len(excelTemp.columns)))
                excelTemp = pd.concat([excelTemp, value.to_frame().T], axis=0, ignore_index=True)

            excel[self.selectedSheet] = excelTemp

        saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))

        with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
            for sheet in self.sheetNames:
                df = pd.DataFrame.from_dict(excel[sheet])
                df.to_excel(writer, sheet_name=sheet, index=False, header=False)
            
        writer.save()
        notification.create('info', 'Data successfully exported', 5000)
        self.exportOptions.destroy()

    def getSortedData(self):
        temp= {}
        units = {}
        mcs = {}

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
                            mc = updatedDetails[f'{v}_MC']
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit
                            mcs[v] = mc
                    except:
                        updatedDetails = loads[0].getDetails().getWorkLoadDetails()

                        for v in self.vars:
                            value = 0
                            unit = updatedDetails[f'{v}_unit']
                            mc = updatedDetails[f'{v}_MC']
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit
                            mcs[v] = mc

        # Sort values
        ordered = {}
        for v in self.vars:
            for key, value in temp.items():
                if key.startswith(v):
                    ordered[key] = value

        return ordered, units, mcs