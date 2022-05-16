from tkinter import *
from tkinter import ttk
import math
from objects.app import app
from modules.notification import notification
from modules.ScrollableNotebook import ScrollableNotebook
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

#
# SVO2 - kumpaa arvoa käytetään, todennäköisesti ph/temp korjauksen jälkeistä?
#

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
            validValues = self.calc(w, details)
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
            plotTabObject = PlotTab(self.plotNotebook, self.workLoadDetailsObjects)

            # Add plot to the notebook and objects list of plots
            self.plotNotebook.add(plotTabObject, text=app.getActiveTest().id)
            self.plots.append(plotTabObject)

            # Make last tab active
            self.plotNotebook.select(self.plotNotebook.index('end')-1)

        else:
            notification.create('error', f'Invalid values. Please check the units and values of {i+1}. load and try again.', 5000)

    def plotProject(self):
        ##
        ## INFO: Pitäiskö filteröidä tyhjät pois?
        ##
        workLoadDetailsObjects = []
        for w in app.getActiveTest().getWorkLoads():
            w = w.getDetails()
            workLoadDetailsObjects.append(w)
        # self.workLoads = app.getActiveTest().getWorkLoads()
        try:
            self.plotNotebook.pack_info()
        except TclError:
            self.plotNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tab for the plot
        plotTabObject = PlotTab(self.plotNotebook, workLoadDetailsObjects)
        plotTab = plotTabObject.createPlotTab()

        # Add plot to the notebook and objects list of plots
        self.plotNotebook.add(plotTab, text=app.getActiveTest().id)
        self.plots.append(plotTabObject)

    def formatQ(self, w, details):
        Q = float(details["Q"])
        unit = details["Q_unit"]

        if Q == 0:
            HR = float(details['HR'])
            SV = float(details['SV'])
            SvUnit = details['SV_unit']
            w.setMC('Q_MC', 1)

            # If HR and SV is given
            if HR != 0 and SV != 0:
                if unit == 'l/min': # Convert Q to l/min
                    if SvUnit == 'ml': # ml -> l
                        SV = SV / 1000

                elif unit == 'ml/min': # Convert Q to ml/min
                    if SvUnit == 'l':
                        SV = SV * 1000 # l -> ml
                    
                return HR * SV
                
            # If HR and SV not given, try with VO2 and CavO2
            else:
                VO2 = float(details['VO2'])
                VO2unit = details['VO2_unit']
                CavO2 = float(details['C(a-v)O2'])
                CavO2unit = details['C(a-v)O2_unit']

                # If VO2 and CavO2 is given
                if VO2 != 0 and CavO2 != 0:
                    if unit == 'l/min': # Convert Q to l/min

                        if VO2unit == 'ml/min':
                            VO2 = VO2 / 1000

                        if CavO2unit == 'ml/l': # -> l/l
                            CavO2 = CavO2 / 1000
                        elif CavO2unit == 'ml/dl':
                            CavO2 = CavO2 / 100

                        return VO2 / CavO2 # l/min

                    elif unit == 'ml/min': # Convert Q to ml/min
                        if VO2unit == 'l/min':
                            VO2 = VO2 / 1000

                        if CavO2unit == 'ml/l': # -> l/l
                            CavO2 = CavO2 / 1000
                        elif CavO2unit == 'ml/dl':
                            CavO2 = CavO2 / 100

                        return VO2 / CavO2 # l/min
                else:
                    return 0
        else:
            return Q

    def formatVO2(self, w, details, Q):
        VO2 = float(details['VO2'])
        unit = details['VO2_unit']

        if VO2 == 0:
            CavO2 = float(details['C(a-v)O2'])
            CavO2Unit = details['C(a-v)O2_unit']
            QUnit = details['Q_unit']
            w.setMC('VO2_MC', 1)

            if Q != 0 and CavO2 != 0:
                if CavO2Unit == 'ml/dl': # -> l/l
                    CavO2 = CavO2 / 100
                else:
                    CavO2 = CavO2 / 1000 # -> l/l

                if QUnit == 'ml/min': # -> l/min
                    Q = Q / 1000

                if unit == 'l/min': # Convert VO2 to l/min
                    return Q * CavO2

                elif unit == 'ml/min': # Convert VO2 to ml/min
                    return Q * CavO2 * 1000
        else:
            return VO2
    
    def formatHb(self, details):
        Hb = float(details['[Hb]'])
        unit = details['[Hb]_unit']

        return Hb

    def formatCavO2(self, w, details, VO2, Q):
        CavO2 = float(details['C(a-v)O2'])
        unit = details['C(a-v)O2_unit']
        CaO2 = float(details['CaO2'])
        CaO2unit = details['CaO2_unit']
        CvO2 = float(details['CvO2'])
        CvO2unit = details['CvO2_unit']

        if CavO2 == 0:
            w.setMC('C(a-v)O2_MC', 1)

            # If CaO2 and CvO2 is given
            if CaO2 != 0 and CvO2 != 0:
                if unit == 'ml/l':
                    if CaO2unit == 'ml/dl': # -> ml/l
                        CaO2 = CaO2 * 10
                    if CvO2unit == 'ml/dl': # -> ml/l
                        CvO2 = CvO2 * 10

                    return CaO2 - CvO2 # ml/l
                elif unit == 'ml/dl':
                    if CaO2unit == 'ml/l': # -> ml/dl
                        CaO2 = CaO2 / 10
                    if CvO2unit == 'ml/l': # -> ml/dl
                        CvO2 = CvO2 / 10

                    return CaO2 - CvO2 # ml/dl
            else:
                VO2Unit = details['VO2_unit']
                QUnit = details['Q_unit']
                
                if unit == 'ml/l':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'ml/min': # -> l/min
                        Q = Q / 1000
                    
                    return VO2 / Q

                elif unit == 'ml/dl':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'l/min': # -> dl/min
                        Q = Q * 10
                    elif QUnit == 'ml/min':
                        Q = Q / 100
                    
                    return VO2 / Q
        else:
            return CavO2
            # If C(a-v)O2 is given, ensure that it fulfills
            # the equations.
            """ print('CAVO2 TARKISTUKSEEN')

            # If CaO2 and CvO2 is given
            if CaO2 != 0 and CvO2 != 0:
                if unit == 'ml/l':
                    if CaO2unit == 'ml/dl': # -> ml/l
                        CaO2 = CaO2 * 10
                    if CvO2unit == 'ml/dl': # -> ml/l
                        CvO2 = CvO2 * 10

                    if CavO2 != (CaO2 - CvO2):
                        w.setMC('C(a-v)O2_MC', 1)
                        print('LASKETTU')
                        return CaO2 - CvO2 # ml/l
                elif unit == 'ml/dl':
                    if CaO2unit == 'ml/l': # -> ml/dl
                        CaO2 = CaO2 / 10
                    if CvO2unit == 'ml/l': # -> ml/dl
                        CvO2 = CvO2 / 10

                    if CavO2 != (CaO2 - CvO2):
                        w.setMC('C(a-v)O2_MC', 1)
                        print('LASKETTU')
                        return CaO2 - CvO2 # ml/dl

            else:
                VO2Unit = details['VO2_unit']
                QUnit = details['Q_unit']
                    
                if unit == 'ml/l':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'ml/min': # -> l/min
                        Q = Q / 1000
                    
                    if CavO2 != (VO2 / Q):
                        w.setMC('C(a-v)O2_MC', 1)
                        print('LASKETTU')
                        return VO2 / Q

                elif unit == 'ml/dl':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'l/min': # -> dl/min
                        Q = Q * 10
                    elif QUnit == 'ml/min':
                        Q = Q / 100

                    if CavO2 != (VO2 / Q):
                        w.setMC('C(a-v)O2_MC', 1)
                        print('LASKETTU')
                        return VO2 / Q """
            
    def formatCaO2(self, w, details, Hb, SaO2):
        CaO2 = float(details['CaO2'])
        unit = details['CaO2_unit']

        if CaO2 == 0:
            w.setMC('CaO2_MC', 1) # Mark as calculated
            HbUnit = details['[Hb]_unit']

            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            return 1.34 * Hb * SaO2
        else:
            return CaO2

    def formatCvO2(self, w, details, Hb, CaO2, CavO2, SvO2):
        CvO2 = float(details['CvO2'])
        unit = details['CvO2_unit']

        if CvO2 == 0:
            w.setMC('CvO2_MC', 1)
            HbUnit = details['[Hb]_unit']
            
            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            
            # CvO2 = 1.34 x [Hb] x SvO2 / 100
            return 1.34 * Hb * SvO2
        else:
            return CvO2 
    
    def formatSvO2(self, w, details, CavO2, CaO2, Hb):
        SvO2 = float(details['SvO2'])

        if SvO2 == 0:
            w.setMC('SvO2_MC', 1)
            CaO2Unit = details['CaO2_unit']
            CavO2Unit = details['C(a-v)O2_unit']
            HbUnit = details['[Hb]_unit']

            if CaO2Unit == 'ml/l': # -> ml/dl
                CaO2 = CaO2 / 10
            if CavO2Unit == 'ml/l': # -> ml/dl
                CavO2 = CavO2 / 10
            if HbUnit == 'g/l': # -> g/dl
                Hb = Hb / 10
            # print(f'WTF {CaO2}, {CavO2}, {Hb}')
            # SvO2 = (CaO2 - C(a-v)O2) x 100 / 1,34 / [Hb]
            return (CaO2 - CavO2) / 1.34 / Hb
        else:
            return SvO2 / 100

    def formatQaO2(self, w, details, Q, CaO2):
        QO2 = float(details['QaO2'])
        unit = details['QaO2_unit']
        QUnit = details['Q_unit']
        CaO2Unit = details['CaO2_unit']

        if QO2 == 0:
            w.setMC('QaO2_MC', 1)
        
            if CaO2Unit == 'ml/l': # l/l
                CaO2 = CaO2 / 1000
            elif CaO2Unit == 'ml/dl': # -> dl/dl
                CaO2 = CaO2 / 100

            if unit == 'ml/min':
                if QUnit == 'l/min': # -> ml/min
                    Q = Q * 1000
            elif unit == 'l/min':
                if QUnit == 'ml/min': # -> l/min
                    Q = Q / 1000
            
            return Q * CaO2
        else:
            return QO2

    def formatPvO2(self, w, details, a, b):
        PvO2 = float(details['PvO2'])

        w.setMC('PvO2_MC', 1)
        return np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))

        """ if PvO2 == 0:
            w.getDetails().setMC('PvO2_MC', 1)
            return np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        else:
            return PvO2 """

    def phTempCorrection(self, pH0, pH, T0, T, PvO2_calc):
        lnPvO2 = np.log(PvO2_calc)
        if pH != pH0 or T != T0:
            lnPO2pH = (pH - pH0) * (-1.1)
            lnPO2Temp = (T-T0) * 0.058 * np.float_power(0.243 * np.float_power(PvO2_calc/100, 3.88) + 1, -1) + (T-T0) * 0.013
        else:
            lnPO2pH = 0
            lnPO2Temp = 0

        PvO2_calc = np.exp( lnPvO2 + lnPO2Temp + lnPO2pH )

        return PvO2_calc

    def formatT(self, details, label):
        T = float(details[label])
        unit = details[f'{label}_unit']

        if unit == 'F':
            return (T - 32)/1.8
        if unit == 'K':
            return T - 273.15
        else:
            return T

    def solveDO2(self, w, details, VO2, PvO2_calc):
        VO2Unit = details['VO2_unit']

        if VO2Unit == 'ml/min': # -> l/min
            VO2 = VO2 / 1000
        
        return VO2 / 2 / PvO2_calc * 1000

    def calc(self, w, details): #w=workload object, details=dict
        validValues = True
        Q = self.formatQ(w, details)
        VO2 = self.formatVO2(w, details, Q)
        if VO2 == 0 or VO2 == None:
            print('VO2 NOLLA')
            validValues = False
            return validValues
        Hb = self.formatHb(details)
        SaO2 = float(details['SaO2'])

        # print(f'Q {Q} - VO2 {VO2} - Hb {Hb} - SaO2 {SaO2}')

        CaO2 = self.formatCaO2(w, details, Hb, SaO2/100)
        CavO2 = self.formatCavO2(w, details, VO2, Q)
        SvO2_calc = self.formatSvO2(w, details, CavO2, CaO2, Hb)
        CvO2 = self.formatCvO2(w, details, Hb, CaO2, CavO2, SvO2_calc)
        QaO2 = self.formatQaO2(w, details, Q, CaO2)

        # print(f'CavO2 {CavO2} - CaO2 {CaO2} - CvO2 {CvO2} - SvO2_calc {SvO2_calc} - QaO2 {QaO2}')

        # Calculate diffusion DO2
        a = 11700 * np.float_power( ( np.float_power(SvO2_calc,-1) - 1 ), -1 )
        b = np.float_power( 50**3 + np.float_power(a,2), 0.5 )
        PvO2_calc = self.formatPvO2(w, details, a, b) # mmHg
        # print(f'WTF2: {a}, {b}, {PvO2_calc}')

        if PvO2_calc < 0:
            # print('PvO2 negative')
            validValues = False
            return validValues

        # pH + temp correction
        # pH = float(details['pH @ rest'])
        pH = float(details['pH'])
        pH0 = float(details['pH @ rest'])
        # T = self.formatT(details, 'Tc\u209A\u2091\u2090\u2096')
        T = self.formatT(details, 'T')
        T0 = self.formatT(details, 'Tc @ rest')
        # print(f'pHrest {pH0}, pH {pH}, Trest {T0}, T {T}')
        PvO2_calc = self.phTempCorrection(pH0, pH, T0, T, PvO2_calc)

        DO2 = self.solveDO2(w, details, VO2, PvO2_calc)

        # Fick's law - Diffusion line 
        # VO2 = DO2 * 2 * PvO2

        PvO2 = np.arange(0,100,1)
        y = 2 * DO2 * PvO2

        # Fick's principle - Convection curve 
        # VO2 = CO * C(a-v)O2                           | CaO2 = 1.34 x Hb x SaO2 
        #                                               | CvO2 = 1.34 x Hb x SvO2
        #
        # f(PvO2) = CO x ( 1.34 x Hb (SaO2 - SvO2) )    | SvO2 = ((23400((PvO2)^3+ 150PvO2)^-1) + 1)^-1
        # 
        # f(PvO2) = CO x (1.34 x Hb x (SaO2 - ((23400((PvO2)^3+ 150PvO2)^-1) + 1)^-1))

        # Prevent runtimewarning (divide by 0)
        with np.errstate(divide='ignore'):
            SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )
        SvO2[np.isnan(SvO2)] = 0

        # Convert to l/min
        if details['Q_unit'] == 'ml/min':
            Q = Q / 1000

        if details['[Hb]_unit'] == 'g/l': # -> g/dl
            Hb = Hb / 10

        y2 = Q * ( 1.34 * Hb * ( SaO2/ 100 - SvO2 ) ) * 10

        # Correction and calculation of intersection point
        idx = np.argwhere(np.diff(np.sign(y - y2))).flatten()
        yDiff = []

        for i in np.arange(0, 1, 0.1):
            y_temp = 2* DO2 * (PvO2[idx]+i)
            y2_temp = Q * ( 1.34 * Hb * ( SaO2/ 100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10

            try:
                yDiff.append( (float(y_temp)-float(y2_temp)) )
            except TypeError:
                #print('TYPEERROR IN CALC')
                validValues = False
                return validValues

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * Hb * ( SaO2/ 100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)

        if details['[Hb]_unit'] == 'g/l': # g/dl -> g/l
            Hb = Hb * 10

        if details['Q_unit'] == 'ml/min': # l/min -> ml/min
            Q = Q * 1000

        SvO2_calc = SvO2_calc * 100

        w.setCalcResults(y, y2, xi, yi, VO2, Q, Hb, SaO2, CaO2, SvO2_calc, CvO2, CavO2, QaO2, T0, T, pH0, pH, PvO2_calc, DO2)
        #print(f'UPDATED DETAILS: {w.getDetails().getWorkLoadDetails()}')
        return validValues

class PlotTab(ttk.Frame):
    def __init__(self, parentFrame, workLoadDetailsObjects, *args, **kwargs):
        ttk.Frame.__init__(self, parentFrame, *args, **kwargs)
        self.pack(expand=TRUE)
        
        self.plot = None
        self.loadTabs = []
        self.activeTest = app.getActiveTest()
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

        self.fixLegend()

    def fixLegend(self):
        self.update_idletasks()
        legSize = self.leg._legend_box.get_window_extent(self.fig.canvas.get_renderer())
        ratio = legSize.width/self.plotFrame.winfo_width()
        print(f'width of plotframe: {self.plotFrame.winfo_width()}')
        print(f'width of canvastk: {self.canvasTk.winfo_width()}')
        print(f'width of canvasframe: {self.canvasFrame.winfo_width()}')
        print(ratio)
        # plt.subplots_adjust(right=0.965-ratio)

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

        # self.plotFrame.bind('<Configure>', lambda e: self.plot[0].canvas.draw())
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
        self.yEntry = ttk.Entry(setYLimFrame, textvariable=self.yValue, width=6)
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
        ratio = legSize.width/self.plotFrame.winfo_width()

        vis = legend.get_visible()
        if vis:
            legend.set_visible(False)
            plt.subplots_adjust(right=0.925)
        else:
            legend.set_visible(True)
            plt.subplots_adjust(right=0.965-ratio)
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

    def defSize(self, event):
        self.indicator.configure(text='', background=app.root.cget('bg'))
        self.loadNotebookFrame.pack_propagate(True)
    
    def setYLim(self):
        vo2unit = self.workLoadDetailsObjects[0].VO2_unit
        if vo2unit == 'ml/min':
            limit = float(self.yValue.get())
        elif vo2unit == 'l/min':
            limit = float(self.yValue.get()) * 1000
        #print(f'limit {limit}')
        self.plot[1].set_ylim(top=float(limit))
        self.plot[0].canvas.draw()

    def createPlot(self):
        PvO2 = np.arange(0,100,1)
        self.plot = plt.subplots()
        self.fig, self.ax = self.plot

        self.ax.set_title('O\u2082 Pathway')
        self.ax.set_xlabel('PvO\u2082 (mmHg)')
        self.ax.set_xlim(left=0, right=100)
        plt.subplots_adjust(bottom=0.175)
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

        # self.leg = self.ax.legend(handles=self.handles , loc='upper right',
        #     fancybox=True, shadow=True, ncol=3)

        # plt.subplots_adjust(right=0.8)
        self.leg = self.ax.legend(handles=self.handles , loc='upper left', bbox_to_anchor=(1.01, 1),
            fancybox=True, shadow=True, ncol=1)

        self.leg.set_visible(False)
        
        # print(type(self.fig))
        # plt.subplots_adjust(right=0.8-legSize.width/1000)
        # self.fig.set(figwidth=figSize.width-legSize.width/100)

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
        print('ON PICK')
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
        print('ON CLICK')
        # print(vars(self.leg))
        # print(vars(self.leg._legend_title_box))
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
        self.parentObject = plotTab
        self.index = index
        self.testId = testId
        self.detailsObject = workLoadDetails # Workdetail object
        self.details = workLoadDetails.getWorkLoadDetails() # Workload details dict
        self.parentNotebook = parentNotebook
        self.plot = plot
        self.rowElements = []

        ##
        ## Details frame
        ##

        ttk.Label(self, text='Value').grid(column=1, row=0)
        ttk.Label(self, text='Unit').grid(column=2, row=0)
        ttk.Label(self, text='Meas.').grid(column=3, row=0)
        ttk.Label(self, text='Calc.').grid(column=4, row=0)
        
        if app.settings.getTestDef()['loadMode'] == 0:
            ttk.Label(self, text='Load').grid(column=0, row=1)
            ttk.Label(self, text=self.details["Load"]).grid(column=1, row=1)
            ttk.Label(self, text=self.details["Load_unit"]).grid(column=2, row=1)
        else:
            ttk.Label(self, text='Velocity').grid(column=0, row=1)
            ttk.Label(self, text=self.details["Velocity"]).grid(column=1, row=1)
            ttk.Label(self, text=self.details["Velocity_unit"]).grid(column=2, row=1)

            ttk.Label(self, text='Incline').grid(column=0, row=2)
            ttk.Label(self, text=self.details["Incline"]).grid(column=1, row=2)
            ttk.Label(self, text=self.details["Incline_unit"]).grid(column=2, row=2)

        # VO2
        vo2Value = float(self.details['VO2'])
        if self.details['VO2_unit'] == 'l/min':
            self.vo2Row = LoadTabRow(self, self, 'VO2', vo2Value, self.index, self.testId, 3, (0,10), self.detailsObject)
        else:
            self.vo2Row = LoadTabRow(self, self, 'VO2', vo2Value, self.index, self.testId, 3, (0,10000), self.detailsObject)
        self.rowElements.append(self.vo2Row)

        # Q
        qValue = float(self.details['Q'])
        if self.details['Q_unit'] == 'l/min':
            self.qRow = LoadTabRow(self, self, 'Q', qValue, self.index, self.testId, 4, (0,25), self.detailsObject)
        else:
            self.qRow = LoadTabRow(self, self, 'Q', qValue, self.index, self.testId, 4, (0,25000), self.detailsObject)
        self.rowElements.append(self.qRow)

        # Hb
        hbValue = float(self.details['[Hb]'])
        if self.details['[Hb]_unit'] == 'g/dl':
            self.hbRow = LoadTabRow(self, self, '[Hb]', hbValue, self.index, self.testId, 5, (0,20), self.detailsObject)
        else:
            hbValue = hbValue
            self.hbRow = LoadTabRow(self, self, '[Hb]', hbValue, self.index, self.testId, 5, (0,200), self.detailsObject)
        self.rowElements.append(self.hbRow)

        # SaO2
        sao2Value = float(self.details['SaO2'])
        self.sao2Row = LoadTabRow(self, self, 'SaO2', sao2Value, self.index, self.testId, 6, (80,100), self.detailsObject)
        self.rowElements.append(self.sao2Row)

        # SvO2
        svo2Value = float(self.details['SvO2'])
        self.svo2Row = LoadTabRow(self, self, 'SvO2', svo2Value, self.index, self.testId, 7, (0,20), self.detailsObject)
        self.rowElements.append(self.svo2Row)

        # CaO2
        cao2Value = float(self.details['CaO2'])
        if self.details['CaO2_unit'] == 'ml/dl':
            self.cao2Row = LoadTabRow(self, self, 'CaO2', cao2Value, self.index, self.testId, 8, (0,100), self.detailsObject)
        else:
            self.cao2Row = LoadTabRow(self, self, 'CaO2', cao2Value, self.index, self.testId, 8, (0,1000), self.detailsObject)
        self.rowElements.append(self.cao2Row)

        # CvO2
        cvo2Value = float(self.details['CvO2'])
        if self.details['CvO2_unit'] == 'ml/dl':
            self.cvo2Row = LoadTabRow(self, self, 'CvO2', cvo2Value, self.index, self.testId, 9, (0,100), self.detailsObject)
        else:
            self.cvo2Row = LoadTabRow(self, self, 'CvO2', cvo2Value, self.index, self.testId, 9, (0,1000), self.detailsObject)
        self.rowElements.append(self.cvo2Row)
        
        # CavO2
        cavo2Value = float(self.details['C(a-v)O2'])
        if self.details['C(a-v)O2_unit'] == 'ml/dl':
            self.cavo2Row = LoadTabRow(self, self, 'C(a-v)O2', cavo2Value, self.index, self.testId, 10, (0,100), self.detailsObject)
        else:
            self.cavo2Row = LoadTabRow(self, self, 'C(a-v)O2', cavo2Value, self.index, self.testId, 10, (0,1000), self.detailsObject)
        self.rowElements.append(self.cavo2Row)

        # PvO2
        pvo2Value = self.details['PvO2']
        self.pvo2Row = LoadTabRow(self, self, 'PvO2', pvo2Value, self.index, self.testId, 11, (0,100), self.detailsObject)
        self.rowElements.append(self.pvo2Row)

        # QaO2
        qao2Value = float(self.details['QaO2'])
        if self.details['QaO2_unit'] == 'ml/min':
            self.qao2Row = LoadTabRow(self, self, 'QaO2', qao2Value, self.index, self.testId, 12, (0,10000), self.detailsObject)
        else:
            self.qao2Row = LoadTabRow(self, self, 'QaO2', qao2Value, self.index, self.testId, 12, (0,10), self.detailsObject)
        self.rowElements.append(self.qao2Row)

        # DO2
        do2Value = self.details['DO2']
        self.do2Row = LoadTabRow(self, self, 'DO2', do2Value, self.index, self.testId, 13, (0,100), self.detailsObject)
        self.rowElements.append(self.do2Row)

        # T
        tValue = float(self.details['T'])
        if self.details['T_unit'] == 'F':
            tValue = (tValue - 32) / 1.8
            self.tRow = LoadTabRow(self, self, 'T', tValue, self.index, self.testId, 14, (95,110), self.detailsObject)
        elif self.details['T_unit'] == 'K':
            tValue = tValue - 273.15
            self.tRow = LoadTabRow(self, self, 'T', tValue, self.index, self.testId, 14, (300,320), self.detailsObject)
        else:
            self.tRow = LoadTabRow(self, self, 'T', tValue, self.index, self.testId, 14, (35,42), self.detailsObject)
        self.rowElements.append(self.tRow)

        # pH
        phValue = self.details['pH']
        self.phRow = LoadTabRow(self, self, 'pH', phValue, self.index, self.testId, 15, (0,14), self.detailsObject)
        self.rowElements.append(self.phRow)

        ##
        ## Options frame
        ##

        # Plot options
        optionsFrame = ttk.Frame(self)
        optionsFrame.grid(column=0, columnspan=5, row=16)
        
        # Plot options
        PlotOptions(optionsFrame, self.plot, self.index)

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
    def __init__(self, parentObject, parentFrame, label, value, index, id, row, scale, detailsObject, *args, **kwargs):
        ttk.Frame.__init__(self, parentFrame, *args, **kwargs)
        # self.grid()
        self.parentObject = parentObject
        self.parent = parentFrame
        self.label = label
        self.value = value
        self.index = index
        self.id = id
        self.row = row
        self.scale = scale
        self.detailsObject = detailsObject
        self.details = detailsObject.getWorkLoadDetails()

        # Adjust the number of decimal according to the used unit
        # print(self.details[f'{self.label}_unit'])

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
                    self.menuButton.config(text=self.details[f'{self.label}_unit'])
                    tempMenu = Menu(self.menuButton, tearoff=False)

                    for i, u in enumerate(units):
                        LoadMenuElem(self, tempMenu, self.menuButton, self.var, u, i, units, f'{self.label}')
                    
                    self.menuButton['menu']=tempMenu
                    self.menuButton.grid(column=2, row=row)
            else:
                ttk.Label(self.parent, text=units[0]).grid(column=2, row=row)
            
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

            elif unit == 'F': 
                if prevUnit == '\N{DEGREE SIGN}C': # C -> F
                    self.detailsObject.setValue(self.label, self.var.get() * 1.8 + 32)
                    self.var.set( f'{"{0:.1f}".format( float(( self.var.get() * 1.8 + 32 )) )}' )
                else: # K -> F
                    self.detailsObject.setValue(self.label, 1.8 * (self.var.get() - 273) + 32)
                    self.var.set( f'{"{0:.1f}".format( float(( 1.8 * (self.var.get() - 273) + 32)) )}' )

            elif unit == 'K':
                if prevUnit == '\N{DEGREE SIGN}C': # C -> K
                    self.detailsObject.setValue(self.label, self.var.get() + 273.15)
                    self.var.set( f'{"{0:.1f}".format( float(( self.var.get() + 273.15)) )}' )
                else: # F -> K
                    self.detailsObject.setValue(self.label, 5/9 * (self.var.get() + 459.67))
                    self.var.set( f'{"{0:.1f}".format( float(( 5/9 * (self.var.get() + 459.67) )) )}' )
            
            elif unit == '\N{DEGREE SIGN}C': # K/F -> C
                if self.var.get() > 94 and self.var.get() < 111: # F
                    self.detailsObject.setValue(self.label, (self.var.get() - 32) / 1.8)
                    self.var.set( f'{"{0:.1f}".format( float(( (self.var.get() - 32) / 1.8)) )}' )
                else: # K
                    self.detailsObject.setValue(self.label, self.var.get() - 273.15)
                    self.var.set( f'{"{0:.1f}".format( float(( self.var.get() - 273.15)) ) }' )

    def getValue(self):
        return self.var.get()
    
    def updateText(self, details):
        self.entry.configure(text=f'{"{0:.1f}".format(float(details[self.label]))}')

class LoadMenuElem(object):
    def __init__(self, parentObject, menu, menuButton, var, label, index, unitElems, name):
        self.parentObject = parentObject
        self.menu = menu
        self.menuButton = menuButton
        self.var = var
        self.label = label
        self.index = index
        self.unitElems = unitElems
        self.name = name

        self.menu.add_command(label=f'{self.label}', command=lambda: self.updateValue())

    def updateValue(self):
        prevUnit = self.menuButton.cget("text")
        unit = self.unitElems[self.index]
        self.menuButton.config(text=unit)
        
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