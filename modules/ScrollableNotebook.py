# Copyright (c) Muhammet Emin TURGUT 2020
# For license see LICENSE

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel
from objects.app import app

class ScrollableNotebook(ttk.Frame):
    def __init__(self, parent, parentObj=None, wheelscroll=False, tabmenu=False, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self.xLocation = 0
        self.notebookContent = ttk.Notebook(self,**kwargs)
        self.notebookContent.pack(fill="both", expand=True)
        self.notebookTab = ttk.Notebook(self,**kwargs)
        self.notebookTab.bind("<<NotebookTabChanged>>",self._tabChanger)
        self.notebookTab.bind("<1>",self.handleTabClick)
        if wheelscroll==True: self.notebookTab.bind("<MouseWheel>", self._wheelscroll)
        slideFrame = ttk.Frame(self)
        slideFrame.place(relx=1.0, x=0, y=1, anchor=NE)
        self.menuSpace=30
        if tabmenu==True:
            self.menuSpace=50
            bottomTab = ttk.Label(slideFrame, text=" \u2630 ")
            bottomTab.bind("<1>",self._bottomMenu)
            bottomTab.pack(side=RIGHT)
        leftArrow = ttk.Label(slideFrame, text=" \u276E")
        leftArrow.bind("<1>",self._leftSlide)
        leftArrow.pack(side=LEFT)
        rightArrow = ttk.Label(slideFrame, text=" \u276F")
        rightArrow.bind("<1>",self._rightSlide)
        rightArrow.pack(side=RIGHT)
        self.notebookContent.bind("<Configure>", self._resetSlide)
        self.parentObj = parentObj

    def handleTabClick(self, e):
        try:
            clickedTabIndex = self.notebookTab.index(f'@{e.x},{e.y}')
            clickedObject = type(self.parentObj).__name__

            if self.notebookTab.identify(e.x, e.y) == 'close':
                if clickedObject == 'LoadNotebook': # If tab in details panel
                    if askokcancel("Confirm", "Do you want to remove the tab?"):

                        tab_id = self.notebookTab.tabs()[clickedTabIndex]
                        content_id = self.notebookContent.tabs()[clickedTabIndex]

                        self.notebookTab.forget(clickedTabIndex)
                        self.notebookContent.forget(clickedTabIndex)

                        for c in self.notebookTab.winfo_children():
                            if str(tab_id) == str(c):
                                c.destroy()
                                del c
                            
                        for c in self.winfo_children():
                            if str(content_id) == str(c):
                                c.destroy()
                                del c

                        tab = self.parentObj.loadTabs[clickedTabIndex]
                        for r in tab.detailRows:
                            if len(r.objects) != 0:
                                for o in r.objects:
                                    del o
                            for i, v in enumerate(r.vars):
                                v.trace_vdelete('w', r.traceids[i] )
                                del v
                            r.destroy()
                            del r
                        tab.loadFrame.destroy()
                        del self.parentObj.loadTabs[clickedTabIndex]
                        del app.getActiveTest().workLoads[clickedTabIndex]
                        # Update ph & temp
                        app.testDetailModule.loadNotebook.updatePhAndTemp()
                        app.testDetailModule.loadNotebook.refresh()
                            
                    if len(self.notebookTab.tabs()) == 0:
                        app.activeTest = None
                        app.testDetailModule.testId.pack_forget()
                        app.testDetailModule.loadsContainer.pack_forget()
                        app.sidepanel_testList.testList.selection_clear(0, 'end')

                else: # If tab in plotting panel
                    if askokcancel("Confirm", "Do you want to remove the tab?"):
                        tab_id = self.notebookTab.tabs()[clickedTabIndex]
                        content_id = self.notebookContent.tabs()[clickedTabIndex]

                        self.notebookTab.forget(clickedTabIndex)
                        self.notebookContent.forget(clickedTabIndex)

                        for c in self.notebookTab.winfo_children():
                            if str(tab_id) == str(c):
                                c.destroy()
                                del c
                            
                        for c in self.winfo_children():
                            if str(content_id) == str(c):
                                c.destroy()
                                del c

                        plots = self.parentObj.plots # PlotTab objects
                        plot = plots[clickedTabIndex]
                        loadTabs = plot.loadTabs # PlotLoadTab objects
                        for t in loadTabs: # PlotLoadTab object
                            for r in t.rowElements:
                                r.destroy()
                                del r
                            t.destroy()
                            del t

                        plot.destroy()  
                        del plot
                        del plots[clickedTabIndex]

                        # Hide plot panel if the last tab is closed
                        if len(plots) == 0:
                            self.parentObj.plotNotebook.pack_forget()
        except TclError:
            pass

    def _wheelscroll(self, event):
        if event.delta > 0:
            self._leftSlide(event)
        else:
            self._rightSlide(event)

    def _bottomMenu(self,event):
        tabListMenu = Menu(self, tearoff = 0)
        for tab in self.notebookTab.tabs():
            tabListMenu.add_command(label=self.notebookTab.tab(tab, option="text"),command= lambda temp=tab: self.select(temp))
        try: 
            tabListMenu.tk_popup(event.x_root, event.y_root) 
        finally: 
            tabListMenu.grab_release()

    def _tabChanger(self,event):
        try: 
            self.notebookContent.select(self.notebookTab.index("current"))
            app.envDetailModule.refresh()
        except: pass

    def _rightSlide(self,event):
        if self.notebookTab.winfo_width()>self.notebookContent.winfo_width()-self.menuSpace:
            if (self.notebookContent.winfo_width()-(self.notebookTab.winfo_width()+self.notebookTab.winfo_x()))<=self.menuSpace+5:
                self.xLocation-=20
                self.notebookTab.place(x=self.xLocation,y=0)
    def _leftSlide(self,event):
        if not self.notebookTab.winfo_x()== 0:
            self.xLocation+=20
            self.notebookTab.place(x=self.xLocation,y=0)

    def _resetSlide(self,event=None):
        self.notebookTab.place(x=0,y=0)
        self.xLocation = 0

    def add(self,frame,**kwargs):
        if len(self.notebookTab.winfo_children())!=0:
            self.notebookContent.add(frame, text="",state="hidden")
        else:
            self.notebookContent.add(frame, text="")
        self.notebookTab.add(ttk.Frame(self.notebookTab),**kwargs)

    def forget(self,tab_id):
        self.notebookContent.forget(self.__ContentTabID(tab_id))
        self.notebookTab.forget(tab_id)

        for c in self.notebookTab.winfo_children():
            if str(tab_id) == str(c):
                c.destroy()
                del c
                
    def hide(self,tab_id):
        self.notebookContent.hide(self.__ContentTabID(tab_id))
        self.notebookTab.hide(tab_id)

    def identify(self,x, y):
        return self.notebookTab.identify(x,y)

    def index(self,tab_id):
        return self.notebookTab.index(tab_id)

    def __ContentTabID(self,tab_id):
        return self.notebookContent.tabs()[self.notebookTab.tabs().index(tab_id)]

    def insert(self,pos,frame, **kwargs):
        self.notebookContent.insert(pos,frame, **kwargs)
        self.notebookTab.insert(pos,frame,**kwargs)

    def select(self,tab_id):
        self.notebookTab.select(tab_id)

    def tab(self,tab_id, option=None, **kwargs):
        kwargs_Content = kwargs.copy()
        kwargs_Content["text"] = "" # important
        self.notebookContent.tab(self.__ContentTabID(tab_id), option=None, **kwargs_Content)
        return self.notebookTab.tab(tab_id, option=None, **kwargs)

    def tabs(self):
        return self.notebookTab.tabs()

    def enable_traversal(self):
        self.notebookContent.enable_traversal()
        self.notebookTab.enable_traversal()