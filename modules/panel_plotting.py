from tkinter import *
from tkinter import ttk
import math
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from objects.app import app
from modules.notification import notification
from modules.ScrollableNotebook import ScrollableNotebook
from modules.O2PTSolver import O2PTSolver

class PlottingPanel(ttk.Frame):
    def __init__(self, mainFrame, *args, **kwargs):
        s = ttk.Style()
        bg = s.lookup('TFrame', 'background')
        s.configure('plottingPanel.TFrame', background=bg)

        ttk.Frame.__init__(self, mainFrame, style='plottingPanel.TFrame', *args, **kwargs)
        self.pack(fill=BOTH, expand=TRUE)
        self.plots = []

        # Plots notebook
        self.plotNotebook = ScrollableNotebook(self, parentObj=self, style="loadNotebook.TNotebook", wheelscroll=True)

        try:
            self.plotNotebook.pack_info()
        except TclError:
            return

    def plot(self):
        self.origLoadObjects = []
        visibleLoadTabs = app.testDetailModule.loadNotebook.loadTabs

        for t in visibleLoadTabs:
            tabLoadDetails = t.details
            self.origLoadObjects.append(tabLoadDetails)

        self.workLoadDetailsObjects = copy.deepcopy(self.origLoadObjects) # Workload objects
        validValues = True

        for i, w in enumerate(self.workLoadDetailsObjects):
            details = w.getWorkLoadDetails()
            solver = O2PTSolver(w, details)
            validValues = solver.calc()
            if validValues == False:
                break

        # Proceed if values are valid
        if validValues == True:
            # Check if plotNotebook is visible and if not, make it visible
            try:
                self.plotNotebook.pack_info()
            except TclError:
                self.plotNotebook.pack(expand=TRUE, fill=BOTH)

            # Create tab for the plot
            plotTabObject = PlotTab(self.plotNotebook, self.workLoadDetailsObjects, copy.deepcopy(app.activeTest))

            # Add plot to the notebook and objects list of plots
            self.plotNotebook.add(plotTabObject, text=app.getActiveTest().id)
            self.plots.append(plotTabObject)

            # Make last tab active
            self.plotNotebook.select(self.plotNotebook.index('end')-1)

        else:
            notification.create('error', f'Invalid values. Please check the units and values of {i+1}. load and try again.', 5000)

    def plotProject(self):
        workLoadDetailsObjects = []
        for w in app.getActiveTest().getWorkLoads():
            w = w.getDetails()
            workLoadDetailsObjects.append(w)
        try:
            self.plotNotebook.pack_info()
        except TclError:
            self.plotNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tab for the plot
        plotTabObject = PlotTab(self.plotNotebook, workLoadDetailsObjects, copy.deepcopy(app.activeTest))

        # Add plot to the notebook and objects list of plots
        self.plotNotebook.add(plotTabObject, text=app.getActiveTest().id)
        self.plots.append(plotTabObject)

class PlotTab(ttk.Frame):
    def __init__(self, parentFrame, workLoadDetailsObjects, test, *args, **kwargs):
        ttk.Frame.__init__(self, parentFrame, *args, **kwargs)
        self.pack(expand=TRUE)
        
        self.plot = None
        self.loadTabs = []
        self.activeTest = test
        self.activeTestId = self.activeTest.id
        self.workLoadDetailsObjects = workLoadDetailsObjects # WorkloadDetails objects

        sty = ttk.Style()
        sty.configure(
            'loadNoteBookFrame.TFrame', 
            relief='raised'
        )

        sty.layout('loadNoteBookFrame.TFrame', [
            ('Frame.border', {'sticky': 'nsw'})
        ])
        
        # LEFT SIDE
        # The figure
        self.createLeftSide()
        
        # TOOLBAR
        # Toolbar under the figure
        self.createToolbar()
    
        # RIGHT SIDE
        # Load details and line options container
        self.createRightSide()

        # Helper variable to improve panel resizing
        self.posX = None

    def createLeftSide(self):
        # Plot canvasframe
        self.canvasFrame = ttk.Frame(self)
        self.canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        # Figure instructions
        self.instructions = ttk.Frame(self.canvasFrame)
        self.instructions.pack()
        wrap = ttk.Frame(self.instructions)
        wrap.grid()
        ttk.Label(wrap, text='Left click - show/hide').grid(column=0, row=0, sticky=NSEW)
        wrap.grid_columnconfigure(1, weight=1, minsize=50)
        ttk.Label(wrap, text='Middle click - show all').grid(column=2, row=0, sticky=NSEW)
        wrap.grid_columnconfigure(3, weight=1, minsize=50)
        ttk.Label(wrap, text='Right click - hide all').grid(column=4, row=0, sticky=NSEW)

        self.plotFrame = ttk.Frame(self.canvasFrame)
        self.plotFrame.pack(fill=BOTH, expand=1)
        self.plotFrame.pack_propagate(False)

        self.createPlot()

    def createToolbar(self):
        # Change y-axis unit based on used vo2 unit
        vo2unit = self.workLoadDetailsObjects[0].VO2_unit
        yfmt = ticker.FuncFormatter(self.numfmt)
        plt.gca().yaxis.set_major_formatter(yfmt)
        if vo2unit == 'l/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (l/min)')
            yLimit = self.plot[1].get_ylim()[1] / 1000
        elif vo2unit == 'ml/min':
            plt.gca().yaxis.set_label_text('VO\u2082 (ml/min)')
            yLimit = self.plot[1].get_ylim()[1]

        # Custom figure tools container
        self.toolbarContainer = ttk.Frame(self.canvasFrame)
        self.toolbarContainer.pack(side=BOTTOM, fill=BOTH)

        # Figure toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarContainer, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(fill=X)
        
        # Custom toolbar
        self.toolbarWrapper = ttk.Frame(self.toolbarContainer)
        self.toolbarWrapper.pack(side=LEFT, anchor='nw')

        # Set y limit
        setYLimFrame = ttk.Labelframe(self.toolbarWrapper, text='Set Y-axis max. value', padding=(5,5))
        setYLimFrame.grid(column=0, row=0, padx=(5,5))
        self.yValue = StringVar(setYLimFrame, value=yLimit)
        self.yEntry = ttk.Entry(setYLimFrame, textvariable=self.yValue, width=8)
        self.yEntry.grid(column=0, row=1)
        ttk.Button(setYLimFrame, text='Set', command=lambda: self.setYLim()).grid(column=1, row=1)

        self.toolbarWrapper.grid_columnconfigure(2, minsize=25)

        # Set plot title
        setTitleFrame = ttk.Labelframe(self.toolbarWrapper, text='Set plot title', padding=(5,5))
        setTitleFrame.grid(column=2, row=0, sticky='w', padx=(5,5))
        self.titleEntry = ttk.Entry(setTitleFrame)
        self.titleEntry.grid(column=2, row=1)
        setTitleButton = ttk.Button(setTitleFrame, text='Set', command=self.setPlotTitle)
        setTitleButton.grid(column=3, row=1)

        # Set tick size
        setTicksFrame = ttk.Labelframe(self.toolbarWrapper, text='Set axis ticks', padding=(5,5))
        setTicksFrame.grid(column=4, row=0, columnspan=4, padx=(5,5))

        # Set Y tick size
        ttk.Label(setTicksFrame, text='Y-axis').grid(column=4, row=0, columnspan=2)
        ttk.Button(setTicksFrame, text='+', width=3 ,command=lambda: self.incTicks('y')).grid(column=4, row=1)
        ttk.Button(setTicksFrame, text='-', width=3, command=lambda: self.decTicks('y')).grid(column=5, row=1)

        # Set X tick size
        ttk.Label(setTicksFrame, text='X-axis').grid(column=6, row=0, columnspan=2)
        ttk.Button(setTicksFrame, text='+', width=3 ,command=lambda: self.incTicks('x')).grid(column=6, row=1)
        ttk.Button(setTicksFrame, text='-', width=3, command=lambda: self.decTicks('x')).grid(column=7, row=1)

        # Hide legend button
        ttk.Button(self.toolbarWrapper, text='Toggle\nlegend', command=lambda: self.hideLegend()).grid(column=8, row=0, padx=(5,5))

    def createRightSide(self):
        self.indicator = ttk.Label(self, text='', anchor='center')
        self.indicator.pack(side=LEFT, fill=Y)

        # Create loads notebook frame and loadnotebook
        self.loadNotebookFrame = ttk.Frame(self, style='loadNoteBookFrame.TFrame', borderwidth=10)
        self.loadNotebookFrame.pack(side=RIGHT, fill=Y)

        self.loadNotebookFrame.bind('<Motion>', self.changeCursor)
        self.loadNotebookFrame.bind('<1>', self.setPosX)
        self.loadNotebookFrame.bind('<B1-Motion>', self.resize)
        self.loadNotebookFrame.bind('<ButtonRelease-1>', self.finishResize)
        self.indicator.bind('<Double-Button-1>', self.defSize)

        self.loadNotebook = ScrollableNotebook(self.loadNotebookFrame, wheelscroll=True)
        self.loadNotebook.pack(expand=TRUE, fill=BOTH)

        self.separator = ttk.Separator(self, style='asd.TSeparator')

        # Create tabs for loads
        for i, details in enumerate(self.workLoadDetailsObjects):
            loadTabObject = PlotLoadTab(self, i, self.activeTestId, details, self.loadNotebook, self.plot)
            self.loadNotebook.add(loadTabObject, text=details.name)
            self.loadTabs.append(loadTabObject)

    def setPlotTitle(self):
        self.ax.set_title(self.titleEntry.get())
        self.canvas.draw()

    def changeCursor(self, e):
        if self.loadNotebookFrame.identify(e.x, e.y) == 'border':
            self.loadNotebookFrame.configure(cursor='sb_h_double_arrow')
        else:
            self.loadNotebookFrame.configure(cursor='arrow')
    
    def numfmt(self, x, pos=None):
            vo2unit = self.workLoadDetailsObjects[0].VO2_unit
            if vo2unit == 'l/min':
                s = '{0:.1f}'.format(x / 1000.0)
            elif vo2unit == 'ml/min':
                s = '{0:.0f}'.format(x)
            return s

    def hideLegend(self):
        legend = self.plot[1].get_legend()
        legSize = self.leg._legend_box.get_window_extent(self.fig.canvas.get_renderer())

        vis = legend.get_visible()
        if vis:
            legend.set_visible(False)
        else:
            legend.set_visible(True)
        self.plot[0].canvas.draw()

    def incTicks(self, axis):
        if axis == 'y':
            yticks = self.plot[1].get_yticks()
            n = len(yticks) + 1
            self.plot[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
            self.plot[0].canvas.draw()
        else:
            xticks = self.plot[1].get_xticks()
            n = len(xticks) + 1
            self.plot[1].xaxis.set_major_locator(plt.LinearLocator(numticks=n))
            self.plot[0].canvas.draw()

    def decTicks(self, axis):
        if axis == 'y':
            yticks = self.plot[1].get_yticks()
            n = len(yticks) - 1
            self.plot[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
            self.plot[0].canvas.draw()
        else:
            xticks = self.plot[1].get_xticks()
            n = len(xticks) - 1
            self.plot[1].xaxis.set_major_locator(plt.LinearLocator(numticks=n))
            self.plot[0].canvas.draw()

    def finishResize(self, event):
        if event.x != self.posX:
            width = self.loadNotebookFrame.winfo_width() - event.x
            self.separator.place_forget()

            if width > 10:
                self.loadNotebookFrame.configure(width=width)
                self.loadNotebookFrame.update_idletasks()
                minWidth = self.loadNotebook.winfo_reqwidth()
                width = self.loadNotebookFrame.winfo_width()

                if width < minWidth:
                    self.indicator.configure(text='\u2B9C', foreground='white', background='#4eb1ff')
                else:
                    self.indicator.configure(text='', background=app.root.cget('bg'))
            else:
                self.loadNotebookFrame.configure(width=10)
                self.indicator.configure(text='\u2B9C', foreground='white', background='#4eb1ff')

    def resize(self, event):
        self.loadNotebookFrame.pack_propagate(False)
        self.separator.place(height=self.loadNotebookFrame.winfo_height(), x=self.canvasFrame.winfo_width()+event.x, y=0)
        self.separator.lift()
    
    def setPosX(self, e):
        self.posX = e.x

    def defSize(self, event):
        self.indicator.configure(text='', background=app.root.cget('bg'))
        self.loadNotebookFrame.pack_propagate(True)
    
    def setYLim(self):
        vo2unit = self.workLoadDetailsObjects[0].VO2_unit
        if vo2unit == 'ml/min':
            limit = float(self.yValue.get())
        elif vo2unit == 'l/min':
            limit = float(self.yValue.get()) * 1000

        self.plot[1].set_ylim(top=float(limit))
        self.plot[0].canvas.draw()

    def createPlot(self):
        PvO2 = np.arange(0,100,1)
        self.plot = plt.subplots(constrained_layout=True)
        self.fig, self.ax = self.plot

        self.ax.set_title('O\u2082 Pathway')
        self.ax.set_xlabel('PvO\u2082 (mmHg)')
        self.ax.set_xlim(left=0, right=100)
        self.handles = []
        ylim = []

        for i, w in enumerate(self.workLoadDetailsObjects):
            coords = w.getCoords()
            y = coords['y']
            y2 = coords['y2']
            xi = coords['xi']
            yi = coords['yi']

            ylim.append(y2[0])

            line, = self.ax.plot(PvO2, y, lw=2, color=f'C{i}', label=w.name)
            curve, = self.ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=w.name)
            dot, = self.ax.plot(xi, yi, 'o', color='red', label=w.name)

            line.set_picker(5)
            curve.set_picker(5)
            dot.set_picker(5)

            self.handles.insert(i, line)

        if max(ylim) > 50: # ml/min
            ylim = 1000 * math.ceil( max(ylim) / 1000 )
        else: # l/min
            ylim = 1 * math.ceil( max(ylim) / 1 ) + 1

        self.ax.set_ylim(top=ylim, bottom=0)

        self.leg = self.ax.legend(handles=self.handles , loc='upper left', bbox_to_anchor=(1.01, 1),
            fancybox=True, shadow=True, ncol=1)

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
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.plotFrame)
        self.canvasTk = self.canvas.get_tk_widget() # Tkinter canvas
        self.canvasTk.pack(fill=BOTH, expand=1)
        self.canvasTk.pack_propagate(False)
        self.canvas.draw()

    def onpick(self, event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        origline = []
        legline = event.artist
        index = None
        # Detect click on legend or plot itself
        try:
            origline = self.lined[legline]
        except:
            for l in plt.gca().get_legend_handles_labels()[0]:
                for i, (key, value) in enumerate(self.lined.items()):
                    if legline in value:
                        index = i
                        origline.append(value)
            origline = origline[0]

        for line in origline:
            vis = not line.get_visible()
            line.set_visible(vis)

            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled
            if vis:
                legline.set_alpha(1.0)
                if index != None:
                    self.leg.get_lines()[index].set_alpha(1.0)
            else:
                legline.set_alpha(0.2)
                if index != None:
                    self.leg.get_lines()[index].set_alpha(0.2)
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

class PlotLoadTab(ttk.Frame):
    def __init__(self, plotTab, index, testId, workLoadDetails, parentNotebook, plot, *args, **kwargs):
        ttk.Frame.__init__(self, plotTab, *args, **kwargs)
        self.configure(cursor='arrow')

        self.upperPart = ttk.Frame(self)
        self.upperPart.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.upperPart)
        self.scrollbar = ttk.Scrollbar(self.upperPart, orient=VERTICAL, command=self.canvas.yview)
        self.contentWrapper = ttk.Frame(self.canvas)
        self.contentWrapper.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.contentWrapper, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.parentObject = plotTab
        self.index = index
        self.testId = testId
        self.detailsObject = workLoadDetails # Workdetail object
        self.details = workLoadDetails.getWorkLoadDetails() # Workload details dict
        self.envDetailsObject = self.parentObject.activeTest.workLoads[self.index].envDetails
        self.envDetails = self.parentObject.activeTest.workLoads[self.index].envDetails.getDetails()
        self.parentNotebook = parentNotebook
        self.plot = plot
        self.rowElements = []

        ##
        ## Details frame
        ##

        ttk.Label(self.contentWrapper, text='Value').grid(column=1, row=0)
        ttk.Label(self.contentWrapper, text='Unit').grid(column=2, row=0)
        ttk.Label(self.contentWrapper, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.contentWrapper, text='Calc.').grid(column=4, row=0)
        
        if app.settings.getTestDef()['loadMode'] == 0:
            ttk.Label(self.contentWrapper, text='Load').grid(column=0, row=1)
            ttk.Label(self.contentWrapper, text=self.details["Load"]).grid(column=1, row=1)
            ttk.Label(self.contentWrapper, text=self.details["Load_unit"]).grid(column=2, row=1)
        else:
            ttk.Label(self.contentWrapper, text='Velocity').grid(column=0, row=1)
            ttk.Label(self.contentWrapper, text=self.details["Velocity"]).grid(column=1, row=1)
            ttk.Label(self.contentWrapper, text=self.details["Velocity_unit"]).grid(column=2, row=1)

            ttk.Label(self.contentWrapper, text='Incline').grid(column=0, row=2)
            ttk.Label(self.contentWrapper, text=self.details["Incline"]).grid(column=1, row=2)
            ttk.Label(self.contentWrapper, text=self.details["Incline_unit"]).grid(column=2, row=2)

        # VO2
        vo2Value = float(self.details['VO2'])
        self.vo2Row = LoadTabRow(self, self.contentWrapper, 'VO2', vo2Value, 3, self.index, self.detailsObject)
        self.rowElements.append(self.vo2Row)

        # Q
        qValue = float(self.details['Q'])
        self.qRow = LoadTabRow(self, self.contentWrapper, 'Q', qValue, 4, self.index, self.detailsObject)
        self.rowElements.append(self.qRow)

        # Hb
        hbValue = float(self.details['[Hb]'])
        self.hbRow = LoadTabRow(self, self.contentWrapper, '[Hb]', hbValue, 5, self.index, self.detailsObject)
        self.rowElements.append(self.hbRow)

        # SaO2
        sao2Value = float(self.details['SaO2'])
        self.sao2Row = LoadTabRow(self, self.contentWrapper, 'SaO2', sao2Value, 6, self.index, self.detailsObject)
        self.rowElements.append(self.sao2Row)

        # SvO2
        svo2Value = float(self.details['SvO2'])
        self.svo2Row = LoadTabRow(self, self.contentWrapper, 'SvO2', svo2Value, 7, self.index, self.detailsObject)
        self.rowElements.append(self.svo2Row)

        # CaO2
        cao2Value = float(self.details['CaO2'])
        self.cao2Row = LoadTabRow(self, self.contentWrapper, 'CaO2', cao2Value, 8, self.index, self.detailsObject)
        self.rowElements.append(self.cao2Row)

        # CvO2
        cvo2Value = float(self.details['CvO2'])
        self.cvo2Row = LoadTabRow(self, self.contentWrapper, 'CvO2', cvo2Value, 9, self.index, self.detailsObject)
        self.rowElements.append(self.cvo2Row)
        
        # CavO2
        cavo2Value = float(self.details['C(a-v)O2'])
        self.cavo2Row = LoadTabRow(self, self.contentWrapper, 'C(a-v)O2', cavo2Value, 10, self.index, self.detailsObject)
        self.rowElements.append(self.cavo2Row)

        # PvO2
        pvo2Value = self.details['PvO2']
        self.pvo2Row = LoadTabRow(self, self.contentWrapper, 'PvO2', pvo2Value, 11, self.index, self.detailsObject)
        self.rowElements.append(self.pvo2Row)

        # QaO2
        qao2Value = float(self.details['QaO2'])
        self.qao2Row = LoadTabRow(self, self.contentWrapper, 'QaO2', qao2Value, 12, self.index, self.detailsObject)
        self.rowElements.append(self.qao2Row)

        # DO2
        do2Value = self.details['DO2']
        self.do2Row = LoadTabRow(self, self.contentWrapper, 'DO2', do2Value, 13, self.index, self.detailsObject)
        self.rowElements.append(self.do2Row)

        # T
        tValue = float(self.details['T'])
        if self.details['T_unit'] == 'F':
            tValue = (tValue - 32) / 1.8
        elif self.details['T_unit'] == 'K':
            tValue = tValue - 273.15
        else:
            self.tRow = LoadTabRow(self, self.contentWrapper, 'T', tValue, 14, self.index, self.detailsObject)
        self.rowElements.append(self.tRow)

        # pH
        phValue = self.details['pH']
        self.phRow = LoadTabRow(self, self.contentWrapper, 'pH', phValue, 15, self.index, self.detailsObject)
        self.rowElements.append(self.phRow)

        # Add environmental details
        self.elevationRow = LoadTabRow(self, self.contentWrapper, 'Elevation', self.envDetails['Elevation'], 16, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.elevationRow)
        self.ATMRow = LoadTabRow(self, self.contentWrapper, 'ATM', self.envDetails['ATM'], 17, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.ATMRow)
        self.FiO2Row = LoadTabRow(self, self.contentWrapper, 'FiO2', self.envDetails['FiO2'], 18, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.FiO2Row)
        self.TemperatureRow = LoadTabRow(self, self.contentWrapper, 'Temperature', self.envDetails['Temperature'], 19, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.TemperatureRow)
        self.RhRow = LoadTabRow(self, self.contentWrapper, 'Rh', self.envDetails['Rh'], 20, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.RhRow)

        ##
        ## Options frame
        ##

        # Plot options
        self.lowerPart = ttk.Frame(self)
        self.lowerPart.pack(side=BOTTOM)
        
        # Plot options
        PlotOptions(self.lowerPart, self.plot, self.index)

    def updateDetails(self):
        self.details = self.workLoad.getWorkLoadDetails()
        for r in self.rowElements:
            r.updateText(self.details)

class PlotOptions(object):
    def __init__(self, parent, plotObject, loadIndex):
        self.plotObject = plotObject
        self.loadIndex = loadIndex

        self.plotOptions = ttk.Labelframe(parent, text='Line options')
        self.plotOptions.grid()

        # Set line shape
        ttk.Label(self.plotOptions, text='Change line type').grid(column=0, row=0)
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

        self.lineTypeMenuButton.grid(column=1, row=0)

        # Set line color
        ttk.Label(self.plotOptions, text='Change line color').grid(column=0, row=1)
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
        self.lineColorMenuButton.grid(column=1, row=1)

        self.plotOptions.grid_columnconfigure(2, minsize=20 )

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

class LoadTabRow(ttk.Frame):
    def __init__(self, parentObject, parentFrame, label, value, row, index, detailsObject=None, envDetailsObject=None, *args, **kwargs):
        ttk.Frame.__init__(self, parentFrame, *args, **kwargs)
        self.parentObject = parentObject
        self.parent = parentFrame
        self.label = label
        self.value = value
        self.row = row
        self.index = index
        self.detailsObject = detailsObject
        if detailsObject:
            self.details = detailsObject.getWorkLoadDetails()
            self.mode = 0
        else:
            self.envDetailsObject = envDetailsObject
            self.envDetails = envDetailsObject.getDetails()
            self.mode = 1

        # Adjust the number of decimal according to the used unit
        self.var = DoubleVar(self.parent, value=f'{"{0:.1f}".format(float(self.value))}')

        # Label
        if '2' in self.label:
            label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(self.parent, text=label_subscripted).grid(column=0, row=row)
        else:
            ttk.Label(self.parent, text=self.label).grid(column=0, row=row)

        # Entry
        self.entry = ttk.Label(self.parent, textvariable=self.var, width=7, anchor='center')
        self.entry.grid(column=1, row=row)


        if self.label != 'pH':
            units = app.settings.getUnits()[f'{self.label}_units']
            if len(units) != 1:
                # Unit entry
                if self.label != 'pH\u209A\u2091\u2090\u2096':
                    self.menuButton = ttk.Menubutton(self.parent)
                    if self.mode == 0:
                        self.menuButton.config(text=self.details[f'{self.label}_unit'])
                    else:
                        self.menuButton.config(text=self.envDetails[f'{self.label}_unit'])
                    tempMenu = Menu(self.menuButton, tearoff=False)

                    for i, u in enumerate(units):
                        LoadMenuElem(self, tempMenu, self.menuButton, self.var, u, i, units, f'{self.label}', self.mode)
                    
                    self.menuButton['menu']=tempMenu
                    self.menuButton.grid(column=2, row=row)
            else:
                ttk.Label(self.parent, text=units[0]).grid(column=2, row=row)
        
        if self.mode == 0:
            # M/C Radiobuttons
            self.mcVar = IntVar(value=self.details[f'{self.label}_MC'])

            self.radio1 = ttk.Radiobutton(self.parent, value=0, variable=self.mcVar)
            self.radio1.grid(column=3, row=row)

            self.radio2 = ttk.Radiobutton(self.parent, value=1, variable=self.mcVar)
            self.radio2.grid(column=4, row=row)
            self.mcVar.trace('w', self.updateMc)

    def updateMc(self, name, index, mode):
        self.detailsObject.setMC(f'{self.label}_MC', self.mcVar.get())

    def updateEntryAndScale(self, unit, prevUnit):
        if self.mode == 0:
            value = float(self.details[self.label])
        else:
            value = float(self.envDetailsObject.getDetails()[self.label])
        
        if unit != prevUnit:
            if unit == 'ml/min': # l/min -> ml/min
                self.detailsObject.setValue(self.label, self.var.get()*1000)
                self.var.set(self.var.get()*1000)
            
            elif unit == 'l/min': # ml/min -> l/min
                self.detailsObject.setValue(self.label, self.var.get()/1000)
                self.var.set(self.var.get()/1000)

            elif unit == 'g/l': # g/dl -> g/l
                self.detailsObject.setValue(self.label, self.var.get()*10)
                self.var.set(self.var.get()*10)

            elif unit == 'g/dl': # g/l -> g/dl
                self.detailsObject.setValue(self.label, self.var.get()/10)
                self.var.set(self.var.get()/10)

            elif unit == 'ml/l': # ml/dl -> ml/l
                self.detailsObject.setValue(self.label, self.var.get()*10)
                self.var.set(self.var.get()*10)

            elif unit == 'ml/dl': # ml/l -> ml/dl
                self.detailsObject.setValue(self.label, self.var.get()/10)
                self.var.set(self.var.get()/10)
            
            elif unit == 'l': #ml -> l
                self.detailsObject.setValue(self.label, self.var.get()/1000)
                self.var.set(self.var.get()/1000)

            elif unit == 'ml': #l -> ml
                self.detailsObject.setValue(self.label, self.var.get()*1000)
                self.var.set(self.var.get()*1000)

            elif unit == 'F' or unit == 'K' or unit == '\N{DEGREE SIGN}C':
                if prevUnit == 'F':
                    if unit == 'K': #F -> K
                        self.detailsObject.setValue(self.label, 5/9 * (value + 459.67)) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, 5/9 * (value + 459.67))
                        self.var.set( f'{"{0:.0f}".format( float(( 5/9 * (value + 459.67) )) ) }' )
                    elif unit == '\N{DEGREE SIGN}C': #F -> C
                        self.detailsObject.setValue(self.label, (value - 32) / 1.8) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, (value - 32) / 1.8)
                        self.var.set( f'{"{0:.1f}".format( float(( (value - 32) / 1.8)) ) }' )

                elif prevUnit == 'K':
                    if unit == 'F': #K -> F
                        self.detailsObject.setValue(self.label, 1.8 * (value - 273) + 32) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, 1.8 * (value - 273) + 32)
                        self.var.set( f'{"{0:.1f}".format( float(( 1.8 * (value - 273) + 32 )) ) }' )
                    elif unit == '\N{DEGREE SIGN}C': #K -> C
                        self.detailsObject.setValue(self.label, value - 273.15) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, value - 273.15)
                        self.var.set( f'{"{0:.1f}".format( float(( value - 273.15)) ) }' )
                
                elif prevUnit == '\N{DEGREE SIGN}C':
                    if unit == 'K': #C -> K
                        self.detailsObject.setValue(self.label, value + 273.15) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, value + 273.15)
                        self.var.set( f'{"{0:.1f}".format( float(( value + 273.15)) ) }' )
                    elif unit == 'F': #C -> F
                        self.detailsObject.setValue(self.label, value * 1.8 + 32) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, value * 1.8 + 32)
                        self.var.set( f'{"{0:.1f}".format( float(( value * 1.8 + 32)) ) }' )

            elif unit == 'm' or unit == 'km' or unit == 'ft':
                if prevUnit == 'm':
                    if unit == 'km': #m -> km
                        self.envDetailsObject.setDetail(self.label, float(value / 1000))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.1f}".format( float(( value / 1000 )) )}' )
                    elif unit == 'ft': #m -> ft
                        self.envDetailsObject.setDetail(self.label, float(value * 3.2808399))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.0f}".format( float(( value * 3.2808399 )) )}' )
                elif prevUnit == 'km':
                    if unit == 'm': #km -> m
                        self.envDetailsObject.setDetail(self.label, float(value * 1000))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.0f}".format( float(( value * 1000 )) )}' )
                    elif unit == 'ft': #km -> ft
                        self.envDetailsObject.setDetail(self.label, float(value * 3280.8399))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.0f}".format( float(( value * 3280.8399 )) )}' )
                elif prevUnit == 'ft':
                    if unit == 'm': #ft -> m
                        self.envDetailsObject.setDetail(self.label, float(value * 0.3048))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.3048 )) )}' )
                    elif unit == 'km': #ft -> km
                        self.envDetailsObject.setDetail(self.label, float(value * 0.0003048))
                        self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                        self.var.set( f'{"{0:.1f}".format( float(( value * 0.0003048 )) )}' )

            elif unit == 'kPa' or unit == 'bar' or unit == 'psi' or unit == 'mmHg':
                if prevUnit == 'kPa':
                    if unit == 'bar': #kPa -> bar
                        self.envDetailsObject.setDetail(self.label, float( value * 0.01 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.01 )) )}' )
                    elif unit == 'psi': #kPa -> psi
                        self.envDetailsObject.setDetail(self.label, float( value * 0.145037738 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.145037738 )) )}' )
                    elif unit == 'mmHg': #kPa -> mmHg
                        self.envDetailsObject.setDetail(self.label, float( value * 7.50061683 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 7.50061683 )) )}' )
                elif prevUnit == 'bar':
                    if unit == 'kPa': #bar -> kPa
                        self.envDetailsObject.setDetail(self.label, float( value * 100 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 100 )) )}' )
                    elif unit == 'psi': #bar -> psi
                        self.envDetailsObject.setDetail(self.label, float( value * 14.5037738 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 14.5037738 )) )}' )
                    elif unit == 'mmHg': #bar -> mmHg
                        self.envDetailsObject.setDetail(self.label, float( value * 750.061683 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 750.061683 )) )}' )
                elif prevUnit == 'psi':
                    if unit == 'kPa': #psi -> kPa
                        self.envDetailsObject.setDetail(self.label, float( value * 6.89475729 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 6.89475729 )) )}' )
                    elif unit == 'bar': #psi -> bar
                        self.envDetailsObject.setDetail(self.label, float( value * 0.0689475729 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.0689475729 )) )}' )
                    elif unit == 'mmHg': #psi -> mmHg
                        self.envDetailsObject.setDetail(self.label, float( value * 51.7149326 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 51.7149326 )) )}' )
                elif prevUnit == 'mmHg':
                    if unit == 'kPa': #mmHg -> kPa
                        self.envDetailsObject.setDetail(self.label, float( value * 0.133322368 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.133322368 )) )}' )
                    elif unit == 'bar': #mmHg -> bar
                        self.envDetailsObject.setDetail(self.label, float( value * 0.00133322368 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.00133322368 )) )}' )
                    elif unit == 'psi': #mmHg -> psi
                        self.envDetailsObject.setDetail(self.label, float( value * 0.0193367747 ))
                        self.var.set( f'{"{0:.0f}".format( float(( value * 0.0193367747 )) )}' )

    def getValue(self):
        return self.var.get()
    
    def updateText(self, details):
        self.entry.configure(text=f'{"{0:.1f}".format(float(details[self.label]))}')

class LoadMenuElem(object):
    def __init__(self, parentObject, menu, menuButton, var, label, index, unitElems, name, mode):
        self.parentObject = parentObject
        self.menu = menu
        self.menuButton = menuButton
        self.var = var
        self.mode = mode # 0: test details / 1: env details
        self.label = label
        self.index = index
        self.unitElems = unitElems
        self.name = name

        self.menu.add_command(label=f'{self.label}', command=lambda: self.updateValue())

    def updateValue(self):
        prevUnit = self.menuButton.cget("text")
        unit = self.unitElems[self.index]
        self.menuButton.config(text=unit)
        
        if self.mode == 0:
            # update unit change to every loadtab workload details
            plotTabWorkloads = self.parentObject.parentObject.parentObject.workLoadDetailsObjects
            for l in plotTabWorkloads:
                l.setUnit(f'{self.name}_unit', unit)
                self.parentObject.updateText(l.getWorkLoadDetails())

            # update unit change to every loadtab
            for tab in self.parentObject.parentObject.parentObject.loadTabs:
                for elem in tab.rowElements:
                    if elem.label == self.name:
                        elem.updateEntryAndScale(unit, prevUnit)
                        elem.menuButton.config(text=unit)
            if unit != prevUnit:
                if self.name == 'VO2':
                    plotIndex = app.getPlottingPanel().plotNotebook.index('current')

                    # Update figure
                    yValueVar = app.getPlottingPanel().plots[plotIndex].yValue
                    yValue = float(yValueVar.get())

                    if unit == 'l/min':
                        plt.gca().yaxis.set_label_text('VO\u2082 (l/min)')
                        yValueVar.set(yValue/1000)
                    elif unit == 'ml/min':
                        plt.gca().yaxis.set_label_text('VO\u2082 (ml/min)')
                        yValueVar.set(yValue*1000)

                    figure = app.getPlottingPanel().plots[plotIndex].plot[0]
                    figure.canvas.draw()







        else:
            # update unit change to every loadtab env details
            workLoads = self.parentObject.parentObject.parentObject.activeTest.workLoads
            for l in workLoads:
                l.envDetails.setDetail(f'{self.name}_unit', unit)
                self.parentObject.updateText(l.envDetails.getDetails())
            
            # update unit change to every loadtab
            for tab in self.parentObject.parentObject.parentObject.loadTabs:
                for elem in tab.rowElements:
                    if elem.label == self.name:
                        elem.updateEntryAndScale(unit, prevUnit)
                        elem.menuButton.config(text=unit)
                        break