from tkinter import *
from tkinter import ttk
from objects.app import app
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import fitz
import math

class Help():
    def __init__(self):
        self.window = Toplevel()
        self.window.title('Help')
        self.window.geometry('750x500')

        windowX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/2)
        windowY = app.root.winfo_rooty() + (app.root.winfo_reqheight()/10)
        self.window.geometry("+%d+%d" % ( windowX, windowY ))

        # Left panel
        self.leftPanel = ttk.Frame(self.window)
        self.leftPanel.pack(side=LEFT, fill=Y)

        self.progressionList = Listbox(self.leftPanel, width=25)
        self.progressionList.insert('end', 'Layout')
        self.progressionList.insert('end', 'Project panel')
        self.progressionList.insert('end', 'Subject panel')
        self.progressionList.insert('end', 'Test panel')
        self.progressionList.insert('end', 'Details panel')
        self.progressionList.insert('end', 'Plotting panel')
        self.progressionList.insert('end', 'Data import')
        self.progressionList.insert('end', 'Data export')
        self.progressionList.insert('end', 'Settings')
        self.progressionList.insert('end', 'Equations')
        self.progressionList.insert('end', 'PDF test')

        self.progressionList.pack(expand=1, fill=BOTH)
        self.progressionList.bind( '<<ListboxSelect>>', lambda e: self.handleListBoxSelect(e) )

        # Right panel
        self.rightPanel = ttk.Frame(self.window)
        self.rightPanel.pack(side=RIGHT, fill=BOTH, expand=True)
        self.content = ttk.Frame(self.rightPanel)
        self.content.pack(fill=BOTH, expand=True)

        self.window.mainloop()

    def handleListBoxSelect(self, e):
        index = self.progressionList.curselection()[0]
        for c in self.content.winfo_children():
            c.destroy()

        wrapper = ttk.Frame(self.content)
        wrapper.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(wrapper)
            
        scrollbar = Scrollbar(wrapper)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=scrollbar.set)
        self.canvas.pack(fill=BOTH, expand=True)

        self.content.bind('<Configure>', self.scale)
        self.canvas.bind('<1>', lambda e: self.zoom(zoomMode=1))
        self.canvas.bind('<2>', lambda e: self.zoom(zoomMode=2))
        self.canvas.bind('<3>', lambda e: self.zoom(zoomMode=3))
        
        if index == 0: # Layout
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""The tool is constructed from three main modules: side module, details module and plotting module.
                
Side module controls the project, subject and test instances. You can toggle the visibility of the side module in the View-menu.
                 
Details module is located in the upper part of the window. Details module contains information of created projects, tests and environmental conditions. O\u2082 pathway plots are calculated with the values given in the details module. You can toggle the visibility of the details module in the View-menu.
                
Plotting module is the main module and takes up the space under details module. Plotting module holds created plots in separate tabs, which you can cycle through and close if needed. Plotting module holds also the calculated details of tests and their submaximal loads/workrates.
                """)
            txt.configure(state='disabled')
        if index == 1: # Project panel
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Projects panel lists all the projects that are imported to or created in the tool. 
                
Add-button creates a new project and sets it as an active project.

Edit-button enables you to set a different name for the project. Default name is "Project".

Del-button enables you to delete the project and its every subject and their test from the tool.

Import-button enables you to import project data from a file. More information about the importing tool can be found in the "Data import"-section.

Plot mean -button can be used to plot mean/standard deviation or mean/interquartile range figure from the whole project. Once the button is pressed, a pop-up window appears, where you can select which figure you want to plot.
                """)
            txt.configure(state='disabled')
        if index == 2: # Subject panel
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
                """Subjects panel lists all the subjects under the active project that are imported to or created in the tool. 
                
Add-button creates a new subject and sets it as an active subject.

Edit-button enables you to set a different name for the subject. Default name is "Subject" + automaticly created index number.

Del-button enables you to delete the selected subject and its every test from the tool.

Import-button enables you to import subject data from a file. More information about the importing tool can be found in the "Data import"-section.

Compare-button enables you to select at least two subjects to be plotted in the same figure. You can select subjects by holding down the CTRL- or SHIFT-button. Once compare-button is pressed, a small options pop-up window appears where you can select the subject's tests for comparison. After selection the selected tests' details are shown in the details module, where they can be modified and eventually plotted.

Plot mean -button can be used to plot mean/standard deviation or mean/interquartile range figure from the selected subject(s) tests. Once the button is pressed, a pop-up window appears, where you can select which figure you want to plot. Once the method is selected, a new tab is created in the plotting module showing the results of calculations and the figure.
                """)
            txt.configure(state='disabled')
            txt.configure(state='disabled')
        if index == 3: # Test panel
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Tests panel lists all tests under the active subject that are imported to or created in the tool. 

When a test is selected from the list it is set to active test and its details are shown in the details module.
                
Add-button creates a new test and sets it as an active test. Once pressed a new test is visible in the tests panel list and in the details module with default settings. 

Edit-button enables you to set a different name for the test. Default name is an automaticly created id.

Del-button enables you to delete the selected test from the tool.

Import-button enables you to import subject data from a file. More information about the importing tool can be found in the "Data import"-section.

Compare-button enables you to select at least two tests to be plotted in the same figure. You can select tests by holding down the CTRL- or SHIFT-button. Once compare-button is pressed, a small options pop-up window appears where you can select the method for comparison. After selection the selected tests' details are shown in the details module, where they can be modified and eventually plotted.

Plot mean -button can be used to plot mean/standard deviation or mean/interquartile range figure from the selected test(s). Once the button is pressed, a pop-up window appears, where you can select which figure you want to plot. Once the method is selected, a new tab is created in the plotting module showing the results of calculations and the figure.
                """)
            txt.configure(state='disabled')
        if index == 4: # Details panel
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Details module shows details of the test and project that is set as active in the tool. 

Details module is constructed of project details -module, test details -module and environmental details -module.

Project details -module lists information about the active project. Details are not updated automaticly (only subject count is), but you can refresh project details by clicking the "Calculate"-button. Once pressed the tool calculated mean, minimum and maximum values of VO\u2082, QaO\u2082 and DO\u2082 from the active project's data.

Test details -module shows information about the test. Main information is the load tabs, which are imported from a file or input by hand. Every parameter's value and unit is changable and every parameter can be marked as calculated or measured value. New loads can be created and modified with buttons "Add" and "Edit" under the parameter list. Load tab can be closed by clicking the small "x" in the tab. The units and values for pH and core temperature are loaded from default settings, which can be adjusted. More information on how to change default settings can be found from the "Default Settings"-section. If the peak values for core temperature and pH is set in the default settings, the change is divided linearily between loads automaticly.

Environmental details -module shows information about the conditions the test has been performed in. Unfortunately these parameters are NOT taken into account in the recent version of the tool. However, the basic functionalities e.g. setting default values and unit control is created.
                """)
            txt.configure(state='disabled')
            txt.configure(state='disabled')
        if index == 5: # Plotting panel
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Plotting panel holds created plots in separated tabs and holds tools to modify them.

You can toggle visibility of each line in plot left-clicking its name on the legend. Right-click hides and middle-click reveals all lines. You can hide the ledeng by clicking the "Hide legend"-button under the plot figure.

Under the plot figure are simple tools to modify the plot. You can activate a desired tool by clicking it. Information about the tool is shown when hoverin mouse over the button. You can drag and move the figure, zoom, modify the size and aspect ratio of figure and save the figure as image file. When saving the figure as an image, the figure is saved as a .png-file just as it's seen on the screen. More information on exporting the results can be found in the "Data export"-section. You can also adjust the scale of axes and the number of ticks. Units of the plot are controlled by the load tabs next to the plot.

Details of every load/workrate are shown as individual tabs next to the plot. Unknown values are calculated automaticly and marked as calculated. You can still modify every parameters units if necessary, since these units are used when exporting the results. You can also set the color and line style for every load/workrate by altering the "Line options"-dropdownmenus.
                """)
            txt.configure(state='disabled')
        if index == 6: # Data import
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""You can import data from an .xlsx-file with the data importer tool. The importing process can be initialized by clicking one of the "Import..."-buttons in the side menu or in the top menu. Once pressed a file selection pop-up window is shown. 

Importing process in a few steps:

1. Click "Import..."-button or choose "Import..." from the top menu
2. Select a .xlsx-file you want to import
3. Choose the sheet of the imported file you want to import from
4. Follow the parameter-by-parameter instructions and identify the tool where the wanted information is located
5. When all wanted parameters are successfully identified, press "Done"

The values can be selected in multiple ways. You can select whole rows or columsn by clicking the row or column index. Multiple rows or columns can be selected by holding down the CTRL- or SHIFT-buttons. Drag selection is also supported. You can also select a single cell by clicking it or multiple cells by CTRL- or SHIFT-buttons or drag selection. The currently selected cells are shown in the upper right corner of the importer tool.

You can navigate in the importing process by clicking wanted parameter in the side menu. The current location in the process is indicated by a left-pointing arrow and successfully imported parameters by a checkmark. You can also move one step ahead or backwards by clicking the "Next"- or "Prev"-buttons.
        """)
            txt.configure(state='disabled')
        if index == 7: # Data export
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Results can be exported to a .xlsx-file. You can export results projectwise or plotwise. Exporting can be done on a newly created file or concatenated on the same file used in importing.

Exporting projectwise to new file:
1. Choose "File" -> "Export..." -> "Project to new file" on the topmenu
2. Choose values you want to export from the popup-window and click "Export"
3. Choose location for the file and name the file
4. Once the exporting process is done, a notification is shown in the top part of the tool
5. The created .xlsx-file contains calculations and plots of project mean/SD and mean/IQR and subjects tests in separate sheets 

Exporting projectwise to imported file:
1. Choose "File" -> "Export..." -> "Project to imported file" on the topmenu
2. Choose values you want to export and the sheet you want to concatenate the calculations to from the popup-window and click "Export"
3. Choose location for the file and name the file
4. Once the exporting process is done, a notification is shown in the top part of the tool
5. The created .xlsx-file contains calculations concatenated in the selected sheet and extra sheets named "Mean-SD", "Mean-IQR" and "Plots". Extra sheets contain the projectwise calculations and plots and plots for every subjects test by test id.
                
Exporting plots to new file:
1. Plot every figure you want to export
2. Choose "File" -> "Export..." -> "Plots to new file" on the topmenu
3. Choose values you want to export from the popup-window and click "Export"
4. Choose location for the file and name the file
5. Once the exporting process is done, a notification is shown in the top part of the tool
6. The created .xlsx-file contains calculations and the plots from the plotting module on separate sheets

Exporting plots to imported file:
1. Plot every figure you want to export
2. Choose "File" -> "Export..." -> "Plots to imported file" on the topmenu
3. Choose values you want to export from the popup-window and click "Export"
4. Choose location for the file and name the file
5. Once the exporting process is done, a notification is shown in the top part of the tool
6. The created .xlsx-file contains calculations and the plots from the plotting module on separate sheets concatenated to the given file

                """)
            txt.configure(state='disabled')
        if index == 8: # Settings
            txt = ScrolledText(self.content, font=('TkDefaultFont', '10'), bg=self.window.cget('bg'))
            txt.pack(fill=BOTH, expand=True)
            txt.insert(INSERT,
"""Default settings can be viewed and modified in the "Settings"-menu in the topmenu.

Environmental-settings contain the default values and units for environmental parameters. These parameters are unfortunately NOT taken into account in the computing in this version. You can still set the values and units and save them by clicking the "Save"-button. A notification is shown in the top part of the settings window after successfull save is done.

Test-settings contain default values and units for the test parameters. The default values that can be set are core temperature and pH. Default units can be set for every parameter. Once the "Save"-button is pressed, the default settings are applied immediately and the test details -module is updated.
                """)
            txt.configure(state='disabled')
        if index == 9: # Equations
            pass
        if index == 10:
            # Get instruction document and create an image
            self.doc = fitz.open(r"C:/Koulu/Harjoittelu/HULA/SporttiaStadiin/Kutsu/SporttiaStadiinkutsu.pdf")
            self.pix = self.doc[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)

    def scale(self, e):
        # ratio = self.pix.height / self.pix.width
        w = math.floor(e.width)
        h = math.floor(self.ratio * e.width)
        img = self.img.resize( (w, h) )
        self.tkimg = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
        self.canvas.configure(scrollregion=(0, 0, w, h))

    def zoom(self, zoomMode):
        if zoomMode == 1:
            print('zoom in')
            img = self.img.resize( (math.floor(self.pix.width * 1.5), math.floor(self.pix.height * 1.5)) )
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
        elif zoomMode == 2:
            print('reset')
            img = self.img.resize( (math.floor(self.pix.width), math.floor(self.pix.height)) )
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
        elif zoomMode == 3:
            print('zoom out')
            img = self.img.resize( (math.floor(self.pix.width * 0.5), math.floor(self.pix.height * 0.5)) )
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)