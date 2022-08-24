import fitz
import math
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from objects.app import app

class Help():
    def __init__(self):
        self.window = Toplevel()
        self.window.title('Help')
        self.window.geometry('750x500')
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='Img/ho2pt.png'))

        windowX = app.root.winfo_rootx() + (app.root.winfo_reqwidth()/2)
        windowY = app.root.winfo_rooty() + (app.root.winfo_reqheight()/10)
        self.window.geometry("+%d+%d" % ( windowX, windowY ))

        # Left panel
        self.leftPanel = ttk.Frame(self.window)
        self.leftPanel.pack(side=LEFT, fill=Y)

        self.progressionList = Listbox(self.leftPanel, width=25)
        options = [
            'Modeling',
            'Layout',
            'Side panel',
            'Details panel',
            'Plot panel',
            'Data import',
            'Data export',
            'Settings',
            'How to',
            'Troubleshooting'
        ]

        for opt in options:
            self.progressionList.insert('end', opt)

        self.progressionList.pack(expand=1, fill=BOTH)
        self.progressionList.bind( '<<ListboxSelect>>', lambda e: self.handleListBoxSelect(e) )

        # Right panel
        self.rightPanel = ttk.Frame(self.window)
        self.rightPanel.pack(side=RIGHT, fill=BOTH, expand=True)

        # Toolbar above the content
        self.toolBar = ttk.Frame(self.rightPanel)
        self.toolBar.pack(fill=X, padx=(5,5), pady=(2,2))

        self.prevButton = ttk.Button(self.toolBar, text='<', command=self.prevPage, width=3)
        self.currentPageLabel = ttk.Label(self.toolBar, text='')
        self.nextButton = ttk.Button(self.toolBar, text='>', command=self.nextPage, width=3)

        self.zoomInButton = ttk.Button(self.toolBar, text='+', command=lambda: self.zoom(1), width=3)
        self.zoomResetButton = ttk.Button(self.toolBar, text='Reset', command=lambda: self.zoom(2), width=5)
        self.zoomOutButton = ttk.Button(self.toolBar, text='-', command=lambda: self.zoom(3), width=3)
        
        # The content
        self.content = ttk.Frame(self.rightPanel)
        self.content.pack(fill=BOTH, expand=True)

        self.pixs = []
        self.index = 1
        self.doc = fitz.open('userInstructions.pdf')

        self.window.mainloop()

    def handleListBoxSelect(self, e):
        index = self.progressionList.curselection()[0]
        for c in self.content.winfo_children():
            c.destroy()

        self.pixs = []
        self.index = 1
        self.prevButton.pack(side=LEFT, expand=True, anchor='e')
        self.currentPageLabel.pack(side=LEFT)
        self.nextButton.pack(side=LEFT, expand=True, anchor='w')
        self.zoomOutButton.pack(side=RIGHT)
        self.zoomResetButton.pack(side=RIGHT)
        self.zoomInButton.pack(side=RIGHT)

        wrapper = ttk.Frame(self.content)
        wrapper.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(wrapper)
            
        scrollbarY = Scrollbar(wrapper)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarY.config(command=self.canvas.yview)

        scrollbarX = Scrollbar(wrapper, orient=HORIZONTAL)
        scrollbarX.pack(side=BOTTOM, fill=X, )
        scrollbarX.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
        self.canvas.pack(fill=BOTH, expand=True)

        self.content.bind('<Configure>', self.scale)
        self.canvas.bind('<MouseWheel>', self.handleMouseWheel)

        if index == 0: # Modelling s.5-7
            for page in self.doc.pages(4, 7, 1):
                self.pixs.append(page)
            
            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 1: # Layout s.9-10
            for page in self.doc.pages(8, 10, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 2: # Side Panel s.11-14
            for page in self.doc.pages(10, 14, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 3: # Details panel s.15-18
            for page in self.doc.pages(14, 18, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 4: # Plotting panel s.19-22
            for page in self.doc.pages(18, 22, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 5: # Data import s.25-32
            for page in self.doc.pages(24, 32, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 6: # Data export s.33-37
            for page in self.doc.pages(32, 37, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 7: # Settings s.23-24
            for page in self.doc.pages(22, 24, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

        elif index == 8: # How to s.38-49
            for page in self.doc.pages(37, 49, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')
        
        elif index == 9: # Troubleshooting s.50-51
            for page in self.doc.pages(49, 51, 1):
                self.pixs.append(page)

            self.pix = self.pixs[0].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
            
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
            
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

    def nextPage(self, e=None):
        if self.index < len(self.pixs):
            self.index += 1
            self.pix = self.pixs[self.index-1].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
                
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
                
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

    def prevPage(self, e=None):
        if self.index > 1:
            self.index -= 1
            self.pix = self.pixs[self.index-1].get_pixmap()
            mode = "RGBA" if self.pix.alpha else "RGB"
            self.img = Image.frombytes(mode, [self.pix.width, self.pix.height], self.pix.samples)
                
            self.ratio = self.pix.height / self.pix.width
            img = self.img.resize(( math.floor(self.content.winfo_width()), math.floor(self.ratio * self.content.winfo_width()) ))
            self.tkimg = ImageTk.PhotoImage(img)
                
            self.canvas.configure( scrollregion=(0, 0, img.width, img.height) )
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.currentPageLabel.config(text=f'{self.index}/{len(self.pixs)}')

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
            w = math.floor(self.tkimg.width() * 1.1)
            h = math.floor(self.tkimg.height() * 1.1)
            img = self.img.resize((w, h))
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.canvas.configure(scrollregion=(0, 0, w, h))
        elif zoomMode == 2:
            w = math.floor(self.pix.width)
            h = math.floor(self.pix.height)
            img = self.img.resize( (w, h) )
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.canvas.configure(scrollregion=(0, 0, w, h))
        elif zoomMode == 3:
            w = math.floor(self.tkimg.width() * 0.9)
            h = math.floor(self.tkimg.height() * 0.9)
            img = self.img.resize((w, h))
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tkimg)
            self.canvas.configure(scrollregion=(0, 0, w, h))

    def handleMouseWheel(self, e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")