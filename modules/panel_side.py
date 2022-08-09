from tkinter import *
from tkinter import ttk
from objects.app import app
from modules.sidepanel_projects import ProjectList
from modules.sidepanel_subjectList import SubjectList
from modules.sidepanel_testList import TestList

class SidePanel(ttk.Frame):
    def __init__(self, mainFrame, *args, **kwargs):
        ttk.Frame.__init__(self, mainFrame, *args, **kwargs)
        self.pack(side=LEFT, fill=Y)

        self.mainFrame = mainFrame
        self.separator = ttk.Separator(self.mainFrame, style='asd.TSeparator')

        sty = ttk.Style()
        sty.configure(
            'sidePanel.TFrame', 
            relief='raised'
        )
        
        self.frame_thickness = 10

        self.sidePanel = ttk.Frame(self, style="sidePanel.TFrame", borderwidth=self.frame_thickness)
        if app.settings.visDefaults['sideMenu']:
            self.sidePanel.pack(side=LEFT, fill=Y)

        sty.layout('sidePanel.TFrame', [
            ('Frame.border', {'sticky': 'nse'})
        ])

        projects = ProjectList(self.sidePanel)
        app.sidepanel_projectList = projects

        subjects = SubjectList(self.sidePanel)
        app.sidepanel_subjectList = subjects

        tests = TestList(self.sidePanel)
        app.sidepanel_testList = tests

        # Add basic instructions to the footer
        self.info = ttk.Frame(self.sidePanel)

        self.info_icon1 = PhotoImage(file='Img/leftclick.png')
        self.info_icon2 = PhotoImage(file='Img/rightclick.png')
        
        infoLeft = ttk.Label(self.info, image=self.info_icon1)
        infoLeft.pack(side=LEFT)
        infoLeft2 = ttk.Label(self.info, text='= Select')
        infoLeft2.pack(side=LEFT)

        infoRight = ttk.Label(self.info, image=self.info_icon2)
        infoRight.pack(side=LEFT)
        infoRight2 = ttk.Label(self.info, text='= Deselect')
        infoRight2.pack(side=LEFT)

        infoDLeft = ttk.Label(self.info, image=self.info_icon1)
        infoDLeft.pack(side=LEFT)
        infoDLeft2 = ttk.Label(self.info, text='x2 = Open')
        infoDLeft2.pack(side=LEFT)
        
        self.info.pack()

        self.indicator = ttk.Label(self, text='', anchor='center')
        self.indicator.pack(side=RIGHT, fill=Y)

        # Helper variable to improve panel resizing
        self.posX = None

        self.sidePanel.bind('<Motion>', self.changeCursor)
        self.sidePanel.bind('<1>', self.setPosX)
        self.sidePanel.bind('<B1-Motion>', self.resize)
        self.sidePanel.bind('<ButtonRelease-1>', self.applyResize)
        self.indicator.bind('<Double-Button-1>', self.defSize)

    def changeCursor(self, e):
        if e.x > self.sidePanel.winfo_width() - self.frame_thickness:
            self.sidePanel.configure(cursor='sb_h_double_arrow')
        else:
            self.sidePanel.configure(cursor='arrow')

    def setPosX(self, e):
        self.posX = e.x

    def resize(self, event):
        self.sidePanel.pack_propagate(False)
        self.separator.place(height=self.winfo_height(), x=event.x, y=0)
        self.separator.lift()

    def applyResize(self, event):
        if event.x != self.posX:
            self.separator.place_forget()
            
            if event.x > 10:
                self.sidePanel.configure(height=self.sidePanel.winfo_height(), width=event.x)
                self.update_idletasks()
                minWidth = app.sidepanel_projectList.container.winfo_reqwidth()
                containerWidth = self.sidePanel.winfo_width()

                if containerWidth < minWidth:
                    self.indicator.configure(text='\u2B9E', foreground='white', background='#4eb1ff')
                else:
                    self.indicator.configure(text='', background=app.root.cget('bg'))
            else:
                self.sidePanel.configure(height=self.sidePanel.winfo_height(), width=10)
                self.indicator.configure(text='\u2B9E', foreground='white', background='#4eb1ff')

    def defSize(self, event):
        self.indicator.configure(text='', background=app.root.cget('bg'))
        self.sidePanel.pack_propagate(True)