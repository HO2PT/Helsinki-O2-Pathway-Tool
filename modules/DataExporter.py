from cgi import test
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from copy import deepcopy
from objects.test import Test
from objects.app import app
from objects.workLoadDetails import WorkLoadDetails
from modules.notification import notification
from modules.ProjectDataImporter import DataMenuElem
from modules.O2PTSolver import O2PTSolver

class DataExporter(object):
    def __init__(self, toNew, onlyPlots=False):
        # 0 = save to existing file
        # 1 = create new file
        self.toNew = toNew
        self.onlyPlots = onlyPlots

        if self.onlyPlots == True and len(app.getPlottingPanel().plots) == 0:
            notification.create('error', 'No created plots to export', '5000')
        elif self.onlyPlots == False and app.getActiveProject() == None:
            notification.create('error', 'No selected project', '5000')
        else:
            self.showOptions()
        self.temp = {}
        self.units = {}
        self.mcs = {}
        self.images = {}
        self.dfs= {}

        # Number of digits for units
        self.l_min_Dig = 1
        self.ml_min_Dig = 2
        self.ml_l_Dig = 2
        self.ml_dl_Dig = 2
        self.ml_min_mmHg_Dig = 1
        self.g_l_Dig = 1
        self.g_dl_Dig = 1
        self.mmHg_Dig = 2
        self.c_Dig = 1
        self.k_Dig = 1
        self.f_Dig = 1
        self.ml_Dig = 0
        self.bpm_Dig = 0
        self.perc_Dig = 0

    def showOptions(self):
        try:
            if self.toNew == False:
                self.importDataMode = app.getActiveProject().dataMode
                excel = app.getActiveProject().data

                if excel == None:
                    raise AttributeError
            
            self.exportOptions = Toplevel(borderwidth=10)
            self.exportOptions.title("Export options")
            self.exportOptions.focus_force()

            self.container = ttk.Labelframe(self.exportOptions,text='Choose values to be exported', padding=(10, 10))
            self.container.pack()

            self.footer = ttk.Frame(self.exportOptions, padding=(10,0))
            self.footer.pack(side=BOTTOM, fill=X)

            self.vars = []
            loadMode = app.settings.getTestDef()['loadMode']

            temp = WorkLoadDetails(name='dummy')
            for i, key in enumerate(temp.getWorkLoadDetails().keys()):
                if '_unit' not in key and '_MC' not in key and key != 'id' and key != 'Tc @ rest' and key != 'pH @ rest':
                    if loadMode == 0: # Loads
                        if key != 'Velocity' and key != 'Incline':
                            var = IntVar(value=1, name=key)
                            self.vars.append(var)

                            if '2' in key:
                                key = key.replace('2', '\u2082')

                            ttk.Checkbutton(self.container, text=key, variable=var).grid(column=0, row=i, sticky='nw')
                    else: # Velocity&Incline
                        if key != 'Load':
                            var = IntVar(value=1, name=key)
                            self.vars.append(var)

                            if '2' in key:
                                key = key.replace('2', '\u2082')

                            ttk.Checkbutton(self.container, text=key, variable=var).grid(column=0, row=i, sticky='nw')

            ttk.Button(self.container, text='Select All', command=self.selectAll).grid(column=0, row=len(temp.getWorkLoadDetails().keys()))
            ttk.Button(self.container, text='Deselect All', command=self.deselectAll).grid(column=1, row=len(temp.getWorkLoadDetails().keys()))
            
            self.cancelButton = ttk.Button(self.footer, text='Cancel', command=self.cancel)
            self.cancelButton.pack(side=RIGHT)
            self.exportButton = ttk.Button(self.footer, text='Export', command=self.getSelected)
            self.exportButton.pack(side=RIGHT)
            
            # If exporting to imported file
            if self.toNew == False:
                self.sheetNames = []

                for key, value in excel.items():
                    self.sheetNames.append(key)

                # Create the sheet selection dropdown where the data is appended to
                if self.onlyPlots == False:
                    self.container.pack_configure(side=LEFT, padx=10)
                    self.rightContainer = ttk.Frame(self.exportOptions)
                    self.rightContainer.pack(side=RIGHT, fill=X, expand=True)

                    sheetSelFrame = ttk.Labelframe(self.rightContainer, text='To sheet', padding=(10,10))

                    # Create menubutton for selection of excel sheet
                    self.menuButton = ttk.Menubutton(sheetSelFrame, text=self.sheetNames[0])
                    menu = Menu(self.menuButton, tearoff=False)

                    for s in self.sheetNames:
                        DataMenuElem(self, menu, self.menuButton, s, isExporter=True)

                    self.menuButton['menu'] = menu
                    
                    sheetSelFrame.pack(fill=X, expand=True, padx=10)
                    self.menuButton.pack()

                    expOptions = ttk.Labelframe(self.rightContainer, text='Options', padding=(10,10))
                    expOptions.pack(fill=X, expand=True, padx=10)

                    self.statsVar0 = IntVar(value=0)
                    self.statsVar1 = IntVar(value=0)
                    self.statsVar2 = IntVar(value=0)
                    ttk.Checkbutton(expOptions, text='Create mean (SD) graph', variable=self.statsVar0).grid(column=0, row=0, sticky='nw')
                    ttk.Checkbutton(expOptions, text='Create median (IQR) graph', variable=self.statsVar1).grid(column=0, row=1, sticky='nw')
                    ttk.Checkbutton(expOptions, text='Create mean (CI95%) graph', variable=self.statsVar2).grid(column=0, row=2, sticky='nw')

                    expOptions.grid_rowconfigure(3, minsize=15)

                    self.plotVar = IntVar(value=0)
                    ttk.Radiobutton(expOptions, text='Create graph for every test on a separate sheet', variable=self.plotVar, value=0).grid(column=0, row=4, sticky='nw')
                    ttk.Radiobutton(expOptions, text='Export only quantitative results', variable=self.plotVar, value=1).grid(column=0, row=5, sticky='nw')
                else:
                    self.exportOptions.geometry("550x450")
            # If exporting to a new file
            else:
                if self.onlyPlots == False:
                    self.container.pack_configure(side=LEFT, padx=10)
                    expOptions = ttk.Labelframe(self.exportOptions, text='Options')
                    expOptions.pack(side=LEFT, fill=X, expand=True, padx=10)

                    self.statsVar0 = IntVar(value=0)
                    self.statsVar1 = IntVar(value=0)
                    self.statsVar2 = IntVar(value=0)
                    ttk.Checkbutton(expOptions, text='Create mean (SD) plot', variable=self.statsVar0).grid(column=0, row=0, sticky='nw')
                    ttk.Checkbutton(expOptions, text='Create median (IQR) plot', variable=self.statsVar1).grid(column=0, row=1, sticky='nw')
                    ttk.Checkbutton(expOptions, text='Create mean (CI95%) plot', variable=self.statsVar2).grid(column=0, row=2, sticky='nw')
                else:
                    self.exportOptions.geometry("550x450")

            self.exportOptions.update_idletasks()
            optionsX = int(self.exportOptions.winfo_screenwidth()) * 0.5 - int(self.exportOptions.winfo_width()) * 0.5
            optionsY = int(self.exportOptions.winfo_screenheight()) * 0.5 - int(self.exportOptions.winfo_height()) * 0.5
            self.exportOptions.geometry("+%d+%d" % ( optionsX, optionsY ))

            self.varTemp = []

        except:
            notification.create('error', 'No imported file detected. Data input by hand?', 5000)
            # self.exportOptions.destroy()
    
    def getSelected(self):
        # Block the export options pop-up
        self.exportOptions.update_idletasks()
        self.exportButton.configure(text='Exporting', state=DISABLED)
        self.cancelButton.configure(state=DISABLED)

        w = self.exportOptions.winfo_width()
        h = self.exportOptions.winfo_height()
        self.overLay = Toplevel( width=w, height=h, bg='light gray')
        self.overLay.overrideredirect(True)
        X = self.exportOptions.winfo_rootx()
        Y = self.exportOptions.winfo_rooty()
        self.overLay.geometry("+%d+%d" % ( X, Y ))
        self.overLay.lift()
        self.overLay.attributes('-alpha', 0.3)

        def proceed():
            for v in self.vars:
                if v.get() == 1:
                    self.varTemp.append(str(v))
            self.vars = self.varTemp

            if self.toNew == False:
                if self.onlyPlots == False:
                    self.selectedSheet = self.menuButton.cget('text')
                self.exportToSelected()
            else:
                self.exportToNew()

        self.exportButton.after(100, proceed)

    def selectAll(self):
        for v in self.vars:
            v.set(1)

    def deselectAll(self):
        for v in self.vars:
            v.set(0)

    def cancel(self):
        try:
            self.overLay.destroy()
        except:
            pass
        self.exportOptions.destroy()

    def exportToNew(self):
        imgs = []
        columns = []
        
        if self.onlyPlots == True:
            for i, p in enumerate(app.getPlottingPanel().plots):
                
                # Keep the aspect ratio of the plot the same even
                # if the legend's size varies
                legSize = p.plot[1].legend_._legend_box.get_window_extent(p.plot[0].canvas.get_renderer())
                coef = 1 + (legSize.width/100)/5.4
                p.plot[0].set(figwidth=5.4*coef, figheight=4)

                img = p.plot[0].savefig(f'plot{i}.png')
                imgs.append( img )
                columns = []
                for l in p.workLoadDetailsObjects:
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

                for j in range(len(p.workLoadDetailsObjects)):
                    for v in self.vars:
                        self.temp[f'{v}'] = []

                for li, l in enumerate(p.workLoadDetailsObjects):
                    details = l.getWorkLoadDetails()

                    for v in self.vars:
                        value = details[v]
                        unit = details[f'{v}_unit']
                        try:
                            mc = details[f'{v}_MC']
                        except KeyError:
                            mc = None
                        self.temp[f'{v}'].append(value)
                        if v.startswith('pH'):
                            self.units[v] = ''
                        else:
                            self.units[v] = unit
                        self.mcs[v] = mc

                    # Sort values
                    ordered = {}
                    for v in self.vars:
                        for key, value in self.temp.items():
                            ordered[key] = value

                for key, value in ordered.items():
                    unit = self.units[key]
                    mc = self.mcs[key]
                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'

                    # Change 2's to subscript
                    if '2' in key:
                        key = key.replace('2', '\u2082')

                    value = self.formatValue(value, unit)

                    value.insert(0, f'{key}')
                    value.insert(len(value), f'{unit}')
                    value.insert(len(value), f'{mc}')
                    value = pd.Series(value)
                    df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

                # Allow duplicates
                if id in self.dfs.keys():
                    id = f'{id}-{i+1}'

                self.dfs[id] = df

            # Create excel
            try:
                saveFile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                if saveFile:
                    with pd.ExcelWriter(f'{saveFile}.xlsx', engine='xlsxwriter') as writer:
                        for i, (key, value) in enumerate(self.dfs.items()):
                            value.to_excel(writer, sheet_name=str(key)[0:30], index=False, header=False)
                            worksheet = writer.sheets[str(key)[0:30]]
                            imgDest = f'{os.getcwd()}\plot{i}.png'
                            worksheet.insert_image('N1', imgDest)

                    notification.create('info', 'Data successfully exported', 5000)
                else:
                    self.cancel()
                    notification.create('error', 'Data not exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for i, img in enumerate(imgs):
                os.remove(f'{os.getcwd()}\plot{i}.png')
            self.exportOptions.destroy()
        else:
            project = app.getActiveProject()
            subjects = project.getSubjects()

            # Create project plots
            if self.statsVar0.get() == 1:
                self.images['Mean(SD)'] = []
                df = self.createProjectPlots('Mean(SD)')
                self.dfs['Mean(SD)'] = df

            if self.statsVar1.get() == 1:
                self.images['Median(IQR)'] = []
                df = self.createProjectPlots('Median(IQR)', iqr=True)
                self.dfs['Median(IQR)'] = df

            if self.statsVar2.get() == 1:
                self.images['Mean(CI95%)'] = []
                df = self.createProjectPlots('Mean(CI95%)', ci95=True)
                self.dfs['Mean(CI95%)'] = df

            # Create plots for subjects
            for s in subjects:
                tests = s.getTests()
                dfSubject = pd.DataFrame()
                self.images[s.id] = []

                for t in tests:
                    df = self.createDfForTest(t, s.id)
                    dfSubject = pd.concat([df, dfSubject], axis=0, ignore_index=True)

                self.dfs[s.id] = dfSubject

            # Create mass info sheet
            self.dfs['Data'] = self.createDataDumpSheet()

            # Create excel
            try:
                saveFile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                if saveFile:
                    with pd.ExcelWriter(f'{saveFile}.xlsx', engine='xlsxwriter') as writer:
                        for key, value in self.dfs.items():
                            value.to_excel(writer, sheet_name=str(key)[0:30], index=False, header=False)
                            worksheet = writer.sheets[str(key)[0:30]]

                            for subjectId, testId in list(self.images.items()):
                                if key == subjectId:
                                    for ti, t in enumerate(reversed(testId)):
                                        imgDest = f'{os.getcwd()}\plot-{key}-{t}.png'
                                        
                                        if ti == 0:   
                                            worksheet.insert_image('N1', imgDest)
                                        else:
                                            worksheet.insert_image(f'N{int(ti)+(int(ti)*20)+1}', imgDest)

                    self.overLay.destroy()
                    notification.create('info', 'Data successfully exported', 5000)
                else:
                    self.cancel()
                    notification.create('error', 'Data not exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for subjectId, testId in self.images.items():
                for ti, t in enumerate(testId):
                    os.remove(f'{os.getcwd()}\plot-{subjectId}-{testId[ti]}.png')

            self.exportOptions.destroy()

    def createDataDumpSheet(self):
        project = app.getActiveProject()
        subjects = project.getSubjects()
        nLoads = 0
        df = pd.DataFrame()
        rows = []

        # Get number of loads 
        for s in subjects:
            for t in s.tests:
                n = len(t.workLoads)
                if n > nLoads:
                    nLoads = n

        # Construct header row
        headerRow = ['ID']
        for v in self.vars:
            unit = subjects[0].tests[0].workLoads[0].details.getWorkLoadDetails()[f'{v}_unit']
            for i in range(nLoads):
                headerRow.append(f'{v}-{i}({unit})')

        headerRow = pd.Series(headerRow)
        df = pd.concat([df, headerRow.to_frame().T], axis=0, ignore_index=True)
        
        # Append subject data row by row
        for s in subjects:
            for t in s.tests:
                row = pd.Series([t.id])
                for var in self.vars:
                    for w in t.workLoads:
                        row = pd.concat([row, pd.Series([w.details.getWorkLoadDetails()[var]], dtype='float64')], axis=0, ignore_index=True)
                df = pd.concat([df, row.to_frame().T], axis=0, ignore_index=True)
        
        return df

    def exportToSelected(self):
        excel = deepcopy(app.getActiveProject().data)
        ordered, units, mcs = self.getSortedData()

        if self.onlyPlots == True: # Export only created plots
            self.createDfsOfPlots()
            for key,value in self.dfs.items():
                excel[str(key)[0:30]] = value
                self.sheetNames.append(str(key)[0:30])

            # Create excel
            try:
                saveFile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                if saveFile:
                    with pd.ExcelWriter(f'{saveFile}.xlsx', engine='xlsxwriter') as writer:
                        for sheet in self.sheetNames:
                            df = pd.DataFrame.from_dict(excel[sheet])
                            df.to_excel(writer, sheet_name=sheet, index=False, header=False)

                            for i, (key, value) in enumerate(self.dfs.items()):
                                if sheet == str(key)[0:30]:
                                    worksheet = writer.sheets[sheet]
                                    imgDest = f'{os.getcwd()}\plot{key}.png'
                                    worksheet.insert_image('N1', imgDest)

                    notification.create('info', 'Data successfully exported', 5000)
                else:
                    self.cancel()
                    notification.create('error', 'Data not exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for i, (key, value) in enumerate(self.dfs.items()):
                os.remove(f'{os.getcwd()}\plot{key}.png')
            self.exportOptions.destroy()

        else: # Export all values and plots to excel file
            if self.importDataMode == 'long':
                for key, value in ordered.items():
                    if 'C(a-v)O2' in key:
                        key0 = 'C(a-v)O\u2082'
                        key1 = key.split('-')[2]
                        key = f'{key0}-{key1}'
                        unit = units['C(a-v)O2']
                        mc = mcs['C(a-v)O2']
                    else:
                        unit = units[f'{key.split("-")[0]}']
                        mc = mcs[f'{key.split("-")[0]}']
                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'

                    # Change 2's to subscript
                    if '2' in key.split('-')[0]:
                        key0 = key.split('-')[0].replace('2', '\u2082')
                        key1 = key.split('-')[1]
                        key = f'{key0}-{key1}'

                    value = self.formatValue(value, unit)
                    
                    value.insert(0, f'{key} ({unit})-{mc}')
                    excel[self.selectedSheet][key] = value
            else: # 'wide'
                excelTemp = pd.DataFrame.from_dict(excel[self.selectedSheet])

                for key, value in ordered.items():
                    if 'C(a-v)O2' in key:
                        key0 = 'C(a-v)O\u2082'
                        key1 = key.split('-')[2]
                        key = f'{key0}-{key1}'
                        unit = units['C(a-v)O2']
                        mc = mcs['C(a-v)O2']
                    else:
                        unit = units[f'{key.split("-")[0]}']
                        mc = mcs[f'{key.split("-")[0]}']

                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'

                    # Change 2's to subscript
                    if '2' in key.split('-')[0]:
                        key0 = key.split('-')[0].replace('2', '\u2082')
                        key1 = key.split('-')[1]
                        key = f'{key0}-{key1}'

                    value = self.formatValue(value, unit)

                    value.insert(0, f'{key} ({unit})-{mc}')
                    value = pd.Series(value, index=range(len(excelTemp.columns)))
                    excelTemp = pd.concat([excelTemp, value.to_frame().T], axis=0, ignore_index=True)

                excel[self.selectedSheet] = excelTemp

            # Create project plots
            if self.statsVar0.get() == 1:
                df = self.createProjectPlots('Mean(SD)')
                excel['Mean(SD)'] = df
                self.sheetNames.append('Mean(SD)')

            if self.statsVar1.get() == 1:
                df = self.createProjectPlots('Median(IQR)', iqr=True)
                excel['Median(IQR)'] = df
                self.sheetNames.append('Median(IQR)')

            if self.statsVar2.get() == 1:
                df = self.createProjectPlots('Mean(CI95%)', ci95=True)
                excel['Mean(CI95%)'] = df
                self.sheetNames.append('Mean(CI95%)')

            # Create plots for subjects
            if self.plotVar.get() == 0:
                subjects = app.getActiveProject().getSubjects()
                plotsDf = pd.DataFrame()
                for s in subjects:
                    tests = s.getTests()
                    self.images[s.id] = []

                    for t in tests:
                        loads = t.workLoads

                        # Filter possible empty loads
                        filteredLoads = []
                        for i, l in enumerate(loads):
                            detailsDict = l.getDetails().getWorkLoadDetails()
                            
                            if i == 0 or detailsDict['Load'] != 0:
                                filteredLoads.append(l.details)

                        self.createPlot(filteredLoads, t.id)
                        self.images[s.id].append(str(t.id))

                excel['Plots'] = plotsDf
                self.sheetNames.append('Plots')

            try:
                saveFile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                if saveFile:
                    # Create excel
                    with pd.ExcelWriter(f'{saveFile}.xlsx', engine='xlsxwriter') as writer:
                        for sheet in self.sheetNames:
                            df = pd.DataFrame.from_dict(excel[sheet])
                            df.to_excel(writer, sheet_name=sheet, index=False, header=False)

                            if sheet == 'Plots':
                                worksheet = writer.sheets[sheet]
                                for i, (key, value) in enumerate(self.images.items()):
                                    imgDest = f'{os.getcwd()}\plot{value[0]}.png'
                                    if i != 0:
                                        worksheet.write(f'A{i*20+3}', f'Test ID: {value[0]}')
                                        worksheet.insert_image(f'A{i*20+4}', imgDest)
                                    else:
                                        worksheet.write('A1', f'Test ID: {value[0]}')
                                        worksheet.insert_image('A2', imgDest)
                            if sheet == 'Median(IQR)':
                                worksheet = writer.sheets[sheet]
                                imgDest = f'{os.getcwd()}\plot-Median(IQR)-Project Median(IQR).png'
                                worksheet.insert_image('H1', imgDest)
                            elif sheet == 'Mean(SD)':
                                worksheet = writer.sheets[sheet]
                                imgDest = f'{os.getcwd()}\plot-Mean(SD)-Project Mean(SD).png'
                                worksheet.insert_image('H1', imgDest)
                            elif sheet == 'Mean(CI95%)':
                                worksheet = writer.sheets[sheet]
                                imgDest = f'{os.getcwd()}\plot-Mean(CI95%)-Project mean(95% CI).png'
                                worksheet.insert_image('H1', imgDest)
                        
                    notification.create('info', 'Data successfully exported', 5000)
                else:
                    self.cancel()
                    notification.create('error', 'Data not exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            if self.plotVar.get() == 0:
                for s in subjects:
                    tests = s.getTests()
                    for t in tests:
                        os.remove(f'{os.getcwd()}\plot{t.id}.png')

            if self.statsVar0.get() == 1:
                os.remove(f'{os.getcwd()}\plot-Mean(SD)-Project Mean(SD).png')
            if self.statsVar1.get() == 1:
                os.remove(f'{os.getcwd()}\plot-Median(IQR)-Project Median(IQR).png')
            if self.statsVar2.get() == 1:
                os.remove(f'{os.getcwd()}\plot-Mean(CI95%)-Project mean(95% CI).png')
            
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
                workLoadObjects = []
                for l in t.getWorkLoads():
                    workLoadObjects.append(l.getDetails())

                for i in range(nLoads):
                    try:
                        details = workLoadObjects[i].getWorkLoadDetails()
                        O2PTSolver(workLoadObjects[i], details).calc()
                        updatedDetails = workLoadObjects[i].getWorkLoadDetails()
                        for v in self.vars:
                            value = updatedDetails[v]
                            unit = updatedDetails[f'{v}_unit']
                            try:
                                mc = updatedDetails[f'{v}_MC']
                            except:
                                mc = None
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit
                            mcs[v] = mc

                    except Exception as err:
                        updatedDetails = workLoadObjects[0].getWorkLoadDetails()

                        for v in self.vars:
                            value = 0
                            unit = updatedDetails[f'{v}_unit']
                            try:
                                mc = updatedDetails[f'{v}_MC']
                            except KeyError:
                                mc = None
                            temp[f'{v}-{i+1}'].append(value)
                            units[v] = unit
                            mcs[v] = mc

        # Sort values
        ordered = {}
        for v in self.vars:
            for key, value in temp.items():
                if v == 'C(a-v)O2':
                    str = f'{key.split("-")[0]}-{key.split("-")[1]}'
                    if str == v:
                        ordered[key] = value
                else:
                    if key.split('-')[0] == v:
                        ordered[key] = value

        return ordered, units, mcs

    def createPlot(self, workLoads, id, sid=None): #workloads = workloaddetails object
        PvO2 = np.arange(0,100,1)
        plot = plt.subplots(constrained_layout=True)
        fig, ax = plot

        ax.set_title('O\u2082 Pathway')
        ax.set_xlabel('PvO\u2082 (mmHg)')
        ax.set_ylim(top=5000, bottom=0)
        ax.set_xlim(left=0, right=100)

        handles = []
        ylim = []

        def numfmt(x, pos=None):
            vo2unit = workLoads[0].VO2_unit
            if vo2unit == 'l/min':
                s = '{0:.1f}'.format(x / 1000.0)
            elif vo2unit == 'ml/min':
                s = '{0:.0f}'.format(x)
            return s

        # Change y-axis unit based on used vo2 unit
        vo2unit = workLoads[0].VO2_unit
        yfmt = ticker.FuncFormatter(numfmt)
        plt.gca().yaxis.set_major_formatter(yfmt)
        if vo2unit == 'l/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (l/min)')
        elif vo2unit == 'ml/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (ml/min)')

        for i, w in enumerate(workLoads):
            coords = w.getCoords()
            y = coords['y']
            y2 = coords['y2']
            xi = coords['xi']
            yi = coords['yi']

            ylim.append(y2[0])

            line, = ax.plot(PvO2, y, lw=2, color=f'C{i}', label=w.name)
            curve, = ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=w.name)
            dot, = ax.plot(xi, yi, 'o', color='red', label=w.name)

            handles.insert(i, line)
        
        if max(ylim) > 50: # ml/min
            ylim = 1000 * math.ceil( max(ylim) / 1000 )
        else: # l/min
            ylim = 1 * math.ceil( max(ylim) / 1 ) + 1

        ax.set_ylim(top=ylim, bottom=0)

        leg = ax.legend(handles=handles , loc='upper left', bbox_to_anchor=(1.01, 1),
            fancybox=True, shadow=True, ncol=1)

        legSize = leg._legend_box.get_window_extent(fig.canvas.get_renderer())
        coef = 1 + (legSize.width/100)/5.4
        fig.set(figwidth=5.4*coef, figheight=4)
        
        if sid == None:
            fig.savefig(f'plot{id}.png')
        else:
            fig.savefig(f'plot-{sid}-{id}.png')
        fig.clear()
        plt.close(fig)

    def createDfForTest(self, test, sid, projectPlot = False):
        workLoads = test.getWorkLoads() # Load objects
        filteredLoads = []
        # Filter possible empty loads
        for i, l in enumerate(workLoads):
            detailsDict = l.getDetails().getWorkLoadDetails()
            if projectPlot == True:
                filteredLoads.append(l)
            else:
                if i == 0 or detailsDict['Load'] != 0:
                    filteredLoads.append(l)

        columns = []
        for l in filteredLoads:
            name = l.name
            columns.append(name)

        df = pd.DataFrame()
        id = test.id
        idRow = pd.Series(['id', id])
        df = pd.concat([df, idRow.to_frame().T], axis=0, ignore_index=True)
        emptyRow = pd.Series([''])
        df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)
                
        columns.insert(0, '')
        columns.insert(len(columns), 'Unit')
        columns.insert(len(columns), 'Meas/Calc')

        cols = pd.Series(columns)
        df = pd.concat([df, cols.to_frame().T], axis=0, ignore_index=True)

        # initialize row indexes
        for v in self.vars:
            self.temp[f'{v}'] = []

        for li, l in enumerate(filteredLoads):
            details = l.getDetails().getWorkLoadDetails()
            if projectPlot == False:
                O2PTSolver(l.getDetails(), details).calc()
            updatedDetails = l.getDetails().getWorkLoadDetails()

            for v in self.vars:
                value = updatedDetails[v]
                unit = updatedDetails[f'{v}_unit']
                try:
                    mc = updatedDetails[f'{v}_MC']
                except KeyError:
                    mc = None

                self.temp[f'{v}'].append(value)
                if v.startswith('pH'):
                    self.units[v] = ''
                else:
                    self.units[v] = unit
                self.mcs[v] = mc

            # Sort values
            ordered = {}
            for v in self.vars:
                for key, value in self.temp.items():
                    ordered[key] = value

        # Create plot
        workLoadObjects = []
        for l in filteredLoads:
            workLoadObjects.append(l.getDetails())

        if projectPlot == False:
            self.createPlot(workLoadObjects, id, sid=sid)

        try:
            self.images[sid].append(f'{id}')
        except:
            pass

        for key, value in ordered.items():
            unit = self.units[key]
            mc = self.mcs[key]
            if mc == 1:
                mc = 'Calculated'
            else:
                mc = 'Measured'

            # Change 2's to subscript
            if '2' in key:
                key = key.replace('2', '\u2082')

            value = self.formatValue(value, unit)

            value.insert(0, f'{key}')
            value.insert(len(value), f'{unit}')
            value.insert(len(value), f'{mc}')
            value = pd.Series(value)
            df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

        df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)
        df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)

        return df

    def createProjectPlots(self, label=None, iqr=False, ci95=False):
        dummyTest = Test()
        subjects = app.getActiveProject().getSubjects()
        
        app.plotMean(test=dummyTest, subjects=subjects, plotProject=True, iqr=iqr, ci95=ci95, export=True)
        workLoadDetailObjects = []
        for w in dummyTest.getWorkLoads():
            workLoadDetailObjects.append(w.getDetails())
        self.createPlot(workLoadDetailObjects, dummyTest.id, sid=label)
        
        df = self.createDfForTest(dummyTest, label, projectPlot=True)
        return df

    def createDfsOfPlots(self):
        for i, p in enumerate(app.getPlottingPanel().plots):
            self.images[i] = 'img'
            columns = []
            for l in p.workLoadDetailsObjects:
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

            for i in range(len(p.workLoadDetailsObjects)):
                for v in self.vars:
                    self.temp[f'{v}'] = []

            for li, l in enumerate(p.workLoadDetailsObjects):
                details = l.getWorkLoadDetails()

                for v in self.vars:
                    value = details[v]
                    unit = details[f'{v}_unit']
                    try:
                        mc = details[f'{v}_MC']
                    except KeyError:
                        mc = None
                    self.temp[f'{v}'].append(value)
                    if v.startswith('pH'):
                        self.units[v] = ''
                    else:
                        self.units[v] = unit
                    self.mcs[v] = mc

                # Sort values
                ordered = {}
                for v in self.vars:
                    for key, value in self.temp.items():
                        ordered[key] = value
                
            for key, value in ordered.items():
                unit = self.units[key]
                mc = self.mcs[key]
                
                if mc == 1:
                    mc = 'Calculated'
                else:
                    mc = 'Measured'

                # Change 2's to subscript
                if '2' in key:
                    key = key.replace('2', '\u2082')

                value = self.formatValue(value, unit)

                value.insert(0, f'{key}')
                value.insert(len(value), f'{unit}')
                value.insert(len(value), f'{mc}')
                value = pd.Series(value)
                df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

            # Create plot
            self.createPlot(p.workLoadDetailsObjects, id)
            
            self.dfs[id] = df

    def formatValue(self, value, unit):
        res = []
        if unit == 'l/min':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.l_min_Dig)
                res.append(v)
            return res
        elif unit == 'ml/min':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.ml_min_Dig)
                res.append(v)
            return res
        elif unit == 'ml/l':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.ml_l_Dig)
                res.append(v)
            return res
        elif unit == 'ml/dl':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.ml_dl_Dig)
                res.append(v)
            return res
        elif unit == 'ml/min/mmHg':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.ml_min_mmHg_Dig)
                res.append(v)
            return res
        elif unit == 'g/l':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.g_l_Dig)
                res.append(v)
            return res
        elif unit == 'g/dl':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.g_dl_Dig)
                res.append(v)
            return res
        elif unit == 'mmHg':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.mmHg_Dig)
                res.append(v)
            return res
        elif unit == '\N{DEGREE SIGN}C':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.c_Dig)
                res.append(v)
            return res
        elif unit == 'K':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.k_Dig)
                res.append(v)
            return res
        elif unit == 'F':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.f_Dig)
                res.append(v)
            return res
        elif unit == '%':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.perc_Dig)
                res.append(v)
            return res
        elif unit == 'ml':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.ml_Dig)
                res.append(v)
            return res
        elif unit == 'bpm':
            for v in value:
                v = '{0:.{1}f}'.format(float(v), self.bpm_Dig)
                res.append(v)
            return res
        else:
            for v in value:
                res.append(str(v))
            return res