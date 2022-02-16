from itertools import tee
from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.notification import notification
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

#
# BUG: Jostain syystä päivittää laskennan oudosti jos klikkaa oikealla painikkeella scale barista
#

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
        self.plotNotebook = ttk.Notebook(self.container)
        try:
            print(f'PACKINFO: {self.plotNotebook.pack_info()}')
        except TclError:
            return

    def plot(self):
        # Check if plotNotebook is visible and if not, make it visible
        try:
            self.plotNotebook.pack_info()
        except TclError:
            self.plotNotebook.pack(expand=TRUE, fill=BOTH)

        self.workLoads = app.getActiveTest().getWorkLoads()

        # Create tab for the plot
        plotTabObject = PlotTab(self.plotNotebook)
        plotTab = plotTabObject.createPlotTab()
        
        # Add plot to the notebook and objects list of plots
        self.plotNotebook.add(plotTab, text=app.getActiveTest().id)
        self.plots.append(plotTabObject)

class PlotTab(object):
    def __init__(self, parentFrame):
        self.loadTabs = []
        self.parentFrame = parentFrame
        self.activeTest = app.getActiveTest()
        self.activeTestId = self.activeTest.id
        self.workLoads = self.activeTest.getWorkLoads()
        
    def createPlotTab(self):
        # Create tab for test
        self.tabFrame = ttk.Frame(self.parentFrame, width=300, height=200)
        self.tabFrame.pack(expand=TRUE)

        # Plot canvasframe
        self.canvasFrame = ttk.Frame(self.tabFrame)
        self.canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.createPlot()

        # Create loads notebook frame and notebook
        self.loadNotebookFrame = ttk.Frame(self.tabFrame)
        self.loadNotebookFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        self.loadNotebook = ttk.Notebook(self.loadNotebookFrame)
        self.loadNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tabs for loads
        for i, w in enumerate(self.workLoads):

            loadTabObject = LoadTab(self, i, self.activeTestId, w, self.loadNotebook)
            loadTab = loadTabObject.createLoadTab()
            self.loadNotebook.add(loadTab, text=f'Load{w.id+1}')
            self.loadTabs.append(loadTabObject)

        return self.tabFrame
    
    def createPlot(self):
        PvO2 = np.arange(0,100,1)
        self.fig, ax = plt.subplots()
        ax.set_ylim(top=5000, bottom=0)
        ax.set_xlim(left=0, right=100)
        self.handles = []

        for i, w in enumerate(self.workLoads):
            details = w.getWorkLoadDetails()
            
            try:
                y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.calc(float(details['Q']), float(details['VO2']), float(details['Hb']), float(details['SaO2']))
                #y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.calc(float(14+i), float(1.0+i), float(13.0+i), float(99.0))
            except (ValueError, TypeError):
                notification.create('error', 'Unable to compute with given values. Check values', 5000)
                return False

            w.setCalcResults(QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc)

            line, = ax.plot(PvO2, y, lw=2, color=f'C{i}', label=f'Load{i+1}')
            curve, = ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=f'Load{i+1}')
            dot, = ax.plot(xi, yi, 'o', color='red', label=f'Load{i+1}')

            self.handles.insert(i, line)

        self.leg = ax.legend(handles=self.handles , loc='upper center', bbox_to_anchor=(0.5, 1.1),
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
            #print( 2* DO2 * (PvO2[idx]+i) )
            y_temp = 2* DO2 * (PvO2[idx]+i)

            #print( Q * ( 1.34 * hb * ( SaO2 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10 )
            y2_temp = Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10
            #print(y_temp-y2_temp)

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


class LoadTab(object):
    def __init__(self, plotTab, index, testId, workLoad, parentNotebook):
        self.parentPlotTab = plotTab
        self.index = index
        self.testId = testId
        self.workLoad = workLoad
        self.details = workLoad.getWorkLoadDetails()
        self.parentNotebook = parentNotebook

    def createLoadTab(self):
        self.loadtab = ttk.Frame(self.parentNotebook)
        self.loadtab.grid()
        
        #Content
        ttk.Label(self.loadtab, text=f'Load: {self.details["Load"]}').grid(column=0, row=0)

        VO2 = f'VO2-{self.testId}-{self.index}'
        Q = f'Q-{self.testId}-{self.index}'
        Hb = f'Hb-{self.testId}-{self.index}'
        SaO2 = f'SaO2-{self.testId}-{self.index}'

        for var in app.strVars:
            if var._name == VO2:
                self.vo2Var = var
            elif var._name == Q:
                self.qVar = var
            elif var._name == Hb:
                self.hbVar = var
            elif var._name == SaO2:
                self.sao2Var = var

        ttk.Label(self.loadtab, text='VO2').grid(column=0, row=1)
        vo2Slider = ttk.Scale(self.loadtab, from_=0, to=5, orient=HORIZONTAL, value=self.vo2Var.get(), variable=self.vo2Var)
        vo2Slider.grid(column=1, row=1)
        vo2Entry = ttk.Entry(self.loadtab, textvariable=self.vo2Var, width=7)
        vo2Entry.grid(column=2, row=1)
        self.vo2Var.trace('w', self.updatePlot)

        ttk.Label(self.loadtab, text='Q').grid(column=0, row=2)
        qSlider = ttk.Scale(self.loadtab, from_=10, to=20, orient=HORIZONTAL, value=self.qVar.get(), variable=self.qVar)
        qSlider.grid(column=1, row=2)
        qEntry = ttk.Entry(self.loadtab, textvariable=self.qVar, width=7)
        qEntry.grid(column=2, row=2)
        self.qVar.trace('w', self.updatePlot)

        ttk.Label(self.loadtab, text='Hb').grid(column=0, row=3)
        hbSlider = ttk.Scale(self.loadtab, from_=10, to=20, orient=HORIZONTAL, value=self.hbVar.get(), variable=self.hbVar)
        hbSlider.grid(column=1, row=3)
        hbEntry = ttk.Entry(self.loadtab, textvariable=self.hbVar, width=7)
        hbEntry.grid(column=2, row=3)
        self.hbVar.trace('w', self.updatePlot)

        ttk.Label(self.loadtab, text='SaO2').grid(column=0, row=4)
        sao2Slider = ttk.Scale(self.loadtab, from_=80, to=100, orient=HORIZONTAL, value=self.sao2Var.get(), variable=self.sao2Var)
        sao2Slider.grid(column=1, row=4)
        sao2Entry = ttk.Entry(self.loadtab, textvariable=self.sao2Var, width=7)
        sao2Entry.grid(column=2, row=4)
        self.sao2Var.trace('w', self.updatePlot)

        self.cao2 = ttk.Label(self.loadtab, text=f'CaO2:')
        self.cao2.grid(column=0, row=5)
        self.cao2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["CaO2"]) } {self.details["CaO2_unit"]}')
        self.cao2_valUnit.grid(column=1, row=5)

        self.cvo2 = ttk.Label(self.loadtab, text=f'CvO2:')
        self.cvo2.grid(column=0, row=6)
        self.cvo2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["CvO2"]) } {self.details["CvO2_unit"]}')
        self.cvo2_valUnit.grid(column=1, row=6)

        self.cavo2 = ttk.Label(self.loadtab, text=f'CavO2:')
        self.cavo2.grid(column=0, row=7)
        self.cavo2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["CavO2"]) } {self.details["CavO2_unit"]}')
        self.cavo2_valUnit.grid(column=1, row=7)

        self.pvo2 = ttk.Label(self.loadtab, text=f'PvO2:')
        self.pvo2.grid(column=0, row=8)
        self.pvo2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["pVO2"]) } {self.details["pVO2_unit"]}')
        self.pvo2_valUnit.grid(column=1, row=8)

        self.svo2 = ttk.Label(self.loadtab, text=f'SvO2:')
        self.svo2.grid(column=0, row=9)
        self.svo2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["SvO2"]) } {self.details["SvO2_unit"]}')
        self.svo2_valUnit.grid(column=1, row=9)

        self.qao2 = ttk.Label(self.loadtab, text=f'QaO2:')
        self.qao2.grid(column=0, row=10)
        self.qao2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["QaO2"]) } {self.details["QaO2_unit"]}')
        self.qao2_valUnit.grid(column=1, row=10)

        self.do2 = ttk.Label(self.loadtab, text=f'DO2:')
        self.do2.grid(column=0, row=11)
        self.do2_valUnit = ttk.Label(self.loadtab, text=f'{"{0:.2f}".format(self.details["DO2"]) } {self.details["DO2_unit"]}')
        self.do2_valUnit.grid(column=1, row=11)

        return self.loadtab

    def updatePlot(self, val=None, name=None, index=None, mode=None, loadtab=None):
        try:
            y, y2, xi, yi, QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc = self.parentPlotTab.calc(float(self.qVar.get()), float(self.vo2Var.get()), float(self.hbVar.get()), float(self.sao2Var.get()))
        except (ValueError, TypeError):
            print('Calculation error')
            notification.create('error', 'Unable to compute with given values. Check values', 5000)
            return False

        self.workLoad.setCalcResults(QO2, DO2, Ca_vO2, CaO2, CvO2, SvO2_calc, PvO2_calc)
        self.parentPlotTab.canvas.get_tk_widget().destroy()
        self.parentPlotTab.toolbar.destroy()
        self.parentPlotTab.createPlot()
        self.updateDetails()

    def updateDetails(self):
        self.details = self.workLoad.getWorkLoadDetails()
        self.cao2_valUnit.config(text=f'{"{0:.2f}".format(self.details["CaO2"]) } {self.details["CaO2_unit"]}')
        self.cvo2_valUnit.config(text=f'{"{0:.2f}".format(self.details["CvO2"]) } {self.details["CvO2_unit"]}')
        self.cavo2_valUnit.config(text=f'{"{0:.2f}".format(self.details["CavO2"]) } {self.details["CavO2_unit"]}')
        self.pvo2_valUnit.config(text=f'{"{0:.2f}".format(self.details["pVO2"]) } {self.details["pVO2_unit"]}')
        self.svo2_valUnit.config(text=f'{"{0:.2f}".format(self.details["SvO2"]) } {self.details["SvO2_unit"]}')
        self.qao2_valUnit.config(text=f'{"{0:.2f}".format(self.details["QaO2"]) } {self.details["QaO2_unit"]}')  
        self.do2_valUnit.config(text=f'{"{0:.2f}".format(self.details["DO2"]) } {self.details["DO2_unit"]}')