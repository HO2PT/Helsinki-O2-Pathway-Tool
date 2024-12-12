from tkinter import *
from tkinter import ttk
import math
import numpy as np
import copy
import matplotlib
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
            
            # Prevent mac version from segmentation faulting
            self.update_idletasks()

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
        self.parentFrame = parentFrame

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
        self.wrap = ttk.Frame(self.instructions)
        self.wrap.grid()

        ttk.Label(self.wrap, text='Left click - show/hide').grid(column=0, row=0, sticky=NSEW)
        self.wrap.grid_columnconfigure(1, weight=1, minsize=15)
        ttk.Label(self.wrap, text='Middle click - show all').grid(column=2, row=0, sticky=NSEW)
        self.wrap.grid_columnconfigure(3, weight=1, minsize=15)
        ttk.Label(self.wrap, text='Right click - hide all').grid(column=4, row=0, sticky=NSEW)

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
            plt.gca().yaxis.set_label_text(r'VO$_2$ (L/min)')
            yLimit = self.plot[1].get_ylim()[1] / 1000
        elif vo2unit == 'ml/min':
            plt.gca().yaxis.set_label_text(r'VO$_2$ (ml/min)')
            yLimit = self.plot[1].get_ylim()[1]

        # Custom figure tools container
        self.toolbarContainer = ttk.Frame(self.canvasFrame)
        self.toolbarContainer.pack(side=BOTTOM, fill=BOTH)

        # Figure toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarContainer, pack_toolbar=False)
        if app.platform == 'linux':
            self.toolbar.configure(bg='#EFEBE7')
            self.toolbar._message_label.config(background='#EFEBE7')
            for c in self.toolbar.winfo_children():
                c.config(background='#EFEBE7')
        elif app.platform == 'darwin':
            self.toolbar.configure(bg='#F5F6F7')
            self.toolbar._message_label.config(background='#F5F6F7', foreground='black')
            for c in self.toolbar.winfo_children():
                c.config(background='#F5F6F7', highlightbackground='#F5F6F7')
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

        # self.toolbarWrapper.grid_columnconfigure(2, minsize=25)

        # Set plot title
        setTitleFrame = ttk.Labelframe(self.toolbarWrapper, text='Set plot title', padding=(5,5))
        setTitleFrame.grid(column=1, row=0, sticky='w', padx=(5,5))
        self.titleEntry = ttk.Entry(setTitleFrame)
        self.titleEntry.grid(column=0, row=1)
        setTitleButton = ttk.Button(setTitleFrame, text='Set', command=self.setPlotTitle)
        setTitleButton.grid(column=1, row=1)

        # Set tick size
        self.setTicksFrame = ttk.Labelframe(self.toolbarWrapper, text='Set axis ticks', padding=(5,5))
        self.setTicksFrame.grid(column=2, row=0, padx=(5,5))

        ss = ttk.Style()
        ss.configure('ss.TButton', anchor='center')

        # Set Y tick size
        ttk.Label(self.setTicksFrame, text='Y-axis').grid(column=0, row=0, columnspan=2)
        ttk.Button(self.setTicksFrame, style='ss.TButton', text='+', width=3, command=lambda: self.incTicks('y')).grid(column=0, row=1)
        ttk.Button(self.setTicksFrame, style='ss.TButton', text='-', width=3, command=lambda: self.decTicks('y')).grid(column=1, row=1)

        # Set X tick size
        ttk.Label(self.setTicksFrame, text='X-axis').grid(column=2, row=0, columnspan=2)
        ttk.Button(self.setTicksFrame, style='ss.TButton', text='+', width=3 ,command=lambda: self.incTicks('x')).grid(column=2, row=1)
        ttk.Button(self.setTicksFrame, style='ss.TButton', text='-', width=3, command=lambda: self.decTicks('x')).grid(column=3, row=1)

        # Hide legend button
        self.hideLegendBtn = ttk.Button(self.toolbarWrapper, text='Toggle\nlegend', command=lambda: self.hideLegend())
        self.hideLegendBtn.grid(column=3, row=0, padx=(5,5))

        self.toolbarWrapper.update_idletasks()
        self.toolbarReqWidth = self.toolbarWrapper.winfo_reqwidth()

    def createRightSide(self):
        self.indicator = ttk.Label(self, text='', anchor='center')
        self.indicator.pack(side=LEFT, fill=Y)

        # Create loads notebook frame and loadnotebook
        self.loadNotebookFrame = ttk.Frame(self, style='loadNoteBookFrame.TFrame', borderwidth=5)
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
            if e.y > 25:
                self.loadNotebookFrame.configure(cursor='sb_h_double_arrow')
        else:
            self.loadNotebookFrame.configure(cursor='arrow')
            self.loadNotebook.configure(cursor='arrow')
    
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
        width = self.loadNotebookFrame.winfo_width() - event.x
        p = self.parentFrame.winfo_width()

        # Reorganize toolbar buttons if necessary
        if (p-width) < self.toolbarReqWidth:
            self.setTicksFrame.grid(column=1, row=1, padx=(5,5))
            self.hideLegendBtn.grid(column=0, row=1, padx=(5,5))
        else:
            self.setTicksFrame.grid(column=2, row=0, padx=(5,5))
            self.hideLegendBtn.grid(column=3, row=0, padx=(5,5))

        if event.x != self.posX:
            self.separator.place_forget()

            if width > 10:
                self.loadNotebookFrame.configure(width=width)
                self.loadNotebookFrame.update_idletasks()
                minWidth = self.loadNotebook.winfo_reqwidth()
                width = self.loadNotebookFrame.winfo_width()

                if width < minWidth:
                    if app.platform == 'darwin':
                        self.indicator.configure(text='<', foreground='white', background='#4eb1ff')
                    else: 
                        self.indicator.configure(text='\u2B9C', foreground='white', background='#4eb1ff')
                else:
                    self.indicator.configure(text='', background=app.root.cget('bg'))
            else:
                self.loadNotebookFrame.configure(width=10)
                if app.platform == 'darwin':
                    self.indicator.configure(text='<', foreground='white', background='#4eb1ff')
                else:
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
        PvO2 = np.arange(0.0,100.01,0.1)
        self.plot = plt.subplots(constrained_layout=True)
        self.fig, self.ax = self.plot

        # Prevent macOS from changing app icon
        if app.platform == 'darwin':
            app.root.tk.call('wm', 'iconphoto', app.root._w, PhotoImage(file=f'{app.path}/Img/ho2pt.png'))

        matplotlib.rcParams['font.sans-serif'] = "Arial"
        matplotlib.rcParams['font.family'] = "sans-serif"

        self.ax.set_title(r'O$_2$ Pathway')
        self.ax.set_xlabel(r'PvO$_2$ (mmHg)')
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

            if 'Q1' == w.name or 'Q3' == w.name or '-1 SD' == w.name or '+1 SD' == w.name or '2.5%' == w.name or '97.5%' == w.name: 
                line, = self.ax.plot(PvO2, y, '--', scalex=True, lw=2, color='C7', visible=False, label=w.name)
                curve, = self.ax.plot(PvO2, y2, '--', scalex=True, lw=2, color='C7', visible=False, label=w.name)
                dot, = self.ax.plot(-1, -1, 'o', scalex=True, color='red', visible=False, label=w.name)
            else:
                line, = self.ax.plot(PvO2, y, scalex=True, lw=2, color=f'C{i}', label=w.name)
                curve, = self.ax.plot(PvO2, y2, scalex=True, lw=2, color=f'C{i}', label=w.name)
                dot, = self.ax.plot(xi, yi, 'o', scalex=True, color='red', label=w.name)

                line.set_picker(5)
                curve.set_picker(5)
                dot.set_picker(5)
                # line.set_pickradius(5)
                # curve.set_pickradius(5)
                # dot.set_pickradius(5)

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
            # legline.set_pickradius(5)

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

        linelist = self.removeHidden(plt.gca().get_legend_handles_labels())
        visibleLegendLines = list(dict.fromkeys(linelist[1]))

        try: # Legend
            origline = linelist[0][legline]
        except: # Plot
            index = []
            for i, value in enumerate(linelist[0]):
                if legline._label == value._label:
                    index = visibleLegendLines.index(value._label)
                    origline.append(value)
            
        for line in origline:
            if 'Q1' == line._label or 'Q3' == line._label or '-1 SD' == line._label or '+1 SD' == line._label or '2.5%' == line._label or '97.5%' == line._label:
                pass
            else:
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

    def removeHidden(self, lines):
        filteredLines = [[],[]]
        idxs = []

        # Collect indexes to remove
        for idx, i in enumerate(lines[1]):
            if 'Q1' == i or 'Q3' == i or '-1 SD' == i or '+1 SD' == i or '2.5%' == i or '97.5%' == i:
                pass
            else:
                idxs.append(idx)

        for i in idxs:
            filteredLines[0].append(lines[0][i])
            filteredLines[1].append(lines[1][i])

        return filteredLines

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
            if 'Q1' == line._label or 'Q3' == line._label or '-1 SD' == line._label or '+1 SD' == line._label or '2.5%' == line._label or '97.5%' == line._label:
                pass
            else:
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
        self.upperPart.pack(fill=Y, expand=True, anchor='nw')

        if app.platform == 'darwin':
            self.canvas = Canvas(self.upperPart, highlightbackground='#F5F6F7')
        else:
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

        # k
        do2Value = self.details['k']
        self.kRow = LoadTabRow(self, self.contentWrapper, 'k', do2Value, 14, self.index, self.detailsObject)
        self.rowElements.append(self.kRow)

        # T0
        tValue = float(self.details['T @ rest'])
        if self.details['T_unit'] == 'F':
            tValue = (tValue - 32) / 1.8
        elif self.details['T_unit'] == 'K':
            tValue = tValue - 273.15
        else:
            self.tRestRow = LoadTabRow(self, self.contentWrapper, 'T @ rest', tValue, 15, self.index, self.detailsObject)
        self.rowElements.append(self.tRestRow)

        # T
        tValue = float(self.details['T'])
        if self.details['T_unit'] == 'F':
            tValue = (tValue - 32) / 1.8
        elif self.details['T_unit'] == 'K':
            tValue = tValue - 273.15
        else:
            self.tRow = LoadTabRow(self, self.contentWrapper, 'T', tValue, 16, self.index, self.detailsObject)
        self.rowElements.append(self.tRow)

        # pH0
        phValue = self.details['pH @ rest']
        self.phRestRow = LoadTabRow(self, self.contentWrapper, 'pH @ rest', phValue, 17, self.index, self.detailsObject)
        self.rowElements.append(self.phRestRow)

        # pH
        phValue = self.details['pH']
        self.phRow = LoadTabRow(self, self.contentWrapper, 'pH', phValue, 18, self.index, self.detailsObject)
        self.rowElements.append(self.phRow)

        # Add environmental details
        self.elevationRow = LoadTabRow(self, self.contentWrapper, 'Elevation', self.envDetails['Elevation'], 19, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.elevationRow)
        self.ATMRow = LoadTabRow(self, self.contentWrapper, 'ATM', self.envDetails['ATM'], 20, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.ATMRow)
        self.FIO2Row = LoadTabRow(self, self.contentWrapper, 'FIO2', self.envDetails['FIO2'], 21, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.FIO2Row)
        self.TemperatureRow = LoadTabRow(self, self.contentWrapper, 'Temperature', self.envDetails['Temperature'], 22, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.TemperatureRow)
        self.RhRow = LoadTabRow(self, self.contentWrapper, 'Rh', self.envDetails['Rh'], 23, self.index, envDetailsObject=self.envDetailsObject)
        self.rowElements.append(self.RhRow)

        ##
        ## Options frame
        ##

        # Plot options
        self.lowerPart = ttk.Frame(self)
        self.lowerPart.pack(side=BOTTOM, anchor='nw', pady=5)
        
        # Plot options
        plotopt = PlotOptions(self.lowerPart, self.plot, self.index)

        # Config canvas width
        self.update_idletasks()
        self.canvas.config(width=self.contentWrapper.winfo_reqwidth())
        self.lowerPart.pack_configure(padx=[plotopt.plotOptions.winfo_width()/4, 0])

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
        if app.platform == 'linux':
            lineTypeMenu = Menu(self.lineTypeMenuButton, tearoff=False, background='#EFEBE7')
        elif app.platform == 'darwin':
            lineTypeMenu = Menu(self.lineTypeMenuButton, tearoff=False, background='#F5F6F7')
        else:
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

        if app.platform == 'linux':
            lineColorMenu = Menu(self.lineColorMenuButton, tearoff=False, background='#EFEBE7')
        elif app.platform == 'darwin':
            lineColorMenu = Menu(self.lineColorMenuButton, tearoff=False, background='#F5F6F7')
        else:
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
        if len(self.plotObject[1].get_legend().get_lines()) > 1:
            legend = self.plotObject[1].get_legend().get_lines()[self.loadIndex]
            legend.set_color(f'C{color}')
        else:
            legend = self.plotObject[1].get_legend().get_lines()[0]
            legend.set_color(f'C{color}')

        self.plotObject[0].canvas.draw()

    def changeLineType(self, type):
        styles = ['solid', 'dotted', 'dashed', 'dashdot']
        mappedLines = self.mapLines()[self.loadIndex]

        for l in mappedLines:
            l.set_linestyle(styles[type])
        
        self.lineTypeMenuButton.config(text=f"{styles[type]}".title())

        # Update legend
        if len(self.plotObject[1].get_legend().get_lines()) > 1:
            legend = self.plotObject[1].get_legend().get_lines()[self.loadIndex]
            legend.set_linestyle(styles[type])
        else:
            legend = self.plotObject[1].get_legend().get_lines()[0]
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
            self.decimals = self.formatValue(label=self.label, details=self.details)
        else:
            self.envDetailsObject = envDetailsObject
            self.envDetails = envDetailsObject.getDetails()
            self.mode = 1
            self.decimals = self.formatValue(label=self.label, details=self.envDetails)

        self.var = DoubleVar(self.parent, value=f'{"{0:.{decimals}f}".format(float(self.value), decimals=self.decimals)}')

        # Label
        if '2' in self.label:
            label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(self.parent, text=label_subscripted).grid(column=0, row=row)
        else:
            ttk.Label(self.parent, text=self.label).grid(column=0, row=row)

        # Entry
        self.entry = ttk.Label(self.parent, textvariable=self.var, width=7, anchor='center')
        self.entry.grid(column=1, row=row)

        if self.label != 'pH' and self.label != 'k':
            units = app.settings.getUnits()[f'{self.label}_units']
            if len(units) != 1:
                # Unit entry
                if self.label != 'pH' and self.label != 'k':
                    self.menuButton = ttk.Menubutton(self.parent)
                    if self.mode == 0:
                        self.menuButton.config(text=self.details[f'{self.label}_unit'])
                    else:
                        self.menuButton.config(text=self.envDetails[f'{self.label}_unit'])
                    if app.platform == 'linux':
                        tempMenu = Menu(self.menuButton, tearoff=False, background='#EFEBE7')
                    elif app.platform == 'darwin':
                        tempMenu = Menu(self.menuButton, tearoff=False, background='#F5F6F7')
                    else:
                        tempMenu = Menu(self.menuButton, tearoff=False)

                    for i, u in enumerate(units):
                        LoadMenuElem(self, tempMenu, self.menuButton, self.var, u, i, units, f'{self.label}', self.mode)
                    
                    self.menuButton['menu']=tempMenu
                    self.menuButton.grid(column=2, row=row)
            else:
                ttk.Label(self.parent, text=units[0]).grid(column=2, row=row)
        
        if self.mode == 0 and self.label != 'k':
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
        if unit != prevUnit:
            if unit == 'ml/min': # l/min -> ml/min
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])*1000
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')
            
            elif unit == 'l/min': # ml/min -> l/min
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])/1000
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'g/l': # g/dl -> g/l
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])*10
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'g/dl': # g/l -> g/dl
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])/10
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'ml/l': # ml/dl -> ml/l
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])*10
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'ml/dl': # ml/l -> ml/dl
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])/10
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')
            
            elif unit == 'l': #ml -> l
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])/1000
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'ml': #l -> ml
                value = float(self.detailsObject.getWorkLoadDetails()[self.label])*1000
                self.detailsObject.setValue(self.label, value)
                decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'F' or unit == 'K' or unit == '\N{DEGREE SIGN}C':
                if self.mode == 0:
                    value = float(self.detailsObject.getWorkLoadDetails()[self.label])
                else:
                    value = float(self.envDetailsObject.getDetails()[self.label])

                if prevUnit == 'F':
                    if unit == 'K': #F -> K
                        value = 5/9 * (value + 459.67)
                    elif unit == '\N{DEGREE SIGN}C': #F -> C
                        value = (value - 32) / 1.8
                elif prevUnit == 'K':
                    if unit == 'F': #K -> F
                        value = 1.8 * (value - 273) + 32
                    elif unit == '\N{DEGREE SIGN}C': #K -> C
                        value = value - 273.15
                elif prevUnit == '\N{DEGREE SIGN}C':
                    if unit == 'K': #C -> K
                        value = value + 273.15
                    elif unit == 'F': #C -> F
                        value = value * 1.8 + 32

                self.detailsObject.setValue(self.label, value) if self.mode == 0 else self.envDetailsObject.setDetail(self.label, value)
                if self.mode == 0:
                    decimals = self.formatValue(self.label, self.detailsObject.getWorkLoadDetails())
                else:
                    decimals = self.formatValue(self.label, self.envDetailsObject.getDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'm' or unit == 'km' or unit == 'ft':
                value = float(self.envDetailsObject.getDetails()[self.label])

                if prevUnit == 'm':
                    if unit == 'km': #m -> km
                        value = float(value / 1000)
                    elif unit == 'ft': #m -> ft
                        value = float(value * 3.2808399)
                elif prevUnit == 'km':
                    if unit == 'm': #km -> m
                        value = float(value * 1000)
                    elif unit == 'ft': #km -> ft
                        value = float(value * 3280.8399)
                elif prevUnit == 'ft':
                    if unit == 'm': #ft -> m
                        value = float(value * 0.3048)
                    elif unit == 'km': #ft -> km
                        value = float(value * 0.0003048)

                self.envDetailsObject.setDetail(self.label, value)
                self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                decimals = self.formatValue(self.label, self.envDetailsObject.getDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

            elif unit == 'kPa' or unit == 'bar' or unit == 'psi' or unit == 'mmHg':
                value = float(self.envDetailsObject.getDetails()[self.label])

                if prevUnit == 'kPa':
                    if unit == 'bar': #kPa -> bar
                        value = float( value * 0.01 )
                    elif unit == 'psi': #kPa -> psi
                        value = float( value * 0.145037738 )
                    elif unit == 'mmHg': #kPa -> mmHg
                        value = float( value * 7.50061683 )
                elif prevUnit == 'bar':
                    if unit == 'kPa': #bar -> kPa
                        value = float( value * 100 )
                    elif unit == 'psi': #bar -> psi
                        value = float( value * 14.5037738 )
                    elif unit == 'mmHg': #bar -> mmHg
                        value = float( value * 750.061683 )
                elif prevUnit == 'psi':
                    if unit == 'kPa': #psi -> kPa
                        value = float( value * 6.89475729 )
                    elif unit == 'bar': #psi -> bar
                        value = float( value * 0.0689475729 )
                    elif unit == 'mmHg': #psi -> mmHg
                        value = float( value * 51.7149326 )
                elif prevUnit == 'mmHg':
                    if unit == 'kPa': #mmHg -> kPa
                        value = float( value * 0.133322368 )
                    elif unit == 'bar': #mmHg -> bar
                        value = float( value * 0.00133322368 )
                    elif unit == 'psi': #mmHg -> psi
                        value = float( value * 0.0193367747 )

                self.envDetailsObject.setDetail(self.label, value)
                self.envDetailsObject.setDetail(f'{self.label}_unit', unit)
                decimals = self.formatValue(self.label, self.envDetailsObject.getDetails())
                self.var.set(f'{"{0:.{decimals}f}".format(float(value), decimals=decimals)}')

    def getValue(self):
        return self.var.get()
    
    def updateText(self, details):
        decimals = self.formatValue(label=self.label, details=details)
        self.entry.configure(text=f'{"{0:.{decimals}f}".format(float(details[self.label]), decimals=decimals)}')

    def formatValue(self, label, details=None):
        if self.mode == 0:
            if details[f'{label}_unit'] == 'l/min':
                decimals = app.settings.decimals['l/min']
            elif details[f'{label}_unit'] == 'ml/min':
                decimals = app.settings.decimals['ml/min']
            elif details[f'{label}_unit'] == 'ml/l':
                decimals = app.settings.decimals['ml/l']
            elif details[f'{label}_unit'] == 'ml/dl':
                decimals = app.settings.decimals['ml/dl']
            elif details[f'{label}_unit'] == 'ml/min/mmHg':
                decimals = app.settings.decimals['ml/min/mmHg']
            elif details[f'{label}_unit'] == 'g/l':
                decimals = app.settings.decimals['g/l']
            elif details[f'{label}_unit'] == 'mmHg':
                decimals = app.settings.decimals['mmHg']
            elif details[f'{label}_unit'] == '\N{DEGREE SIGN}C':
                decimals = app.settings.decimals['\N{DEGREE SIGN}C']
            elif details[f'{label}_unit'] == 'K':
                decimals = app.settings.decimals['K']
            elif details[f'{label}_unit'] == 'F':
                decimals = app.settings.decimals['F']
            elif details[f'{label}_unit'] == 'ml':
                decimals = app.settings.decimals['ml']
            elif details[f'{label}_unit'] == 'bmp':
                decimals = app.settings.decimals['bpm']
            elif details[f'{label}_unit'] == '%':
                decimals = app.settings.decimals['%']
            else:
                decimals = 2
        else:
            if details[f'{label}_unit'] == 'm':
                decimals = app.settings.decimals['m']
            elif details[f'{label}_unit'] == 'km':
                decimals = app.settings.decimals['km']
            elif details[f'{label}_unit'] == 'ft':
                decimals = app.settings.decimals['ft']
            elif details[f'{label}_unit'] == 'kPa':
                decimals = app.settings.decimals['kPa']
            elif details[f'{label}_unit'] == 'bar':
                decimals = app.settings.decimals['bar']
            elif details[f'{label}_unit'] == 'psi':
                decimals = app.settings.decimals['psi']
            elif details[f'{label}_unit'] == '%':
                decimals = app.settings.decimals['%']
            else:
                decimals = 2

        return decimals

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
                self.parentObject.updateText(details=l.getWorkLoadDetails())

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
                        plt.gca().yaxis.set_label_text(r'VO$_2$(L/min)')
                        yValueVar.set(yValue/1000)
                    elif unit == 'ml/min':
                        plt.gca().yaxis.set_label_text(r'VO$_2$ (ml/min)')
                        yValueVar.set(yValue*1000)

                    figure = app.getPlottingPanel().plots[plotIndex].plot[0]
                    figure.canvas.draw()

        else:
            # update unit change to every loadtab env details
            workLoads = self.parentObject.parentObject.parentObject.activeTest.workLoads
            for l in workLoads:
                l.envDetails.setDetail(f'{self.name}_unit', unit)
                self.parentObject.updateText(details=l.envDetails.getDetails())
            
            # update unit change to every loadtab
            for tab in self.parentObject.parentObject.parentObject.loadTabs:
                for elem in tab.rowElements:
                    if elem.label == self.name:
                        elem.updateEntryAndScale(unit, prevUnit)
                        elem.menuButton.config(text=unit)
                        break