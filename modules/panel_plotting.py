from tkinter import *
from tkinter import ttk
from objects.app import app
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

    def plot(self):
        self.workLoads = app.getActiveTest().getWorkLoads()

        self.container.destroy()
        self.container = ttk.Frame(self.mainFrame, style='plottingPanel.TFrame')
        self.container.pack(fill=BOTH, expand=TRUE)

        # Plots notebook
        plotNotebook = ttk.Notebook(self.container)
        plotNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tab for test
        tab = ttk.Frame(plotNotebook, width=300, height=200)
        tab.pack(expand=TRUE)

        # Plot canvasframe
        self.canvasFrame = ttk.Frame(tab)
        self.canvasFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

        # Plot data
        self.plotter()

        # Loads notebook frame
        loadNotebookFrame = ttk.Frame(tab)
        loadNotebookFrame.pack(side=RIGHT, expand=TRUE, fill=BOTH)
        
        # Load notebook
        loadNotebook = ttk.Notebook(loadNotebookFrame)
        loadNotebook.pack(expand=TRUE, fill=BOTH)

        # Create tabs for loads
        for w in self.workLoads:
            #print(w.getWorkLoadDetails())
            loadtab = ttk.Frame(loadNotebook)
            loadtab.pack(expand=TRUE, fill=BOTH)
            loadNotebook.add(loadtab, text=f'Load{w.id+1}')
        
        plotNotebook.add(tab, text=app.getActiveTest().id)

    def plotter(self):
        
        PvO2 = np.arange(0,100,1)
        self.fig, ax = plt.subplots()
        self.handles = []

        for i, w in enumerate(self.workLoads):
            details = w.getWorkLoadDetails()
            
            #y, y2, xi, yi, QO2, DO2 = self.calc(float(details['Q']), float(details['VO2']), float(details['Hb']), float(details['SaO2']))
            y, y2, xi, yi, QO2, DO2 = self.calc(float(14+i), float(1.0+i), float(13.0+i), float(99.0))

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
        canvas = FigureCanvasTkAgg(self.fig, self.canvasFrame)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.canvasFrame)
        toolbar.update()

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

    def calc(self, Q, vo2, hb, SaO2):
        #Q = hr * sv / 1000

        # Computated variables
        Ca_vO2 = vo2 / Q * 100
        print(f"Ca_vO2: {Ca_vO2}")

        CaO2 = 1.34 * hb * SaO2/100
        print(f"CaO2: {CaO2}")

        CvO2 = CaO2-Ca_vO2
        print(f"CvO2: {CvO2}")

        SvO2 = CvO2 / 1.34 / hb
        print(f"SvO2: {SvO2}")

        # Convection
        QO2 = Q * CaO2 * 10 #ml/min
        print(f"QO2: {QO2}")

        # Calculate diffusion DO2
        a = 11700 * np.float_power( ( np.float_power(SvO2,-1) - 1 ), -1 )
        print(f'A: {a}')

        b = np.float_power( 50**3 + np.float_power(a,2) , 0.5 )
        print(f'B: {b}')

        PvO2 = np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        print(f'PvO2: {PvO2}')

        DO2 = vo2 / 2 / PvO2 * 1000
        print(f"DO2:{DO2}")

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

            yDiff.append( (float(y_temp)-float(y2_temp)) )

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * hb * ( SaO2/100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)
        
        return y, y2, xi, yi, QO2, DO2