from tkinter import *
from objects.app import app

class About():
    def __init__(self):
        self.window = Toplevel()
        self.window.title('About')
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='Img/ho2pt.png'))

        msg = Message(self.window, padx=25, pady=10, text='Thank you for finding the Helsinki O\u2082 Pathway Tool (HO\u2082PT)!\n\nThis tool has been designed and programmed as a bachelor’s thesis project of an engineering student in health technology. The idea for the tool came from the professionals of Helsinki Sports and Exercise Medicine Clinic (HULA) and Department of Sports and Exercise Medicine, Clinicum, University of Helsinki. The tool is based on the integrated O\u2082 pathway model originally theorized by Peter D. Wagner (e.g., Wagner PD. Annu Rev Physiol 1996;58:21-50; Wagner PD. J Breath Res 2008;2:024001) and enables the description of O\u2082 uptake (V̇O\u2082) and its components both quantitatively and graphically. The modeling is based on the Fick equation and the Fick law of diffusion with some previously described assumptions (e.g., Legendre et al. Int J Cardiol 2021;330:120-127). The tool can be used with existing or new data.\n\nThere is no technical support for the source code. However, the source code of this tool is free to use and be modified to fit one’s individual needs.\n\nThe HO\u2082PT is intended to be used to analyze V̇O\u2082, its limiting components, and their alterations of a single test subject or a dataset. It is intended to be used as a tool for everyone researching V̇O\u2082, for example, in research, education, and athlete’s physical performance testing and coaching. It can be used in research of pulmonary, cardiovascular, and skeletal muscle conditions and disorders, for example, for identifying and monitoring factors limiting physical performance. In addition, if the tool and the information it provides are demonstrated by peer-reviewed original studies to be suitable for appropriate patient groups in clinical patient work as a part of diagnosis, monitoring, and decision-making, one of its intended use environments may be clinical patient work in the future. The tool can also be used to study effects of environmental factors and medication on physiological responses.')
        msg.pack()

        self.window.update_idletasks()

        windowX = app.root.winfo_rootx() + (app.root.winfo_width()/2) - self.window.winfo_width()/2
        windowY = app.root.winfo_rooty() + (app.root.winfo_height()/2) - self.window.winfo_height()/2
        self.window.geometry("+%d+%d" % ( windowX, windowY ))

        self.window.mainloop()