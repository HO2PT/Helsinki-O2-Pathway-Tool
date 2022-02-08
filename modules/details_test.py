from cgitb import text
from tkinter import *
from tkinter import ttk
from objects.app import app

class TestDetailModule(object):
    def __init__(self, detailsPanel):
        container = ttk.Labelframe(detailsPanel, text="Test details")
        container.pack(side = LEFT, fill = BOTH, expand=TRUE)

        # Details frame
        details = ttk.Frame(container)
        details.pack(side=LEFT, fill = BOTH, expand=TRUE)

        self.testId = ttk.Label(details, text=None)
        self.testId.pack()

        ttk.Button(details, text="Calculate").pack(side=BOTTOM)

        # Load notebook frame
        loadsContainer = ttk.Frame(container)
        loadsContainer.pack(side=RIGHT)

        # Add 'x'-button to tabs
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        style.configure('loadNotebook.TNotebook')
        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("loadNotebook.TNotebook", [
            ("loadNotebook.TNotebook.client", {
                "sticky": "nswe"
            })
        ])
        style.layout("loadNotebook.TNotebook.Tab", [
            ("loadNotebook.TNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("loadNotebook.TNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("loadNotebook.TNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("loadNotebook.TNotebook.label", {"side": "left", "sticky": ''}),
                                    ("loadNotebook.TNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

        # Notebook
        #self.loadNotebook = ttk.Notebook(loadsContainer, style='loadNotebook.TNotebook')
        self.loadNotebook = ttk.Notebook(loadsContainer)
        
        self.loadNotebook.pack(expand=TRUE)
        self.loadNotebook.bind('<Button-1>', lambda e: self.handleTabClick(e))

        # Initial Tab
        self.tab0 = ttk.Frame(self.loadNotebook, width=300, height=200)
        self.tab0.pack(expand=TRUE)
        
        self.loadNotebook.add(self.tab0, text='+')

    def handleTabClick(self, e):
        clickedTabIndex = self.loadNotebook.index(f'@{e.x},{e.y}')

        if self.loadNotebook.identify(e.x, e.y) == 'close':
            self.loadNotebook.forget(clickedTabIndex)
        else:
            self.createTab(e)

    def createTab(self, e):
        # Make sure '+'-tab is pressed
        clickedTabIndex = self.loadNotebook.index(f'@{e.x},{e.y}')
        tabCount = self.loadNotebook.index('end')      

        if clickedTabIndex == tabCount-1:
            load = ttk.Frame(self.loadNotebook, width=300, height=200)
            load.pack(expand=TRUE)
            ttk.Label(load, text="qwerty").pack()
            self.loadNotebook.insert(tabCount-1, load, text=f'Load{tabCount}')

    def refreshTestDetails(self):
        activeTest = app.activeTest
        self.testId.config(text=f'Id: {activeTest.id}')
