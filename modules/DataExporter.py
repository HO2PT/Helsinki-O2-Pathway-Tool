import os
import math
from tkinter import *
from tkinter import ttk
from objects.test import Test
from objects.app import app
from objects.workLoadDetails import WorkLoadDetails
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
        elif self.onlyPlots == False and app.getActiveProject() == None:
            notification.create('error', 'No selected project', '5000')
        else:
            self.showOptions()
        self.temp = {}
        self.units = {}
        self.mcs = {}
        self.images = {}
        self.dfs= {}

    def showOptions(self):
        # try:
            if self.toNew == False:
                self.importDataMode = app.getActiveProject().dataMode
                excel = app.getActiveProject().data
            
            self.exportOptions = Toplevel(borderwidth=10)
            self.exportOptions.title("Export options")
            self.exportOptions.geometry("500x450")

            self.exportOptions.update_idletasks()
            optionsX = int(self.exportOptions.winfo_screenwidth()) * 0.5 - int(self.exportOptions.winfo_width()) * 0.5
            optionsY = int(self.exportOptions.winfo_screenheight()) * 0.5 - int(self.exportOptions.winfo_height()) * 0.5
            self.exportOptions.geometry("+%d+%d" % ( optionsX, optionsY ))

            self.container = ttk.Labelframe(self.exportOptions,text='Choose values to be exported', padding=(10, 10))
            self.container.pack()

            self.footer = ttk.Frame(self.exportOptions, padding=(10,0))
            self.footer.pack(side=BOTTOM, fill=X)

            self.vars = []
            loadMode = app.settings.getTestDef()['loadMode']

            temp = WorkLoadDetails(name='dummy')
            for i, key in enumerate(temp.getWorkLoadDetails().keys()):
                if '_unit' not in key and '_MC' not in key and key != 'id' and key != 'Tc\u209A\u2091\u2090\u2096' and key != 'pH\u209A\u2091\u2090\u2096' and key != 'Tc @ rest' and key != 'pH @ rest':
                    if loadMode == 0: # Loads
                        if key != 'Velocity' and key != 'Incline':
                            var = IntVar(value=1, name=key)
                            self.vars.append(var)
                            ttk.Checkbutton(self.container, text=key, variable=var).grid(column=0, row=i, sticky='nw')
                    else: # Velocity&Incline
                        if key != 'Load':
                            var = IntVar(value=1, name=key)
                            self.vars.append(var)
                            ttk.Checkbutton(self.container, text=key, variable=var).grid(column=0, row=i, sticky='nw')

            ttk.Button(self.container, text='Select All', command=self.selectAll).grid(column=0, row=len(temp.getWorkLoadDetails().keys()))
            ttk.Button(self.container, text='Deselect All', command=self.deselectAll).grid(column=1, row=len(temp.getWorkLoadDetails().keys()))
            
            ttk.Button(self.footer, text='Cancel', command=self.cancel).pack(side=RIGHT)
            ttk.Button(self.footer, text='Export', command=lambda: getSelected()).pack(side=RIGHT)
            
            # Create the sheet selection dropdown
            if self.toNew == False and self.onlyPlots == False:
                self.sheetNames = []
                sheetSelFrame = ttk.Labelframe(self.exportOptions, text='To sheet', padding=(10,10))

                for key, value in excel.items():
                    self.sheetNames.append(key)

                # Create menubutton for selection of excel sheet
                self.menuButton = ttk.Menubutton(sheetSelFrame, text=self.sheetNames[0])
                menu = Menu(self.menuButton, tearoff=False)

                for s in self.sheetNames:
                    DataMenuElem(self, menu, self.menuButton, s, isExporter=True)

                self.menuButton['menu'] = menu
                self.container.pack_configure(side=LEFT, padx=10)
                sheetSelFrame.pack(side=LEFT, fill=X, expand=True, padx=10)
                self.menuButton.pack()

            self.varTemp = []

            def getSelected():
                for v in self.vars:
                    if v.get() == 1:
                        self.varTemp.append(str(v))
                self.vars = self.varTemp
                print(f'params to export {self.vars}')
                if self.toNew == False:
                    self.selectedSheet = self.menuButton.cget('text')
                    self.exportToSelected()
                else:
                    self.exportToNew()
        # except:
        #     notification.create('error', 'No imported file detected. Data input by hand?', 5000)

    def selectAll(self):
        for v in self.vars:
            v.set(1)

    def deselectAll(self):
        for v in self.vars:
            v.set(0)

    def cancel(self):
        self.exportOptions.destroy()

    def exportToNew(self):
        imgs = []
        columns = []
        
        if self.onlyPlots == True:
            print('EXPORT TO NEW - ONLY PLOTS')
            for i, p in enumerate(app.getPlottingPanel().plots):
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
            try:
                saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                    for i, (key, value) in enumerate(self.dfs.items()):
                        value.to_excel(writer, sheet_name=str(key)[0:30], index=False, header=False)
                        worksheet = writer.sheets[str(key)[0:30]]
                        imgDest = f'{os.getcwd()}\plot{i}.png'
                        worksheet.insert_image('N1', imgDest)

                # Delete images
                # for i, img in enumerate(imgs):
                #     os.remove(f'{os.getcwd()}\plot{i}.png')

                writer.save()
                notification.create('info', 'Data successfully exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for i, img in enumerate(imgs):
                os.remove(f'{os.getcwd()}\plot{i}.png')
            self.exportOptions.destroy()
        else:
            print('EXPORT TO NEW - WHOLE PROJECT')
            project = app.getActiveProject()
            subjects = project.getSubjects()

            # Create project plots
            self.images['Mean-SD'] = []
            df = self.createProjectPlots('Mean-SD')
            self.dfs['Mean-SD'] = df

            self.images['Median-IQR'] = []
            df = self.createProjectPlots('Median-IQR', iqr=True)
            self.dfs['Median-IQR'] = df

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
            try:
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
                # for s in subjects:
                #     tests = s.getTests()
                #     for t in tests:
                #         os.remove(f'{os.getcwd()}\plot{t.id}.png')
                # os.remove(f'{os.getcwd()}\plotProject median-IQR.png')
                # os.remove(f'{os.getcwd()}\plotProject mean-SD.png')

                writer.save()
                notification.create('info', 'Data successfully exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for s in subjects:
                tests = s.getTests()
                for t in tests:
                    os.remove(f'{os.getcwd()}\plot{t.id}.png')
            os.remove(f'{os.getcwd()}\plotProject median-IQR.png')
            os.remove(f'{os.getcwd()}\plotProject mean-SD.png')
            self.exportOptions.destroy()

    def exportToSelected(self):
        excel = app.getActiveProject().data
        ordered, units, mcs = self.getSortedData()

        if self.onlyPlots == True: # Export only created plots
            print('TO SELECTED - ONLY PLOTS')
            self.createDfsOfPlots()
            for key,value in self.dfs.items():
                # print(key, value)
                excel[str(key)[0:30]] = value
                self.sheetNames.append(str(key)[0:30])

            # Create excel
            try:
                saveFile = asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                with pd.ExcelWriter(f'{saveFile.name}.xlsx', engine='xlsxwriter') as writer:
                    for sheet in self.sheetNames:
                        #print(f'sheet: {sheet}')
                        df = pd.DataFrame.from_dict(excel[sheet])
                        df.to_excel(writer, sheet_name=sheet, index=False, header=False)

                        for i, (key, value) in enumerate(self.dfs.items()):
                            if sheet == str(key)[0:30]:
                                #print('osuma')
                                #print(str(key)[0:30])
                                worksheet = writer.sheets[sheet]
                                imgDest = f'{os.getcwd()}\plot{key}.png'
                                worksheet.insert_image('N1', imgDest)

                # Delete images
                # for i, (key, value) in enumerate(self.dfs.items()):
                #     os.remove(f'{os.getcwd()}\plot{key}.png')

                writer.save()
                notification.create('info', 'Data successfully exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for i, (key, value) in enumerate(self.dfs.items()):
                os.remove(f'{os.getcwd()}\plot{key}.png')
            self.exportOptions.destroy()

        else: # Export all values and plots to excel file
            print('TO SELECTED - WHOLE PROJECT')
            if self.importDataMode == 'long':
                for key, value in ordered.items():
                    unit = units[f'{key.split("-")[0]}']
                    mc = mcs[f'{key.split("-")[0]}']
                    # unit = units[key]
                    # mc = mcs[key]
                    if mc == 1:
                        mc = 'Calculated'
                    else:
                        mc = 'Measured'
                    value.insert(0, f'{key} ({unit})-{mc}')
                    excel[self.selectedSheet][key] = value
            else: # 'wide'
                excelTemp = pd.DataFrame.from_dict(excel[self.selectedSheet])

                for key, value in ordered.items():
                    # print(key, value)
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

            df = self.createProjectPlots('Median-IQR', iqr=True)
            excel['Median-IQR'] = df
            self.sheetNames.append('Median-IQR')

            # Create plots for subjects
            subjects = app.getActiveProject().getSubjects()
            plotsDf = pd.DataFrame()
            for s in subjects:
                tests = s.getTests()
                self.images[s.id] = []

                for t in tests:
                    # plotDf = pd.DataFrame()
                    loads = t.workLoads
                    # workLoadObjects = []
                    # for l in loads:
                        # workLoadObjects.append(l.getDetails())

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
                        if sheet == 'Median-IQR':
                            worksheet = writer.sheets[sheet]
                            imgDest = f'{os.getcwd()}\plotProject median-IQR.png'
                            worksheet.insert_image('H1', imgDest)
                        elif sheet == 'Mean-SD':
                            worksheet = writer.sheets[sheet]
                            imgDest = f'{os.getcwd()}\plotProject mean-SD.png'
                            worksheet.insert_image('H1', imgDest)

                # # Delete images
                # for s in subjects:
                #     tests = s.getTests()
                #     for t in tests:
                #         os.remove(f'{os.getcwd()}\plot{t.id}.png')
                # os.remove(f'{os.getcwd()}\plotProject median-IQR.png')
                # os.remove(f'{os.getcwd()}\plotProject mean-SD.png')
                    
                writer.save()
                notification.create('info', 'Data successfully exported', 5000)
            except:
                notification.create('error', 'Data not exported', 5000)

            # Delete images
            for s in subjects:
                tests = s.getTests()
                for t in tests:
                    os.remove(f'{os.getcwd()}\plot{t.id}.png')
            os.remove(f'{os.getcwd()}\plotProject median-IQR.png')
            os.remove(f'{os.getcwd()}\plotProject mean-SD.png')
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
                        app.getPlottingPanel().calc(workLoadObjects[i], details)
                        updatedDetails = workLoadObjects[i].getWorkLoadDetails()
                        # print(updatedDetails)

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
                            # print(value, unit, mc)
                    except Exception as err:
                        # print(f'ERROR: {err}')
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
                # print(f'from ordered: {key, value}')
                if key.split('-')[0] == v:
                    ordered[key] = value

        return ordered, units, mcs

    def createPlot(self, workLoads, id): #workloads = workloaddetails object
        PvO2 = np.arange(0,100,1)
        plot = plt.subplots()
        fig, ax = plot

        fig.set_figheight(4)
        fig.set_figwidth(5.4)

        ax.set_title('O2 Pathway')
        ax.set_xlabel('PvO\u2082 (mmHg)')
        ax.set_ylim(top=5000, bottom=0)
        ax.set_xlim(left=0, right=100)
        plt.subplots_adjust(bottom=0.175)

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

        leg = ax.legend(handles=handles , loc='upper right',
            fancybox=True, shadow=True, ncol=2)
        
        fig.savefig(f'plot{id}.png')
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

        # print(f'initializes rows: {self.temp.keys()}')

        for li, l in enumerate(filteredLoads):
            details = l.getDetails().getWorkLoadDetails()
            # app.getPlottingPanel().calc(workLoads[li], details)
            # updatedDetails = workLoads[li].getDetails().getWorkLoadDetails()
            if projectPlot == False:
                app.getPlottingPanel().calc(l.getDetails(), details)
            updatedDetails = l.getDetails().getWorkLoadDetails()
            # print(f'DO2 in updatedDetails: {updatedDetails["DO2"]}')

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
                    # print(key, value)
                    # if key.split('-')[0] == v:
                    #     ordered[key] = value
                    ordered[key] = value

        # Create plot
        workLoadObjects = []
        for l in filteredLoads:
            workLoadObjects.append(l.getDetails())

        if projectPlot == False:
            self.createPlot(workLoadObjects, id)

        try:
            self.images[sid].append('img')
        except:
            pass
                        
        for key, value in ordered.items():
            # unit = self.units[f'{key.split("-")[0]}']
            # mc = self.mcs[f'{key.split("-")[0]}']
            unit = self.units[key]
            mc = self.mcs[key]
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
        
        app.plotMean(test=dummyTest, subjects=subjects, plotProject=True, iqr=iqr, export=True)
        workLoadDetailObjects = []
        for w in dummyTest.getWorkLoads():
            # print(w.getDetails())
            workLoadDetailObjects.append(w.getDetails())
            # print(f'plotMeanista detailit: {w.getDetails().getWorkLoadDetails()}')
        self.createPlot(workLoadDetailObjects, dummyTest.id)
        
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
            self.createPlot(p.workLoadDetailsObjects, id)
            
            self.dfs[id] = df