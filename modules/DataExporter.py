import os
from tkinter import *
from tkinter import ttk
from objects.test import Test
from objects.app import app
from modules.notification import notification
from modules.DataImporter import DataMenuElem
from tkinter.filedialog import asksaveasfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class DataExporter(object):
    def __init__(self, toNew, onlyPlots=False):
        # 0 = save to existing file
        # 1 = create new file
        self.toNew = toNew
        self.onlyPlots = onlyPlots

        if self.onlyPlots == True and len(app.getPlottingPanel().plots) == 0:
            notification.create('error', 'No created plots to export', '5000')
        elif app.getActiveProject() == None:
            notification.create('error', 'No selected project', '5000')
        else:
            self.showOptions()
        self.temp = {}
        self.units = {}
        self.mcs = {}
        self.images = {}
        self.dfs= {}

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

            ttk.Button(container, text='Export', command=lambda: getSelected()).grid(column=1, row=15)

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
        
        imgs = []
        columns = []
        
        if self.onlyPlots == True:
            for i, p in enumerate(app.getPlottingPanel().plots):
                img = p.plot[0].savefig(f'plot{i}.png')
                imgs.append( img )
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
                        self.temp[f'{v}'] = []

                for li, l in enumerate(p.workLoads):
                    details = l.getDetails().getWorkLoadDetails()

                    for v in self.vars:
                        value = details[v]
                        unit = details[f'{v}_unit']
                        mc = details[f'{v}_MC']
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
                            if key.split('-')[0] == v:
                                ordered[key] = value
                
                for key, value in ordered.items():
                    unit = self.units[f'{key.split("-")[0]}']
                    mc = self.mcs[f'{key.split("-")[0]}']
                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'
                    value.insert(0, f'{key}')
                    value.insert(len(value), f'{unit}')
                    value.insert(len(value), f'{mc}')
                    value = pd.Series(value)
                    df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

                self.dfs[id] = df

            # Create excel
            saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
            with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                for i, (key, value) in enumerate(self.dfs.items()):
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
            project = app.getActiveProject()
            subjects = project.getSubjects()

            # Create project plots
            self.images['Mean-SD'] = []
            df = self.createProjectPlots('Mean-SD')
            self.dfs['Mean-SD'] = df

            self.images['Mean-IQR'] = []
            df = self.createProjectPlots('Mean-IQR', iqr=True)
            self.dfs['Mean-IQR'] = df

            # Create plots for subjects
            for s in subjects:
                tests = s.getTests()
                dfSubject = pd.DataFrame()
                self.images[s.id] = []

                for t in tests:
                    df = self.createDfForTest(t, s.id)
                    dfSubject = pd.concat([df, dfSubject], axis=0, ignore_index=True)

                self.dfs[s.id] = dfSubject

            # Create excel
            saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
            with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                for i, (key, value) in enumerate(self.dfs.items()):
                    value.to_excel(writer, sheet_name=str(key)[0:30], index=False, header=False)
                    worksheet = writer.sheets[str(key)[0:30]]
                    for i in range(len(self.images[key])):
                        if i != 0:
                            imgDest = f'{os.getcwd()}\plot{value.iloc[i*20][1]}.png'
                            worksheet.insert_image(f'N{i*20}', imgDest)
                        else:
                            imgDest = f'{os.getcwd()}\plot{value.iloc[0][1]}.png'
                            worksheet.insert_image('N1', imgDest)

            # Delete images
            for s in subjects:
                tests = s.getTests()
                for t in tests:
                    os.remove(f'{os.getcwd()}\plot{t.id}.png')
            os.remove(f'{os.getcwd()}\plotProject mean-IQR.png')
            os.remove(f'{os.getcwd()}\plotProject mean-SD.png')

            writer.save()
            notification.create('info', 'Data successfully exported', 5000)
            self.exportOptions.destroy()

    def exportToSelected(self):
        print('exporting to existing')

        excel = app.getActiveProject().data
        ordered, units, mcs = self.getSortedData()

        if self.onlyPlots == True: # Export only created plots
            self.createDfsOfPlots()
            for key,value in self.dfs.items():
                # print(key, value)
                excel[str(key)[0:30]] = value
                self.sheetNames.append(str(key)[0:30])

            # Create excel
            saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
            with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                for sheet in self.sheetNames:
                    print(f'sheet: {sheet}')
                    df = pd.DataFrame.from_dict(excel[sheet])
                    df.to_excel(writer, sheet_name=sheet, index=False, header=False)

                    for i, (key, value) in enumerate(self.dfs.items()):
                        if sheet == str(key)[0:30]:
                            print('osuma')
                            print(str(key)[0:30])
                            worksheet = writer.sheets[sheet]
                            imgDest = f'{os.getcwd()}\plot{key}.png'
                            worksheet.insert_image('N1', imgDest)

            # Delete images
            for i, (key, value) in enumerate(self.dfs.items()):
                os.remove(f'{os.getcwd()}\plot{key}.png')

            writer.save()
            notification.create('info', 'Data successfully exported', 5000)
            self.exportOptions.destroy()

        else: # Export all values and plots to excel file
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

            # Create project plots
            df = self.createProjectPlots('Mean-SD')
            excel['Mean-SD'] = df
            self.sheetNames.append('Mean-SD')

            df = self.createProjectPlots('Mean-SD', iqr=True)
            excel['Mean-IQR'] = df
            self.sheetNames.append('Mean-IQR')

            # Create plots for subjects
            subjects = app.getActiveProject().getSubjects()
            plotsDf = pd.DataFrame()
            for s in subjects:
                tests = s.getTests()
                self.images[s.id] = []

                for t in tests:
                    # plotDf = pd.DataFrame()
                    loads = t.getWorkLoads()
                    self.createPlot(loads, t.id)
                    self.images[s.id].append(str(t.id))

            excel['Plots'] = plotsDf
            self.sheetNames.append('Plots')

            saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))

            # Create excel
            with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
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
                    if sheet == 'Mean-IQR':
                        worksheet = writer.sheets[sheet]
                        imgDest = f'{os.getcwd()}\plotProject mean-IQR.png'
                        worksheet.insert_image('H1', imgDest)
                    elif sheet == 'Mean-SD':
                        worksheet = writer.sheets[sheet]
                        imgDest = f'{os.getcwd()}\plotProject mean-SD.png'
                        worksheet.insert_image('H1', imgDest)

            # Delete images
            for s in subjects:
                tests = s.getTests()
                for t in tests:
                    os.remove(f'{os.getcwd()}\plot{t.id}.png')
            os.remove(f'{os.getcwd()}\plotProject mean-IQR.png')
            os.remove(f'{os.getcwd()}\plotProject mean-SD.png')
                
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
                if key.split('-')[0] == v:
                    ordered[key] = value

        return ordered, units, mcs

    def createPlot(self, workLoads, id):
        PvO2 = np.arange(0,100,1)
        plot = plt.subplots()
        fig, ax = plot

        fig.set_figheight(4)
        fig.set_figwidth(5.4)

        ax.set_title('O2 Pathway')
        ax.set_xlabel('PvO\u2082 (mmHg)')
        ax.set_ylim(top=5000, bottom=0)
        ax.set_xlim(left=0, right=100)
        handles = []

        def numfmt(x, pos=None):
            vo2unit = workLoads[0].getDetails().VO2_unit
            if vo2unit == 'l/min':
                s = '{0:.1f}'.format(x / 1000.0)
            elif vo2unit == 'ml/min':
                s = '{0:.0f}'.format(x)
            return s

        # Change y-axis unit based on used vo2 unit
        vo2unit = workLoads[0].getDetails().VO2_unit
        yfmt = ticker.FuncFormatter(numfmt)
        plt.gca().yaxis.set_major_formatter(yfmt)
        if vo2unit == 'l/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (l/min)')
        elif vo2unit == 'ml/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (ml/min)')

        for i, w in enumerate(workLoads):
            coords = w.getDetails().getCoords()
            y = coords['y']
            y2 = coords['y2']
            xi = coords['xi']
            yi = coords['yi']

            line, = ax.plot(PvO2, y, lw=2, color=f'C{i}', label=w.name)
            curve, = ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=w.name)
            dot, = ax.plot(xi, yi, 'o', color='red', label=w.name)

            handles.insert(i, line)

        leg = ax.legend(handles=handles , loc='upper center', bbox_to_anchor=(0.5, 1.1),
            fancybox=True, shadow=True, ncol=5)
        
        fig.savefig(f'plot{id}.png')
        fig.clear()
        plt.close(fig)

    def createDfForTest(self, test, sid):
        workLoads = test.getWorkLoads() # Load objects

        columns = []
        for l in workLoads:
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

        for li, l in enumerate(workLoads):
            details = l.getDetails().getWorkLoadDetails()
            app.getPlottingPanel().calc(workLoads[li], details)
            updatedDetails = workLoads[li].getDetails().getWorkLoadDetails()

            for v in self.vars:
                value = updatedDetails[v]
                unit = updatedDetails[f'{v}_unit']
                mc = updatedDetails[f'{v}_MC']

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
                    if key.split('-')[0] == v:
                        ordered[key] = value

        # Create plot
        self.createPlot(workLoads, id)
        try:
            self.images[sid].append('img')
        except:
            pass
                        
        for key, value in ordered.items():
            unit = self.units[f'{key.split("-")[0]}']
            mc = self.mcs[f'{key.split("-")[0]}']
            if mc == 1:
                mc = 'Calculated'
            else:
                mc = 'Measured'
            value.insert(0, f'{key}')
            value.insert(len(value), f'{unit}')
            value.insert(len(value), f'{mc}')
            value = pd.Series(value)
            df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

        df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)
        df = pd.concat([df, emptyRow.to_frame().T], axis=0, ignore_index=True)

        return df

    def createProjectPlots(self, label=None, iqr=False):
        dummyTest = Test()
        subjects = app.getActiveProject().getSubjects()
        
        app.plotMean(test=dummyTest, subjects=subjects, plotProject=True, iqr=iqr ,export=True)
        self.createPlot(dummyTest.getWorkLoads(), dummyTest.id)
        
        df = self.createDfForTest(dummyTest, label)
        return df

    def createDfsOfPlots(self):
        for i, p in enumerate(app.getPlottingPanel().plots):
            self.images[i] = 'img'
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
                    self.temp[f'{v}'] = []

            for li, l in enumerate(p.workLoads):
                details = l.getDetails().getWorkLoadDetails()

                for v in self.vars:
                    value = details[v]
                    unit = details[f'{v}_unit']
                    mc = details[f'{v}_MC']
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
                        if key.split('-')[0] == v:
                            ordered[key] = value
                
            for key, value in ordered.items():
                unit = self.units[f'{key.split("-")[0]}']
                mc = self.mcs[f'{key.split("-")[0]}']
                if mc == 1:
                    mc = 'Calculated'
                else:
                    mc = 'Measured'
                value.insert(0, f'{key}')
                value.insert(len(value), f'{unit}')
                value.insert(len(value), f'{mc}')
                value = pd.Series(value)
                df = pd.concat([df, value.to_frame().T], axis=0, ignore_index=True)

            # Create plot
            self.createPlot(p.workLoads, id)
            
            self.dfs[id] = df