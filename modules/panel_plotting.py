from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel
from objects.app import app
from modules.notification import notification
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        self.plot = None
        self.loadTabs = []
        self.parentFrame = parentFrame
        self.activeTest = app.getActiveTest()
        self.activeTestId = self.activeTest.id
        self.origWorkLoads = self.activeTest.getWorkLoads()
        self.workLoads = copy.deepcopy(self.origWorkLoads) # Workload objects
        
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
            loadTabObject = PlotLoadTab(self, i, self.activeTestId, w, self.loadNotebook, self.plot)
            loadTab = loadTabObject.createLoadTab()
            self.loadNotebook.add(loadTab, text=w.getName())
            self.loadTabs.append(loadTabObject)

        return self.tabFrame

    def createPlot(self):
        PvO2 = np.arange(0,100,1)

        self.plot = plt.subplots()
        self.fig, self.ax = self.plot

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

    def getTestId(self):
        return self.activeTestId

class PlotLoadTab(object):
    def __init__(self, plotTab, index, testId, workLoad, parentNotebook, plot):
        self.parentPlotTab = plotTab
        self.index = index
        self.testId = testId
        self.workLoad = workLoad # Load object
        self.details = workLoad.getDetails().getWorkLoadDetails()
        self.parentNotebook = parentNotebook
        self.plot = plot

    def createLoadTab(self):
        self.loadtab = ttk.Frame(self.parentNotebook)
        self.loadtab.pack()

        # Details frame
        self.loadDetails = ttk.Frame(self.loadtab)
        self.loadDetails.grid()
        
        ttk.Label(self.loadDetails, text=f'Load: {self.details["Load"]}').grid(column=0, row=0)

        vo2Value = self.details['VO2']
        self.vo2Row = LoadTabRow(self.loadDetails, 'VO2', vo2Value, self.index, self.testId, 1, (0,5))
        self.vo2Row.var.trace('w', self.updatePlot)

        qValue = self.details['Q']
        self.qRow = LoadTabRow(self.loadDetails, 'Q', qValue, self.index, self.testId, 2, (10,20))
        self.qRow.var.trace('w', self.updatePlot)

        hbValue = self.details['Hb']
        self.hbRow = LoadTabRow(self.loadDetails, 'Hb', hbValue, self.index, self.testId, 3, (10,20))
        self.hbRow.var.trace('w', self.updatePlot)

        sao2Value = self.details['SaO2']
        self.sao2Row = LoadTabRow(self.loadDetails, 'SaO2', sao2Value, self.index, self.testId, 4, (80,100))
        self.sao2Row.var.trace('w', self.updatePlot)

        self.cao2Row = LoadTabRow(self.loadDetails, 'CaO2', None, None, None, 5, None, self.details)
        self.cvo2Row = LoadTabRow(self.loadDetails, 'CvO2', None, None, None, 6, None, self.details)
        self.cavo2Row = LoadTabRow(self.loadDetails, 'CavO2', None, None, None, 7, None, self.details)
        self.pvo2Row = LoadTabRow(self.loadDetails, 'PvO2', None, None, None, 8, None, self.details)
        self.svo2Row = LoadTabRow(self.loadDetails, 'SvO2', None, None, None, 9, None, self.details)
        self.qao2Row = LoadTabRow(self.loadDetails, 'QaO2', None, None, None, 10, None, self.details)
        self.do2Row = LoadTabRow(self.loadDetails, 'DO2', None, None, None, 11, None, self.details)

        # Plot options
        PlotOptions(self.loadtab, self.plot, self.index)

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

            # Update objects plot for exporting
            self.plot = (self.parentPlotTab.fig, self.parentPlotTab.ax)

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

class PlotOptions(object):
    def __init__(self, parent, plotObject, loadIndex):
        self.plotObject = plotObject
        self.loadIndex = loadIndex

        self.plotOptions = ttk.LabelFrame(parent, text='Plot options')
        self.plotOptions.grid()

        ttk.Label(self.plotOptions, text='Set Y-axis max. value').grid(column=0, row=0)

        # Set y limit
        self.yValue = StringVar(self.plotOptions, value=plotObject[1].get_ylim()[1])
        self.yEntry = ttk.Entry(self.plotOptions, textvariable=self.yValue)
        self.yEntry.grid(column=0, row=1)
        self.yValue.trace('w', self.updateY)
        ttk.Button(self.plotOptions, text='Set', command=lambda: self.updateFig()).grid(column=1, row=1)

        # Set step size
        ttk.Label(self.plotOptions, text='Tick count in y-axis:').grid(column=0, row=2)
        ttk.Button(self.plotOptions, text='+', command=lambda: self.incTicks()).grid(column=2, row=2)
        ttk.Button(self.plotOptions, text='-', command=lambda: self.decTicks()).grid(column=1, row=2)

        # Set line shape
        ttk.Label(self.plotOptions, text='Change line type').grid(column=0, row=3)
        self.lineTypeMenuButton = ttk.Menubutton(self.plotOptions)
        lineTypeMenu = Menu(self.lineTypeMenuButton, tearoff=False)
        lineTypeMenu.add_command(label='Solid', command=lambda: self.changeLineType(0))
        lineTypeMenu.add_command(label='Dotted', command=lambda: self.changeLineType(1))
        lineTypeMenu.add_command(label='Dashed', command=lambda: self.changeLineType(2))
        lineTypeMenu.add_command(label='Dashdot', command=lambda: self.changeLineType(3))
        self.lineTypeMenuButton['menu']=lineTypeMenu
        
        if self.mapLines()[self.loadIndex][0].get_linestyle() == '-':
            self.lineTypeMenuButton.config(text='Solid')
        elif self.mapLines()[self.loadIndex][0].get_linestyle() == ':':
            self.lineTypeMenuButton.config(text='Dotted')
        elif self.mapLines()[self.loadIndex][0].get_linestyle() == '--':
            self.lineTypeMenuButton.config(text='Dashed')
        elif self.mapLines()[self.loadIndex][0].get_linestyle() == '-.':
            self.lineTypeMenuButton.config(text='Dashdot')

        self.lineTypeMenuButton.grid(column=1, row=3)

        # Set line color
        ttk.Label(self.plotOptions, text='Change line color').grid(column=0, row=4)
        self.lineColorMenuButton = ttk.Menubutton(self.plotOptions)

        lineColorMenu = Menu(self.lineColorMenuButton, tearoff=False)
        lineColorMenu.add_command(label='Blue', command=lambda: self.changeColor(0))
        lineColorMenu.add_command(label='Orange', command=lambda: self.changeColor(1))
        lineColorMenu.add_command(label='Green', command=lambda: self.changeColor(2))
        lineColorMenu.add_command(label='Red', command=lambda: self.changeColor(3))
        lineColorMenu.add_command(label='Purple', command=lambda: self.changeColor(4))
        lineColorMenu.add_command(label='Brown', command=lambda: self.changeColor(5))
        lineColorMenu.add_command(label='Pink', command=lambda: self.changeColor(6))
        lineColorMenu.add_command(label='Gray', command=lambda: self.changeColor(7))
        lineColorMenu.add_command(label='Olive', command=lambda: self.changeColor(8))
        lineColorMenu.add_command(label='Cyan', command=lambda: self.changeColor(9))

        self.lineColorMenuButton['menu']=lineColorMenu
        self.lineColorMenuButton.config(text= self.getInitialColor(self.mapLines()[self.loadIndex][0].get_color()) )
        self.lineColorMenuButton.grid(column=1, row=4)

        # Hide legend
        ttk.Button(self.plotOptions, text='Hide legend', command=lambda: self.hideLegend()).grid(column=0, row=5)
    
        """ # Toolbar
        self.toolbarContainer = ttk.Frame(self.plotOptions)
        self.toolbarContainer.grid(columnspan=3)
        self.toolbar = NavigationToolbar2Tk(self.plotObject[0].canvas, self.toolbarContainer)
        self.toolbar.update()
        self.plotObject[1].axes.format_coord = lambda x, y: '' """

    def hideLegend(self):
        legend = self.plotObject[1].get_legend()
        vis = legend.get_visible()
        if vis:
            legend.set_visible(False)
        else:
            legend.set_visible(True)
        self.plotObject[0].canvas.draw()

    def getInitialColor(self, color):
        if color == 'C0':
            return 'Blue'
        elif color == 'C1':
            return 'Orange'
        elif color == 'C2':
            return 'Green'
        elif color == 'C3':
            return 'Red'
        elif color == 'C4':
            return 'Purple'
        elif color == 'C5':
            return 'Brown'
        elif color == 'C6':
            return 'Pink'
        elif color == 'C7':
            return 'Gray'
        elif color == 'C8':
            return 'Olive'
        elif color == 'C9':
            return'Cyan'

    def changeColor(self, color):
        mappedLines = self.mapLines()[self.loadIndex]
        mappedLines[0].set_color(f'C{color}')
        mappedLines[1].set_color(f'C{color}')

        if color == 0:
            self.lineColorMenuButton.config(text='Blue')
        elif color == 1:
            self.lineColorMenuButton.config(text='Orange')
        elif color == 2:
            self.lineColorMenuButton.config(text='Green')
        elif color == 3:
            self.lineColorMenuButton.config(text='Red')
        elif color == 4:
            self.lineColorMenuButton.config(text='Purple')
        elif color == 5:
            self.lineColorMenuButton.config(text='Brown')
        elif color == 6:
            self.lineColorMenuButton.config(text='Pink')
        elif color == 7:
            self.lineColorMenuButton.config(text='Gray')
        elif color == 8:
            self.lineColorMenuButton.config(text='Olive')
        elif color == 9:
            self.lineColorMenuButton.config(text='Cyan')

        # Update legend
        legend = self.plotObject[1].get_legend().get_lines()[self.loadIndex]
        legend.set_color(f'C{color}')

        self.plotObject[0].canvas.draw()

    def changeLineType(self, type):
        styles = ['solid', 'dotted', 'dashed', 'dashdot']
        mappedLines = self.mapLines()[self.loadIndex]

        for l in mappedLines:
            l.set_linestyle(styles[type])
        
        self.lineTypeMenuButton.config(text=f"{styles[type]}".title())

        # Update legend
        legend = self.plotObject[1].get_legend().get_lines()[self.loadIndex]
        legend.set_linestyle(styles[type])
        self.plotObject[0].canvas.draw()

    def mapLines(self):
        allLines = self.plotObject[1].get_lines()
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

        return mappedLines

    def incTicks(self):
        yticks = self.plotObject[1].get_yticks()
        """ newTicks = []
        print(yticks)
        step = yticks[1]/2
        for t in yticks:
            if t != 0:
                newTicks.append(t-step)
                newTicks.append(t)
            else:
                newTicks.append(t)
        print(f'NEWTICKS', newTicks)
        self.plotObject[1].set_yticks(newTicks) """
        n = len(yticks)+1
        self.plotObject[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
        self.plotObject[0].canvas.draw()

    def decTicks(self):
        yticks = self.plotObject[1].get_yticks()
        n = len(yticks)-1
        self.plotObject[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
        self.plotObject[0].canvas.draw()

    def updateY(self, name, index, mode):
        pass
    
    def updateFig(self):
        limit = self.yValue.get()
        self.plotObject[1].set_ylim(top=float(limit))
        self.plotObject[0].canvas.draw()

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