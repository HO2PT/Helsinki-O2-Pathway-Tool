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

#
# BUG: Figure puskee toolbarit piiloon -> figure pitää saada kehystettyä paremmin
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
        self.origWorkLoads = app.getActiveTest().getWorkLoads()
        self.workLoads = copy.deepcopy(self.origWorkLoads) # Workload objects
        validValues = True

        print('VALIDATING VALUES')
        for i, w in enumerate(self.workLoads):
            details = w.getDetails().getWorkLoadDetails()
            validValues = self.calc(w, details)
            if validValues == False:
                break

        # Proceed if values are valid
        if validValues == True:
            print('VALUES OK')
            # Check if plotNotebook is visible and if not, make it visible
            try:
                self.plotNotebook.pack_info()
            except TclError:
                self.plotNotebook.pack(expand=TRUE, fill=BOTH)

            # Create tab for the plot
            plotTabObject = PlotTab(self.plotNotebook, self.workLoads)
            plotTab = plotTabObject.createPlotTab()

            # Add plot to the notebook and objects list of plots
            self.plotNotebook.add(plotTab, text=app.getActiveTest().id)
            self.plots.append(plotTabObject)
        else:
            print('VALIDATION ERROR')
            notification.create('error', f'Invalid values. Please check the values of {i+1}. load and try again.', 5000)
    
    def plotProject(self):
        self.workLoads = app.getActiveTest().getWorkLoads()
        try:
            self.plotNotebook.pack_info()
        except TclError:
            self.plotNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tab for the plot
        plotTabObject = PlotTab(self.plotNotebook, self.workLoads)
        plotTab = plotTabObject.createPlotTab()

        # Add plot to the notebook and objects list of plots
        self.plotNotebook.add(plotTab, text=app.getActiveTest().id)
        self.plots.append(plotTabObject)

    def formatQ(self, w, details, updatedVar):
        Q = float(details["Q"])
        unit = details["Q_unit"]

        if Q == 0:
            HR = float(details['HR'])
            Sv = float(details['Sv'])
            SvUnit = details['Sv_unit']
            w.getDetails().setMC('Q_MC', 1)

            # If HR and Sv is given
            if HR != 0 and Sv != 0:
                if unit == 'l/min': # Convert Q to l/min
                    if SvUnit == 'ml': # ml -> l
                        Sv = Sv / 1000

                elif unit == 'ml/min': # Convert Q to ml/min
                    if SvUnit == 'l':
                        Sv = Sv * 1000 # l -> ml
                    
                return HR * Sv
                
            # If HR and Sv not given, try with VO2 and CavO2
            else:
                VO2 = float(details['VO2'])
                VO2unit = details['VO2_unit']
                CavO2 = float(details['CavO2'])
                CavO2unit = details['CavO2_unit']

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
            #return Q
            if updatedVar == 'HR' or updatedVar == 'Sv':
                HR = float(details['HR'])
                Sv = float(details['Sv'])
                SvUnit = details['Sv_unit']
                w.getDetails().setMC('Q_MC', 1)

                # If HR and Sv is given
                if HR != 0 and Sv != 0:
                    if unit == 'l/min': # Convert Q to l/min
                        if SvUnit == 'ml':
                            Sv = Sv / 1000
                        #return HR * Sv
                    elif unit == 'ml/min': # Convert Q to ml/min
                        if SvUnit == 'l':
                            Sv = Sv * 1000
                        
                    return HR * Sv
            elif updatedVar == 'VO2' or updatedVar == 'CavO2':
                VO2 = float(details['VO2'])
                VO2unit = details['VO2_unit']
                CavO2 = float(details['CavO2'])
                CavO2unit = details['CavO2_unit']

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
                return Q

    def formatVO2(self, w, details, Q, updatedVar, VO2Lock):
        VO2 = float(details['VO2'])
        unit = details['VO2_unit']

        if VO2 == 0:
            CavO2 = float(details['CavO2'])
            CavO2Unit = details['CavO2_unit']
            QUnit = details['Q_unit']
            w.getDetails().setMC('VO2_MC', 1)

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
            if VO2Lock == False:
                if updatedVar == 'CavO2' or updatedVar == 'Q':
                    print('Q IS UPDATED (VO2)')
                    CavO2 = float(details['CavO2'])
                    CavO2Unit = details['CavO2_unit']
                    QUnit = details['Q_unit']
                    w.getDetails().setMC('VO2_MC', 1)

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
            else:
                return VO2
    
    def formatHb(self, details, updatedVar):
        Hb = float(details['Hb'])
        unit = details['Hb_unit']

        return Hb

    def formatCavO2(self, w, details, VO2, Q, updatedVar):
        CavO2 = float(details['CavO2'])
        unit = details['CavO2_unit']
        CaO2 = float(details['CaO2'])
        CaO2unit = details['CaO2_unit']
        CvO2 = float(details['CvO2'])
        CvO2unit = details['CvO2_unit']

        if CavO2 == 0:
            w.getDetails().setMC('CavO2_MC', 1)

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
            if updatedVar == 'CaO2' or updatedVar == 'CvO2':
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
            elif updatedVar == 'Q' or updatedVar == 'VO2':
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
                    elif QUnit == 'ml/min': # -> dl/min
                        Q = Q / 100
                    
                    return VO2 / Q
            else:
                return CavO2
            
    def formatCaO2(self, w, details, Hb, SaO2, updatedVar):
        CaO2 = float(details['CaO2'])
        unit = details['CaO2_unit']

        if CaO2 == 0:
            w.getDetails().setMC('CaO2_MC', 1) # Mark as calculated
            HbUnit = details['Hb_unit']

            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            return 1.34 * Hb * SaO2
        else:
            #if updatedVar == 'Hb' or updatedVar == 'SaO2':
            if updatedVar:
                HbUnit = details['Hb_unit']

                if unit == 'ml/l':
                    if HbUnit == 'g/dl': # -> g/l
                        Hb = Hb * 10
                elif unit == 'ml/dl':
                    if HbUnit == 'g/l': # -> g/dl
                        Hb = Hb / 10
                return 1.34 * Hb * SaO2
            else:
                return CaO2

    def formatCvO2(self, w, details, Hb, CaO2, CavO2, SvO2, updatedVar):
        CvO2 = float(details['CvO2'])
        unit = details['CvO2_unit']

        if CvO2 == 0:
            w.getDetails().setMC('CvO2_MC', 1)
            HbUnit = details['Hb_unit']
            
            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            
            # CvO2 = 1.34 x [Hb] x SvO2 / 100
            return 1.34 * Hb * SvO2
        else:
            #if updatedVar == 'Hb' or updatedVar == 'SvO2' or updatedVar == 'CaO2' or updatedVar == 'CavO2':
            if updatedVar:
                Hb = details['Hb']
                HbUnit = details['Hb_unit']

                if unit == 'ml/l':
                    if HbUnit == 'g/dl': # -> g/l
                        Hb = Hb * 10
                elif unit == 'ml/dl':
                    if HbUnit == 'g/l': # -> g/dl
                        Hb = Hb / 10
                
                return 1.34 * Hb * SvO2
                """ elif updatedVar == 'CaO2' or updatedVar == 'CavO2':
                CaO2Unit = details['CaO2_unit']
                CavO2Unit = details['CavO2_unit']
                
                if unit == 'ml/l':
                    if CaO2Unit == 'ml/dl': # -> ml/l
                        CaO2 = CaO2 * 10
                    if CavO2Unit == 'ml/dl': # -> ml/l
                        CavO2 = CavO2 * 10
                elif unit == 'ml/dl':
                    if CaO2Unit == 'ml/l': # -> ml/dl
                        CaO2 = CaO2 / 10
                    if CavO2Unit == 'ml/l': # -> ml/dl
                        CavO2 = CavO2 / 10

                return CaO2-CavO2 """
            else:
                return CvO2 
    
    def formatSvO2(self, w, details, CavO2, CaO2, Hb, updatedVar):
        SvO2 = float(details['SvO2'])

        if SvO2 == 0:
            w.getDetails().setMC('SvO2_MC', 1)
            CaO2Unit = details['CaO2_unit']
            CavO2Unit = details['CavO2_unit']
            HbUnit = details['Hb_unit']

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
            #if updatedVar == 'CaO2' or updatedVar == 'CavO2' or updatedVar == 'Hb':
            if updatedVar:
                CaO2Unit = details['CaO2_unit']
                CavO2Unit = details['CavO2_unit']
                HbUnit = details['Hb_unit']

                if CaO2Unit == 'ml/l': # -> ml/dl
                    CaO2 = CaO2 / 10
                if CavO2Unit == 'ml/l': # -> ml/dl
                    CavO2 = CavO2 / 10
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
                
                # SvO2 = (CaO2 - C(a-v)O2) x 100 / 1,34 / [Hb]
                return (CaO2 - CavO2) / 1.34 / Hb
            else:
                return SvO2

        """ if SvO2 == 0:
            w.getDetails().setMC('SvO2_MC', 1)
            CvO2Unit = details['CvO2_unit']
            HbUnit = details['Hb_unit']

            if CvO2Unit == 'ml/l': # -> ml/dl
                CvO2 = CvO2 / 10
            if HbUnit == 'g/l': # -> g/dl
                Hb = Hb / 10

            return CvO2 / 1.34 / Hb
        else:
            if updatedVar == 'CvO2' or updatedVar == 'Hb':
                CvO2Unit = details['CvO2_unit']
                HbUnit = details['Hb_unit']

                if CvO2Unit == 'ml/l': # -> ml/dl
                    CvO2 = CvO2 / 10
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10

                return CvO2 / 1.34 / Hb
            else:
                return SvO2 """

    def formatQaO2(self, w, details, Q, CaO2, updatedVar):
        QO2 = float(details['QaO2'])
        unit = details['QaO2_unit']
        QUnit = details['Q_unit']
        CaO2Unit = details['CaO2_unit']

        if QO2 == 0:
            w.getDetails().setMC('QaO2_MC', 1)
        
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

        w.getDetails().setMC('PvO2_MC', 1)
        return np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))

        """ if PvO2 == 0:
            w.getDetails().setMC('PvO2_MC', 1)
            return np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        else:
            return PvO2 """

    def phTempCorrection(self, pH0, pH, T0, T, PvO2_calc):
        lnPvO2 = np.log(PvO2_calc)
        if pH != pH0:
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

    def calc(self, w, details, updatedVar = None, VO2Lock = None):
        validValues = True
        print(f'Details from calc: {details}')
        Q = self.formatQ(w, details, updatedVar)
        VO2 = self.formatVO2(w, details, Q, updatedVar, VO2Lock)
        Hb = self.formatHb(details, updatedVar)
        SaO2 = float(details['SaO2'])

        # print(f'Q {Q} - VO2 {VO2} - Hb {Hb} - SaO2 {SaO2}')

        CaO2 = self.formatCaO2(w, details, Hb, SaO2/100, updatedVar)
        CavO2 = self.formatCavO2(w, details, VO2, Q, updatedVar)
        SvO2_calc = self.formatSvO2(w, details, CavO2, CaO2, Hb, updatedVar)
        CvO2 = self.formatCvO2(w, details, Hb, CaO2, CavO2, SvO2_calc, updatedVar)
        QaO2 = self.formatQaO2(w, details, Q, CaO2, updatedVar)

        # print(f'CavO2 {CavO2} - CaO2 {CaO2} - CvO2 {CvO2} - SvO2_calc {SvO2_calc} - QaO2 {QaO2}')

        # Calculate diffusion DO2
        a = 11700 * np.float_power( ( np.float_power(SvO2_calc,-1) - 1 ), -1 )
        b = np.float_power( 50**3 + np.float_power(a,2), 0.5 )
        PvO2_calc = self.formatPvO2(w, details, a, b) # mmHg
        #print(f'WTF2: {a}, {b}, {PvO2_calc}')

        if PvO2_calc < 0:
            print('PvO2 negative')
            validValues = False

        # pH + temp correction
        pH = float(details['pH @ rest'])
        pH0 = float(details['pH\u209A\u2091\u2090\u2096'])
        T = self.formatT(details, 'Tc\u209A\u2091\u2090\u2096')
        T0 = self.formatT(details, 'Tc @ rest')
        PvO2_calc = self.phTempCorrection(pH0, pH, T0, T, PvO2_calc)

        DO2 = self.solveDO2(w, details, VO2, PvO2_calc)

        #print(f'DO2 {DO2}')

        # Fick's law - Diffusion line 
        # VO2 = DO2 * 2 * PvO2

        PvO2 = np.arange(0,100,1)
        y = 2* DO2 * PvO2

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

        if details['Hb_unit'] == 'g/l': # -> g/dl
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
                print('TYPEERROR IN CALC')
                validValues = False
                return validValues

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * Hb * ( SaO2/ 100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)

        if details['Hb_unit'] == 'g/l': # g/dl -> g/l
            Hb = Hb * 10

        w.getDetails().setCalcResults(y, y2, xi, yi, VO2, Q, Hb, SaO2, CaO2, SvO2_calc, CvO2, CavO2, QaO2, T0, T, pH0, pH, PvO2_calc, DO2)
        #print(f'UPDATED DETAILS: {w.getDetails().getWorkLoadDetails()}')
        return validValues

class PlotTab(object):
    def __init__(self, parentFrame, workLoads):
        self.plot = None
        self.loadTabs = []
        self.parentFrame = parentFrame
        self.activeTest = app.getActiveTest()
        self.activeTestId = self.activeTest.id
        self.workLoads = workLoads # Workload objects
        
    def createPlotTab(self):
        # Create tab for test
        self.tabFrame = ttk.Frame(self.parentFrame)
        self.tabFrame.pack(expand=TRUE)

        # Plot canvasframe
        self.canvasFrame = ttk.Frame(self.tabFrame)
        self.canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        # Figure instructions
        ttk.Label(self.canvasFrame, text='Right click - hide all | Middle click - show all', anchor='n').pack(fill=X)

        self.canvas = self.createPlot() # FigureCanvasTkAgg
        self.canvasTk = self.canvas.get_tk_widget() # Tkinter canvas
        self.canvasTk.pack(fill=BOTH, expand=1)
        self.canvas.draw()

        # Custom figure tools container
        self.toolbarContainer = ttk.Frame(self.canvasFrame)
        self.toolbarContainer.pack(fill=BOTH, expand=1)

        # Figure toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarContainer, pack_toolbar=False)
        self.toolbar.pack(fill=X)
        
        # Custom toolbar
        self.toolbarWrapper = ttk.Frame(self.toolbarContainer)
        self.toolbarWrapper.pack(side=LEFT, anchor='nw')
        ttk.Label(self.toolbarWrapper, text='Set Y-axis max. value').grid(column=0, row=0)

        # Set y limit
        self.yValue = StringVar(self.toolbarWrapper, value=self.plot[1].get_ylim()[1])
        self.yEntry = ttk.Entry(self.toolbarWrapper, textvariable=self.yValue)
        self.yEntry.grid(column=0, row=1)
        self.yValue.trace('w', self.updateY)
        ttk.Button(self.toolbarWrapper, text='Set', command=lambda: self.updateFig()).grid(column=1, row=1)

        self.toolbarWrapper.grid_columnconfigure(2, minsize=25)

        # Set step size
        ttk.Label(self.toolbarWrapper, text='Tick count in y-axis:').grid(column=3, row=0, columnspan=2)
        ttk.Button(self.toolbarWrapper, text='+', width=3 ,command=lambda: self.incTicks()).grid(column=3, row=1)
        ttk.Button(self.toolbarWrapper, text='-', width=3, command=lambda: self.decTicks()).grid(column=4, row=1)
        
        self.toolbarWrapper.grid_columnconfigure(5, minsize=25)

        # Hide legend button
        ttk.Button(self.toolbarWrapper, text='Hide legend', command=lambda: self.hideLegend()).grid(column=6, row=1)
        ttk.Button(self.toolbarWrapper, text='DETAILS', command=lambda: print(self.workLoads[0].getDetails().getWorkLoadDetails())).grid(column=7, row=1)

        # Create loads notebook frame and loadnotebook
        self.loadNotebookFrame = ttk.Frame(self.tabFrame)
        self.loadNotebookFrame.pack(side=RIGHT, fill=Y)

        self.loadNotebook = ttk.Notebook(self.loadNotebookFrame)
        self.loadNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tabs for loads
        for i, w in enumerate(self.workLoads):
            loadTabObject = PlotLoadTab(self, i, self.activeTestId, w, self.loadNotebook, self.plot)
            loadTab = loadTabObject.createLoadTab()
            self.loadNotebook.add(loadTab, text=w.getName())
            self.loadTabs.append(loadTabObject)

        return self.tabFrame

    def hideLegend(self):
        legend = self.plot[1].get_legend()
        vis = legend.get_visible()
        if vis:
            legend.set_visible(False)
        else:
            legend.set_visible(True)
        self.plot[0].canvas.draw()

    def incTicks(self):
        yticks = self.plot[1].get_yticks()
        n = len(yticks)+1
        self.plot[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
        self.plot[0].canvas.draw()

    def decTicks(self):
        yticks = self.plot[1].get_yticks()
        n = len(yticks)-1
        self.plot[1].yaxis.set_major_locator(plt.LinearLocator(numticks=n))
        self.plot[0].canvas.draw()

    def updateY(self, name, index, mode):
        pass
    
    def updateFig(self):
        limit = self.yValue.get()
        self.plot[1].set_ylim(top=float(limit))
        self.plot[0].canvas.draw()

    def createPlot(self):
        PvO2 = np.arange(0,100,1)
        self.plot = plt.subplots()
        self.fig, self.ax = self.plot
        
        #print()

        self.fig.set_figheight(3)
        self.fig.set_figwidth(3)

        #print(f'CANVAS: {self.canvasFrame.winfo_reqwidth()},{self.canvasFrame.winfo_reqheight()}')
        #print(f'FIG: {self.fig.get_figwidth()},{self.fig.get_figheight()}')
        #print(f'NOTEBOOK: {self.parentFrame.winfo_reqwidth()}, {self.parentFrame.winfo_reqheight()}')
        #print(f'TOOLBAR: {self.toolbarContainer.winfo_reqwidth()},{self.toolbarContainer.winfo_reqheight()}')
        self.ax.set_title('O2 Pathway')
        self.ax.set_ylabel('VO\u2082')
        self.ax.set_xlabel('PvO\u2082 (mmHg)')
        """ if self.workLoads[0].getDetails().getWorkLoadDetails()['VO2_unit'] == 'l/min':
            self.ax.set_ylim(top=5.0, bottom=0)
        else:
            self.ax.set_ylim(top=5000, bottom=0) """
        self.ax.set_ylim(top=5000, bottom=0)
        self.ax.set_xlim(left=0, right=100)
        self.handles = []

        for i, w in enumerate(self.workLoads):
            coords = w.getDetails().getCoords()
            y = coords['y']
            y2 = coords['y2']
            xi = coords['xi']
            yi = coords['yi']

            line, = self.ax.plot(PvO2, y, lw=2, color=f'C{i}', label=w.name)
            curve, = self.ax.plot(PvO2, y2, lw=2, color=f'C{i}', label=w.name)
            dot, = self.ax.plot(xi, yi, 'o', color='red', label=w.name)

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
        
        def rescale(e):
            print(f'JEEP, {e}, {e.width}')
            #print(f'CANVAS: {self.canvasFrame.winfo_reqwidth()},{self.canvasFrame.winfo_reqheight()}')
            #print(f'FIG: {self.fig.get_figwidth()},{self.fig.get_figheight()}')
            #print(f'NOTEBOOK: {self.parentFrame.winfo_reqwidth()}, {self.parentFrame.winfo_reqheight()}')
            #print(f'TOOLBAR: {self.toolbarContainer.winfo_reqwidth()},{self.toolbarContainer.winfo_reqheight()}')
            canvasHeight = e.height
            toolbarHeight = self.toolbarContainer.winfo_reqheight()
            newHeight = canvasHeight-toolbarHeight-10
            self.canvas.get_tk_widget().configure(height=100)
            evt = Event()
            evt.width=e.width
            evt.height=100 #newHeight
            evt.state = 'rescaled'
            evt.char = None
            evt.delta = None
            evt.type = 22
            print(evt)
            self.canvas.resize(evt)
            self.canvasFrame.configure(height=100)#self.fig.get_figheight())

        self.canvas = FigureCanvasTkAgg(self.fig, self.canvasFrame)
        #self.canvas.get_tk_widget().bind('<Configure>', rescale)

        return self.canvas

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
        self.rowElements = []

    def createLoadTab(self):
        self.loadtab = ttk.Frame(self.parentNotebook)
        self.loadtab.pack()

        # Details frame
        self.loadDetails = ttk.Frame(self.loadtab)
        self.loadDetails.grid()
        
        ttk.Label(self.loadDetails, text=f'Load: {self.details["Load"]}').grid(column=0, row=0)
        ttk.Label(self.loadDetails, text='Value').grid(column=1, row=0)
        ttk.Label(self.loadDetails, text='Unit').grid(column=2, row=0)
        ttk.Label(self.loadDetails, text='Meas.').grid(column=3, row=0)
        ttk.Label(self.loadDetails, text='Calc.').grid(column=4, row=0)

        """ # HR
        hrValue = self.details['HR']
        self.hrRow = LoadTabRow(self, self.loadDetails, 'HR', hrValue, self.index, self.testId, 1, (40,220), self.workLoad)
        self.rowElements.append(self.hrRow)

        # SV
        svValue = float(self.details['Sv'])
        if self.details['Sv_unit'] == 'ml':
            self.svRow = LoadTabRow(self, self.loadDetails, 'Sv', svValue, self.index, self.testId, 2, (0, 1000), self.workLoad)
        else:
            self.svRow = LoadTabRow(self, self.loadDetails, 'Sv', svValue, self.index, self.testId, 2, (0, 1), self.workLoad)
        self.rowElements.append(self.svRow) """

        # VO2
        vo2Value = float(self.details['VO2'])
        if self.details['VO2_unit'] == 'l/min':
            self.vo2Row = LoadTabRow(self, self.loadDetails, 'VO2', vo2Value, self.index, self.testId, 3, (0,10), self.workLoad)
        else:
            self.vo2Row = LoadTabRow(self, self.loadDetails, 'VO2', vo2Value, self.index, self.testId, 3, (0,10000), self.workLoad)
        self.rowElements.append(self.vo2Row)

        # Q
        qValue = float(self.details['Q'])
        if self.details['Q_unit'] == 'l/min':
            self.qRow = LoadTabRow(self, self.loadDetails, 'Q', qValue, self.index, self.testId, 4, (0,25), self.workLoad)
        else:
            self.qRow = LoadTabRow(self, self.loadDetails, 'Q', qValue, self.index, self.testId, 4, (0,25000), self.workLoad)
        self.rowElements.append(self.qRow)

        # Hb
        hbValue = float(self.details['Hb'])
        if self.details['Hb_unit'] == 'g/dl':
            self.hbRow = LoadTabRow(self, self.loadDetails, 'Hb', hbValue, self.index, self.testId, 5, (0,20), self.workLoad)
        else:
            hbValue = hbValue
            self.hbRow = LoadTabRow(self, self.loadDetails, 'Hb', hbValue, self.index, self.testId, 5, (0,200), self.workLoad)
        self.rowElements.append(self.hbRow)

        # SaO2
        sao2Value = float(self.details['SaO2'])
        self.sao2Row = LoadTabRow(self, self.loadDetails, 'SaO2', sao2Value, self.index, self.testId, 6, (80,100), self.workLoad)
        self.rowElements.append(self.sao2Row)

        # SvO2
        svo2Value = float(self.details['SvO2']) * 100
        self.svo2Row = LoadTabRow(self, self.loadDetails, 'SvO2', svo2Value, self.index, self.testId, 7, (0,20), self.workLoad)
        self.rowElements.append(self.svo2Row)

        # CaO2
        cao2Value = float(self.details['CaO2'])
        if self.details['CaO2_unit'] == 'ml/dl':
            self.cao2Row = LoadTabRow(self, self.loadDetails, 'CaO2', cao2Value, self.index, self.testId, 8, (0,100), self.workLoad)
        else:
            self.cao2Row = LoadTabRow(self, self.loadDetails, 'CaO2', cao2Value, self.index, self.testId, 8, (0,1000), self.workLoad)
        self.rowElements.append(self.cao2Row)

        # CvO2
        cvo2Value = float(self.details['CvO2'])
        if self.details['CvO2_unit'] == 'ml/dl':
            self.cvo2Row = LoadTabRow(self, self.loadDetails, 'CvO2', cvo2Value, self.index, self.testId, 9, (0,100), self.workLoad)
        else:
            self.cvo2Row = LoadTabRow(self, self.loadDetails, 'CvO2', cvo2Value, self.index, self.testId, 9, (0,1000), self.workLoad)
        self.rowElements.append(self.cvo2Row)
        
        # CavO2
        cavo2Value = float(self.details['CavO2'])
        if self.details['CavO2_unit'] == 'ml/dl':
            self.cavo2Row = LoadTabRow(self, self.loadDetails, 'CavO2', cavo2Value, self.index, self.testId, 10, (0,100), self.workLoad)
        else:
            self.cavo2Row = LoadTabRow(self, self.loadDetails, 'CavO2', cavo2Value, self.index, self.testId, 10, (0,1000), self.workLoad)
        self.rowElements.append(self.cavo2Row)

        # PvO2
        pvo2Value = self.details['PvO2']
        self.pvo2Row = LoadTabRow(self, self.loadDetails, 'PvO2', pvo2Value, self.index, self.testId, 11, (0,100), self.workLoad)
        self.rowElements.append(self.pvo2Row)

        # QaO2
        qao2Value = float(self.details['QaO2'])
        if self.details['QaO2_unit'] == 'ml/min':
            self.qao2Row = LoadTabRow(self, self.loadDetails, 'QaO2', qao2Value, self.index, self.testId, 12, (0,10000), self.workLoad)
        else:
            self.qao2Row = LoadTabRow(self, self.loadDetails, 'QaO2', qao2Value, self.index, self.testId, 12, (0,10), self.workLoad)
        self.rowElements.append(self.qao2Row)

        # DO2
        do2Value = self.details['DO2']
        self.do2Row = LoadTabRow(self, self.loadDetails, 'DO2', do2Value, self.index, self.testId, 13, (0,100), self.workLoad)
        self.rowElements.append(self.do2Row)

        # T
        tValue = float(self.details['Tc\u209A\u2091\u2090\u2096'])
        if self.details['Tc\u209A\u2091\u2090\u2096_unit'] == 'F':
            tValue = (tValue - 32) / 1.8
            self.tRow = LoadTabRow(self, self.loadDetails, 'Tc\u209A\u2091\u2090\u2096', tValue, self.index, self.testId, 14, (95,110), self.workLoad)
        elif self.details['Tc\u209A\u2091\u2090\u2096_unit'] == 'K':
            tValue = tValue - 273.15
            self.tRow = LoadTabRow(self, self.loadDetails, 'Tc\u209A\u2091\u2090\u2096', tValue, self.index, self.testId, 14, (300,320), self.workLoad)
        else:
            self.tRow = LoadTabRow(self, self.loadDetails, 'Tc\u209A\u2091\u2090\u2096', tValue, self.index, self.testId, 14, (35,42), self.workLoad)
        self.rowElements.append(self.tRow)

        # pH
        phValue = self.details['pH\u209A\u2091\u2090\u2096']
        self.phRow = LoadTabRow(self, self.loadDetails, 'pH\u209A\u2091\u2090\u2096', phValue, self.index, self.testId, 15, (0,14), self.workLoad)
        self.rowElements.append(self.phRow)

        # Plot options
        optionsFrame = ttk.Frame(self.loadtab)
        optionsFrame.grid(column=0, columnspan=5, row=16)
        
        # Plot options
        PlotOptions(optionsFrame, self.plot, self.index)

        return self.loadtab

    """ def updatePlot(self, label, val=None, name=None, index=None, mode=None, loadtab=None):
        print('UPDATING PLOT')
        validValues = True
        

        validValues = app.getPlottingPanel().calc(
            self.workLoad,
            self.workLoad.getDetails().getWorkLoadDetails(),
            label,
            self.vo2Row.VO2Lock
        )

        if validValues == True:

            coords = self.workLoad.getDetails().getCoords()
                
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
            mappedLines[self.index][0].set_ydata(coords['y'])
            mappedLines[self.index][1].set_ydata(coords['y2'])
            mappedLines[self.index][2].set_ydata(coords['yi'])
            mappedLines[self.index][2].set_xdata(coords['xi'])

            self.parentPlotTab.fig.canvas.draw()
            self.parentPlotTab.fig.canvas.flush_events()

            self.updateDetails()

            # Update objects plot for exporting
            self.plot = (self.parentPlotTab.fig, self.parentPlotTab.ax)
        else:
            notification.create('error', 'Unable to compute with given values. Check values', 5000)
    """

    def updateDetails(self):
        self.details = self.workLoad.getDetails().getWorkLoadDetails()
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
        ttk.Label(self.plotOptions, text='Change line color').grid(column=3, row=0)
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
        self.lineColorMenuButton.grid(column=4, row=0)

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

class LoadTabRow(object):
    def __init__(self, parenObject, parentFrame, label, value, index, id, row, scale, workLoad):
        self.parentObject = parenObject
        self.parent = parentFrame
        self.label = label
        self.value = value
        self.index = index
        self.id = id
        self.row = row
        self.scale = scale
        self.workLoad = workLoad.getDetails()
        self.details = self.workLoad.getWorkLoadDetails()
        self.VO2Lock = False

        #print(f'VALUE: {self.value}')
        self.var = DoubleVar(self.parent, value=f'{"{0:.1f}".format(float(self.value))}')

        # Label
        if '2' in self.label:
            label_subscripted = self.label.replace('2', '\u2082')
            ttk.Label(self.parent, text=label_subscripted).grid(column=0, row=row)
        else:
            ttk.Label(self.parent, text=self.label).grid(column=0, row=row)
        
        # Slider
        # self.slider = ttk.Scale(self.parent, from_=self.scale[0], to=self.scale[1], command=lambda e: formatSlider(e),  orient=HORIZONTAL, value=self.value, variable=self.var)
        # self.slider.grid(column=1, row=row)
        # Entry
        self.entry = ttk.Label(self.parent, textvariable=self.var, width=7, anchor='center')
        self.entry.grid(column=1, row=row)

        """ if self.label == 'VO2':
                self.lockBtn = ttk.Button(self.parent, text='Lock', width=4, command=lambda: handleLock())
                self.lockBtn.grid(column=3, row=row)

            def handleLock():
                s = ttk.Style()
                s.configure('lockBtn.TButton', background="grey")
                if self.VO2Lock == True:
                    self.VO2Lock = False
                    self.lockBtn.config(style='')
                else:
                    self.lockBtn.config(style='lockBtn.TButton')
                    self.VO2Lock = True

                print(f'LOCK: {self.VO2Lock}') """

        """ def formatSlider(e):
                self.entry.delete(0,END)
                self.entry.insert(0, f'{"{0:.1f}".format(float(e))}')

            def sliderReleased(e):
                self.workLoad.setValue(self.label, self.var.get())
                self.parentObject.updatePlot(self.label) 

            def entryFocusOut(e):
                if self.initValue != self.var.get():
                    self.workLoad.setValue(self.label, self.var.get())
                    self.parentObject.updatePlot(self.label)

            def entryFocusIn(e):
                self.initValue = self.var.get() """

        # self.entry.bind('<FocusIn>', entryFocusIn)
        # self.entry.bind('<FocusOut>', entryFocusOut)
        # self.slider.bind('<ButtonRelease-1>', sliderReleased)

        # Unit entry
        if self.label != 'pH\u209A\u2091\u2090\u2096':
            menuButton = ttk.Menubutton(self.parent)
            menuButton.config(text=self.details[f'{self.label}_unit'])
            tempMenu = Menu(menuButton, tearoff=False)
            units = app.settings.getUnits()[f'{self.label}_units']

            for i, u in enumerate(units):
                LoadMenuElem(self, tempMenu, menuButton, self.var, u, i, units, f'{self.label}', self.workLoad)
            
            menuButton['menu']=tempMenu
            menuButton.grid(column=2, row=row)
            
        # M/C Radiobuttons
        self.mcVar = IntVar(value=self.details[f'{self.label}_MC'])

        self.radio1 = ttk.Radiobutton(self.parent, value=0, variable=self.mcVar)
        self.radio1.grid(column=3, row=row)

        self.radio2 = ttk.Radiobutton(self.parent, value=1, variable=self.mcVar)
        self.radio2.grid(column=4, row=row)
        self.mcVar.trace('w', self.updateMc)

        

    def updateMc(self, name, index, mode):
        self.workLoad.setMC(f'{self.label}_MC', self.mcVar.get())

    def updateEntryAndScale(self, unit):
        if unit == 'ml/min': # l/min -> ml/min
            self.workLoad.setValue(self.label, self.var.get()*1000)
            self.var.set(self.var.get()*1000)
            # self.slider.config(to=10000)
        
        elif unit == 'l/min': # ml/min -> l/min
            self.workLoad.setValue(self.label, self.var.get()/1000)
            self.var.set(self.var.get()/1000)
            # self.slider.config(to=10)

        elif unit == 'g/l': # g/dl -> g/l
            self.workLoad.setValue(self.label, self.var.get()*10)
            self.var.set(self.var.get()*10)
            # self.slider.config(to=self.scale[1]*10)

        elif unit == 'g/dl': # g/l -> g/dl
            self.workLoad.setValue(self.label, self.var.get()/10)
            self.var.set(self.var.get()/10)
            # self.slider.config(to=self.scale[1]/10)

        elif unit == 'ml/l': # ml/dl -> ml/l
            self.workLoad.setValue(self.label, self.var.get()*10)
            self.var.set(self.var.get()*10)
            # self.slider.config(to=self.scale[1])

        elif unit == 'ml/dl': # ml/l -> ml/dl
            self.workLoad.setValue(self.label, self.var.get()/10)
            self.var.set(self.var.get()/10)
            # self.slider.config(to=self.scale[1]/10)
        
        elif unit == 'l': #ml -> l
            self.workLoad.setValue(self.label, self.var.get()/1000)
            self.var.set(self.var.get()/1000)
            # self.slider.config(to=1)

        elif unit == 'ml': #l -> ml
            self.workLoad.setValue(self.label, self.var.get()*1000)
            self.var.set(self.var.get()*1000)
            # self.slider.config(to=1000)

        elif unit == 'F': # C -> F
            self.workLoad.setValue(self.label, self.var.get() * 1.8 + 32)
            self.var.set(self.var.get() * 1.8 + 32)
            # self.slider.config(from_=95, to=110)

        elif unit == 'K': # C -> K
            self.workLoad.setValue(self.label, self.var.get() + 273.15)
            self.var.set(self.var.get() + 273.15)
            # self.slider.config(from_=300, to=320)
        
        elif unit == '\N{DEGREE SIGN}C': # K/F -> C
            if self.var.get() > 94 and self.var.get() < 111: # F
                self.workLoad.setValue(self.label, (self.var.get() - 32) / 1.8)
                self.var.set((self.var.get() - 32) / 1.8)
            else: # K
                self.workLoad.setValue(self.label, self.var.get() - 273.15)
                self.var.set(self.var.get() - 273.15)
            
            # self.slider.config(from_=35, to=42)

    def getValue(self):
        return self.var.get()
    
    def updateText(self, details):
        #self.valUnit.config(text=f'{"{0:.2f}".format(details[self.label]) } {details[f"{self.label}_unit"]}')
        self.entry.delete(0,END)
        self.entry.insert(0, f'{"{0:.1f}".format(float(details[self.label]))}')

class LoadMenuElem(object):
    def __init__(self, parentObject, menu, menuButton, var, label, index, unitElems, name, workload):
        self.parentObject = parentObject
        self.menu = menu
        self.menuButton = menuButton
        self.var = var
        self.label = label
        self.index = index
        self.unitElems = unitElems
        self.name = name
        self.workLoad = workload

        self.menu.add_command(label=f'{self.label}', command=lambda: self.updateValue())

    def updateValue(self):
        self.menuButton.config(text=self.unitElems[self.index])
        self.parentObject.updateEntryAndScale(self.unitElems[self.index])

        self.workLoad.setUnit(f'{self.name}_unit', self.unitElems[self.index])
