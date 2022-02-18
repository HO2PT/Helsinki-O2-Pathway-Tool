from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel
from objects.app import app
from modules.notification import notification
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class PlottingPanel(object):
    def __init__(self, mainFrame):
        self.plots = []
        self.mainFrame = mainFrame

        s = ttk.Style()
        bg = s.lookup('TFrame', 'background')
        s.configure('plottingPanel.TFrame', background=bg)

        self.container = ttk.Frame(mainFrame, style='plottingPanel.TFrame')
        self.container.pack(fill=BOTH, expand=TRUE)

        # Plots notebook
        self.plotNotebook = ttk.Notebook(self.container, style='loadNotebook.TNotebook')
        self.plotNotebook.bind('<Button-1>', lambda e: self.closePlotTab(e))
        try:
            print(f'PACKINFO: {self.plotNotebook.pack_info()}')
        except TclError:
            return

    def closePlotTab(self, e):
        if self.plotNotebook.identify(e.x, e.y) == 'close':
            if askokcancel("Confirm", "Do you want to remove the tab?"):
                clickedTabIndex = self.plotNotebook.index(f'@{e.x},{e.y}')
                self.plotNotebook.forget(clickedTabIndex)
                del self.plots[clickedTabIndex]

    def plot(self):
        # Check if plotNotebook is visible and if not, make it visible
        self.workLoads = app.getActiveTest().getWorkLoads()
        self.validValues = True
        
        print('VALIDATING VALUES')
        for i, w in enumerate(self.workLoads):
            details = w.getDetails().getWorkLoadDetails()

            if self.validate(float(details['Q']), float(details['VO2']), float(details['Hb']), float(details['SaO2'])) == False:
                self.validValues = False
                notification.create('error', f'Unable to compute with given values. Check {i+1}. load', 5000)

        # Proceed if values are valid
        if self.validValues:
            print('VALUES OK')
            # Check if plotNotebook is visible and if not, make it visible
            try:
                self.plotNotebook.pack_info()
            except TclError:
                self.plotNotebook.pack(expand=TRUE, fill=BOTH)

            # Create tab for the plot
            plotTabObject = PlotTab(self.plotNotebook)
            plotTab = plotTabObject.createPlotTab()
                    
            # Add plot to the notebook and objects list of plots
            self.plotNotebook.add(plotTab, text=app.getActiveTest().id)
            self.plots.append(plotTabObject)

    def validate(self, Q, vo2, hb, SaO2):
        try:
            Ca_vO2 = vo2 / Q * 100
        except:
            return False

        try:
            CaO2 = 1.34 * hb * SaO2/100
        except:
            return False

        try:
            CvO2 = CaO2-Ca_vO2
        except:
            return False

        try:
            SvO2_calc = CvO2 / 1.34 / hb
        except:
            return False

        try:
            QO2 = Q * CaO2 * 10
        except:
            return False

        try:
            a = 11700 * np.float_power( ( np.float_power(SvO2_calc,-1) - 1 ), -1 )
        except:
            return False

        try:
            b = np.float_power( 50**3 + np.float_power(a,2) , 0.5 )
        except:
            return False
        
        try:
            PvO2_calc = np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        except:
            return False
        
        try:
            DO2 = vo2 / 2 / PvO2_calc * 1000
        except:
            return False
        
        PvO2 = np.arange(0,100,1)
        
        try:
            y = 2* DO2 * PvO2
        except:
            return False
        
        try:
            SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )
        except:
            return False
        
        try:
            y2 = Q * ( 1.34 * hb * ( SaO2/100 - SvO2 ) ) * 10
        except:
            return False

        # Correction and calculation of intersection point
        try:
            idx = np.argwhere(np.diff(np.sign(y - y2))).flatten()
        except:
            return False
        
        yDiff = []

        for i in np.arange(0, 1, 0.1):
            y_temp = 2* DO2 * (PvO2[idx]+i)
            y2_temp = Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10
            try:
                yDiff.append( (float(y_temp)-float(y2_temp)) )
            except:
                return False

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)
        
        return True

class PlotTab(object):
    def __init__(self, parentFrame):
        self.plot = {}
        self.loadTabs = []
        self.parentFrame = parentFrame
        self.activeTest = app.getActiveTest()
        self.activeTestId = self.activeTest.id
        self.workLoads = self.activeTest.getWorkLoads() # Workload objects
        
    def createPlotTab(self):
        # Create tab for test
        self.tabFrame = ttk.Frame(self.parentFrame, width=300, height=200)
        self.tabFrame.pack(expand=TRUE)

        # Plot canvasframe
        self.canvasFrame = ttk.Frame(self.tabFrame)
        self.canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.createPlot()

        # Create loads notebook frame and loadnotebook
        self.loadNotebookFrame = ttk.Frame(self.tabFrame)
        self.loadNotebookFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        self.loadNotebook = ttk.Notebook(self.loadNotebookFrame)
        self.loadNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tabs for loads
        for i, w in enumerate(self.workLoads):
            loadTabObject = PlotLoadTab(self, i, self.activeTestId, w, self.loadNotebook)
            loadTab = loadTabObject.createLoadTab()
            self.loadNotebook.add(loadTab, text=w.getName())
            self.loadTabs.append(loadTabObject)

        return self.tabFrame

    def createPlot(self):
        PvO2 = np.arange(0,100,1)

        self.fig, self.ax = plt.subplots()

        self.ax.set_ylim(top=5000, bottom=0)
        self.ax.set_xlim(left=0, right=100)
        self.handles = []

        for i, w in enumerate(self.workLoads):
            details = w.getDetails().getWorkLoadDetails()
            
            try:
                y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.calc(float(details['Q']), float(details['VO2']), float(details['Hb']), float(details['SaO2']))
                #y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.calc(float(14+i), float(1.0+i), float(13.0+i), float(99.0))
            except (ValueError, TypeError):
                notification.create('error', 'Unable to compute with given values. Check values', 5000)
                return False

            w.getDetails().setCalcResults(QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc)

            line, = self.ax.plot(PvO2, y, lw=2, color=f'C{i}', label=f'Load{i+1}')
            curve, = self.ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=f'Load{i+1}')
            dot, = self.ax.plot(xi, yi, 'o', color='red', label=f'Load{i+1}')

            self.handles.insert(i, line)

        self.leg = self.ax.legend(handles=self.handles , loc='upper center', bbox_to_anchor=(0.5, 1.1),
            fancybox=True, shadow=True, ncol=5)

        # we will set up a dict mapping legend line to orig line, and enable
        # picking on the legend line
        lines = plt.gca().get_legend_handles_labels()[0]
        self.lined = dict()
        i = 0
        temp = []
        for legline, origline in zip(self.leg.get_lines(), lines):
            legline.set_picker(5)  # 5 pts tolerance
            
            for x in range(0,3):
                temp.append(lines[i])
                i += 1

            self.lined[legline] = temp
            temp = []
        
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas = FigureCanvasTkAgg(self.fig, self.canvasFrame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvasFrame)
        self.toolbar.update()

    def calc(self, Q, vo2, hb, SaO2):
        #Q = hr * sv / 1000

        # Computated variables
        Ca_vO2 = vo2 / Q * 100
        #print(f"Ca_vO2: {Ca_vO2}")

        CaO2 = 1.34 * hb * SaO2/100
        #print(f"CaO2: {CaO2}")

        CvO2 = CaO2-Ca_vO2
        #print(f"CvO2: {CvO2}")

        SvO2_calc = CvO2 / 1.34 / hb
        #print(f"SvO2: {SvO2}")

        # Convection
        QO2 = Q * CaO2 * 10 #ml/min
        #print(f"QO2: {QO2}")

        # Calculate diffusion DO2
        a = 11700 * np.float_power( ( np.float_power(SvO2_calc,-1) - 1 ), -1 )
        #print(f'A: {a}')

        b = np.float_power( 50**3 + np.float_power(a,2) , 0.5 )
        #print(f'B: {b}')

        PvO2_calc = np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        #print(f'PvO2: {PvO2}')

        DO2 = vo2 / 2 / PvO2_calc * 1000
        #print(f"DO2:{DO2}")

        PvO2 = np.arange(0,100,1)

        # Fick's law - Diffusion line 
        # VO2 = DO2 * 2 * PvO2

        y = 2* DO2 * PvO2

        # Fick's principle - Convection curve 
        # VO2 = CO * C(a-v)O2                           | CaO2 = 1.34 x Hb x SaO2 
        #                                               | CvO2 = 1.34 x Hb x SvO2
        #
        # f(PvO2) = CO x ( 1.34 x Hb (SaO2 - SvO2) )    | SvO2 = ((23400((PvO2)^3+ 150PvO2)^-1) + 1)^-1
        # 
        # f(PvO2) = CO x (1.34 x Hb x (SaO2 - ((23400((PvO2)^3+ 150PvO2)^-1) + 1)^-1)

        SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )

        y2 = Q * ( 1.34 * hb * ( SaO2/100 - SvO2 ) ) * 10

        # Correction and calculation of intersection point
        idx = np.argwhere(np.diff(np.sign(y - y2))).flatten()
        yDiff = []

        for i in np.arange(0, 1, 0.1):
            y_temp = 2* DO2 * (PvO2[idx]+i)
            y2_temp = Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10

            try:
                yDiff.append( (float(y_temp)-float(y2_temp)) )
            except TypeError:
                return

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)
        
        return y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc

    def onpick(self, event):

        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        legline = event.artist
        origline = self.lined[legline]

        for line in origline:
            vis = not line.get_visible()
            line.set_visible(vis)

            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled
            if vis:
                legline.set_alpha(1.0)
            else:
                legline.set_alpha(0.2)
        self.fig.canvas.draw()

    def on_click(self, event):
        # If middle or righbutton is pressed -> show/hide all lines
        if event.guiEvent.num == 3:
            visible = False
            alpha = 0.2
        elif event.guiEvent.num == 2:
            visible = True
            alpha = 1.0
        else:
            return

        # Show/hide lines
        lines = plt.gca().get_legend_handles_labels()[0]
        legLines = self.leg.get_lines()

        for line in lines:
            line.set_visible(visible)

        for legLine in legLines:
            legLine.set_alpha(alpha)

        self.fig.canvas.draw()

class PlotLoadTab(object):
    def __init__(self, plotTab, index, testId, workLoad, parentNotebook):
        self.parentPlotTab = plotTab
        self.index = index
        self.testId = testId
        self.workLoad = workLoad # Load object
        self.details = workLoad.getDetails().getWorkLoadDetails()
        self.parentNotebook = parentNotebook

    def createLoadTab(self):
        self.loadtab = ttk.Frame(self.parentNotebook)
        self.loadtab.grid()
        
        #Content
        ttk.Label(self.loadtab, text=f'Load: {self.details["Load"]}').grid(column=0, row=0)

        vo2Value = self.details['VO2']
        self.vo2Row = LoadTabRow(self.loadtab, 'VO2', vo2Value, self.index, self.testId, 1, (0,5))
        self.vo2Row.var.trace('w', self.updatePlot)

        qValue = self.details['Q']
        self.qRow = LoadTabRow(self.loadtab, 'Q', qValue, self.index, self.testId, 2, (10,20))
        self.qRow.var.trace('w', self.updatePlot)

        hbValue = self.details['Hb']
        self.hbRow = LoadTabRow(self.loadtab, 'Hb', hbValue, self.index, self.testId, 3, (10,20))
        self.hbRow.var.trace('w', self.updatePlot)

        sao2Value = self.details['SaO2']
        self.sao2Row = LoadTabRow(self.loadtab, 'SaO2', sao2Value, self.index, self.testId, 4, (80,100))
        self.sao2Row.var.trace('w', self.updatePlot)

        self.cao2Row = LoadTabRow(self.loadtab, 'CaO2', None, None, None, 5, None, self.details)
        self.cvo2Row = LoadTabRow(self.loadtab, 'CvO2', None, None, None, 6, None, self.details)
        self.cavo2Row = LoadTabRow(self.loadtab, 'CavO2', None, None, None, 7, None, self.details)
        self.pvo2Row = LoadTabRow(self.loadtab, 'PvO2', None, None, None, 8, None, self.details)
        self.svo2Row = LoadTabRow(self.loadtab, 'SvO2', None, None, None, 9, None, self.details)
        self.qao2Row = LoadTabRow(self.loadtab, 'QaO2', None, None, None, 10, None, self.details)
        self.do2Row = LoadTabRow(self.loadtab, 'DO2', None, None, None, 11, None, self.details)

        return self.loadtab

    def updatePlot(self, val=None, name=None, index=None, mode=None, loadtab=None):
        try:
            y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.parentPlotTab.calc(
                float(self.qRow.getValue()), 
                float(self.vo2Row.getValue()), 
                float(self.hbRow.getValue()), 
                float(self.sao2Row.getValue())
                )

            self.workLoad.getDetails().setCalcResults(QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc)
            
            # Split figure lines to 3's
            allLines = self.parentPlotTab.ax.get_lines()
            temp = []
            mappedLines = {}
            i = 0
            idx = 0

            for line in allLines:
                temp.append(line)
                if i == 2:
                    mappedLines[idx] = temp
                    temp = []
                    i = 0
                    idx += 1
                else:
                    i += 1

            # Update x and y values for plot
            mappedLines[self.index][0].set_ydata(y)
            mappedLines[self.index][1].set_ydata(y2)
            mappedLines[self.index][2].set_ydata(yi)
            mappedLines[self.index][2].set_xdata(xi)

            self.parentPlotTab.fig.canvas.draw()
            self.parentPlotTab.fig.canvas.flush_events()

            self.updateDetails()
        except (ValueError, TypeError):
            notification.create('error', 'Unable to compute with given values. Check values', 5000)

    def updateDetails(self):
        self.details = self.workLoad.getDetails().getWorkLoadDetails()
        self.cao2Row.updateText(self.details)
        self.cvo2Row.updateText(self.details)
        self.cavo2Row.updateText(self.details)
        self.pvo2Row.updateText(self.details)
        self.svo2Row.updateText(self.details)
        self.qao2Row.updateText(self.details)
        self.do2Row.updateText(self.details)

class LoadTabRow(object):
    def __init__(self, parent, label, value, index, id, row, scale, details=None):
        self.parent = parent
        self.label = label
        self.value = value
        self.index = index
        self.id = id
        self.row = row
        self.scale = scale
        self.details = details
        
        if self.scale == None:
            self.labelElem = ttk.Label(self.parent, text=f'{label}:')
            self.labelElem.grid(column=0, row=row)
            self.valUnit = ttk.Label(self.parent, text=f'{"{0:.2f}".format(self.details[label])} {self.details[f"{label}_unit"]}')
            self.valUnit.grid(column=1, row=row, sticky='w')
        else:
            self.var = DoubleVar(self.parent, value=f'{"{0:.2f}".format(float(self.value))}', name=f'{self.label}-{self.id}-Plot-{self.index}')

            ttk.Label(self.parent, text=self.label).grid(column=0, row=row)
            slider = ttk.Scale(self.parent, from_=self.scale[0], to=self.scale[1], orient=HORIZONTAL, value=self.value, variable=self.var)
            slider.grid(column=1, row=row)
            entry = ttk.Entry(self.parent, textvariable=self.var, width=7)
            entry.grid(column=2, row=row)

    def getValue(self):
        return self.var.get()
    
    def updateText(self, details):
        self.valUnit.config(text=f'{"{0:.2f}".format(details[self.label]) } {details[f"{self.label}_unit"]}')