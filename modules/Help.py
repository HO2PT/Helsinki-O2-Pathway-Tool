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
        if app.platform == 'darwin':
            self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'{app.path}/Img/ho2pt.png'))
        else:
            self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='Img/ho2pt.png'))

        # Left panel
        self.leftPanel = ttk.Frame(self.window)
        self.leftPanel.pack(side=LEFT, fill=Y)

        if app.platform == 'darwin':
            self.progressionList = Listbox(self.leftPanel, width=25, bg='#F5F6F7', fg='black')
        else:
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
        if app.platform == 'darwin':
            self.doc = fitz.open(f'{app.path}/userInstructions.pdf')
        else:
            self.doc = fitz.open('userInstructions.pdf')

        self.window.update_idletasks()
        windowX = app.root.winfo_rootx() + (app.root.winfo_width()/2) - self.window.winfo_width()/2
        windowY = app.root.winfo_rooty() + (app.root.winfo_height()/2) - self.window.winfo_height()/2
        self.window.geometry("+%d+%d" % ( windowX, windowY ))

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

        if index == 0: # Modelling s.6-9
            for page in self.doc.pages(5, 9, 1):
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

        elif index == 1: # Layout s.11-12
            for page in self.doc.pages(10, 12, 1):
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

        elif index == 2: # Side Panel s.13-16
            for page in self.doc.pages(12, 16, 1):
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

        elif index == 3: # Details panel s.17-21
            for page in self.doc.pages(16, 21, 1):
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

        elif index == 4: # Plotting panel s.22-25
            for page in self.doc.pages(21, 25, 1):
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

        elif index == 5: # Data import s.28-35
            for page in self.doc.pages(27, 35, 1):
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

        elif index == 6: # Data export s.36-42
            for page in self.doc.pages(35, 42, 1):
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

        elif index == 7: # Settings s.26-27
            for page in self.doc.pages(25, 27, 1):
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

        elif index == 8: # How to s.43-58
            for page in self.doc.pages(42, 58, 1):
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
        
        elif index == 9: # Troubleshooting s.59-60
            for page in self.doc.pages(58, 60, 1):
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