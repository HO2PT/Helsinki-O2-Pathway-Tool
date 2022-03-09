from tkinter import *
from tkinter import ttk
from objects.app import app
from objects.test import Test
import numpy as np
from modules.notification import notification

class ProjectDetailsModule(object):
    def __init__(self, detailsPanel):
        self.container = ttk.Labelframe(detailsPanel, text="Project details")
        self.container.pack(side = LEFT, fill=Y)

        self.subjectCount = ttk.Label(self.container, text=None)
        self.subjectCount.pack(expand=False)

        # VO2 details
        self.VO2max = ttk.Label(self.container, text=None)
        self.VO2max.pack(expand=False)
        self.VO2min = ttk.Label(self.container, text=None)
        self.VO2min.pack(expand=False)
        self.VO2avg = ttk.Label(self.container, text=None)
        self.VO2avg.pack(expand=False)

        # QaO2 details
        self.QaO2max = ttk.Label(self.container, text=None)
        self.QaO2max.pack(expand=False)
        self.QaO2min = ttk.Label(self.container, text=None)
        self.QaO2min.pack(expand=False)
        self.QaO2avg = ttk.Label(self.container, text=None)
        self.QaO2avg.pack(expand=False)

        # DO2 details
        self.DO2max = ttk.Label(self.container, text=None)
        self.DO2max.pack(expand=False)
        self.DO2min = ttk.Label(self.container, text=None)
        self.DO2min.pack(expand=False)
        self.DO2avg = ttk.Label(self.container, text=None)
        self.DO2avg.pack(expand=False)

        self.calculateButton = ttk.Button(self.container, text="Calculate", command=lambda: print(app.getActiveProject()) ) #self.getMaxMinAvg()
        self.plotButton = ttk.Button(self.container, text="Plot VO\u2082", command=lambda: self.plotMaxMinAvg())

    def refreshDetails(self):
        # Show buttons
        try:
            self.calculateButton.pack_info()
            self.plotButton.pack_info()
        except:
            self.calculateButton.pack(side=BOTTOM)
            self.plotButton.pack(side=BOTTOM)
        
        activeProject = app.getActiveProject()
        self.subjectCount.config(text=f'Subjects: {len(activeProject.subjects)}')
        # VO2
        self.VO2max.config(text=f'VO\u2082\u2098\u2090\u2093 peak: {"{0:.1f}".format(float(activeProject.VO2max))}')
        self.VO2min.config(text=f'VO\u2082\u2098\u2090\u2093 min: {"{0:.1f}".format(float(activeProject.VO2min))}')
        self.VO2avg.config(text=f'VO\u2082\u2098\u2090\u2093 avg: {"{0:.1f}".format(float(activeProject.VO2avg))}')
        # QaO2
        self.QaO2max.config(text=f'QaO\u2082 peak: {"{0:.1f}".format(float(activeProject.QaO2max))}')
        self.QaO2min.config(text=f'QaO\u2082 min: {"{0:.1f}".format(float(activeProject.QaO2min))}')
        self.QaO2avg.config(text=f'QaO\u2082 avg: {"{0:.1f}".format(float(activeProject.QaO2avg))}')
        # DO2
        self.DO2max.config(text=f'DO\u2082 peak: {"{0:.1f}".format(float(activeProject.DO2max))}')
        self.DO2min.config(text=f'DO\u2082 min: {"{0:.1f}".format(float(activeProject.DO2min))}')
        self.DO2avg.config(text=f'DO\u2082 avg: {"{0:.1f}".format(float(activeProject.DO2avg))}')

    def getMaxMinAvg(self):
        activeProject = app.getActiveProject()
        subjects = activeProject.getSubjects()

        self.vo2maxList = []
        self.hrmaxList = []
        self.svmaxList = []
        self.qmaxList = []
        self.hbmaxList = []
        self.sao2maxList = []
        self.do2maxList = []
        self.qao2maxList = []
        self.cao2maxList = []
        self.svo2maxList = []
        self.cvo2maxList = []
        self.cavo2maxList = []
        self.pvo2maxList = []
        
        for s in subjects:
            tests = s.getTests()

            for t in tests:
                # details = t.getMaxLoad()
                w = t.getWorkLoads()[-1] # Last workload object
                details = w.getDetails().getWorkLoadDetails()

                validValues = app.getPlottingPanel().calc(w, details)
                if validValues == False:
                    notification.create('error', f"Couldn't calculate project metrics. Check values of subject: {s.id} test: {t.id}", '5000')
                details = w.getDetails().getWorkLoadDetails()

                self.vo2maxList.append(float(details['VO2']))
                self.hrmaxList.append(float(details['HR']))
                self.svmaxList.append(float(details['Sv']))
                self.qmaxList.append(float(details['Q']))
                self.hbmaxList.append(float(details['Hb']))
                self.sao2maxList.append(float(details['SaO2']))

                self.cao2maxList.append(float(details['CaO2']))
                self.svo2maxList.append(float(details['SvO2']))
                self.cvo2maxList.append(float(details['CvO2']))
                self.cavo2maxList.append(float(details['CavO2']))
                self.pvo2maxList.append(float(details['PvO2']))
                self.do2maxList.append(float(details['DO2']))
                self.do2maxList.append(float(details['DO2']))
                self.qao2maxList.append(float(details['QaO2']))
    
        self.avgVO2 = sum(self.vo2maxList) / len(self.vo2maxList)
        self.avgHR = sum(self.hrmaxList) / len(self.hrmaxList)
        self.avgSv= sum(self.svmaxList) / len(self.svmaxList)
        self.avgQ = sum(self.qmaxList) / len(self.qmaxList)
        self.avgHb = sum(self.hbmaxList) / len(self.hbmaxList)
        self.avgSaO2 = sum(self.sao2maxList) / len(self.sao2maxList)
        self.avgDO2 = sum(self.do2maxList) / len(self.do2maxList)
        self.avgQaO2 = sum(self.qao2maxList) / len(self.qao2maxList)

        self.avgCaO2 = sum(self.cao2maxList) / len(self.cao2maxList)
        self.avgSvO2 = sum(self.svo2maxList) / len(self.svo2maxList)
        self.avgCvO2 = sum(self.cvo2maxList) / len(self.cvo2maxList)
        self.avgCavO2 = sum(self.cavo2maxList) / len(self.cavo2maxList)
        self.avgPvO2 = sum(self.pvo2maxList) / len(self.pvo2maxList)
        

        activeProject.VO2max = max(self.vo2maxList)
        activeProject.VO2min = min(self.vo2maxList)
        activeProject.VO2avg = self.avgVO2
        self.VO2std = np.std(self.vo2maxList)
        # print(activeProject.VO2max, activeProject.VO2min,activeProject.VO2avg)
        # print(f'VO2 STD: {np.std(self.vo2maxList)}')
                
        activeProject.HRmax = max(self.hrmaxList)
        activeProject.HRmin = min(self.hrmaxList)
        activeProject.HRavg = self.avgHR
        self.HRstd = np.std(self.hrmaxList)
        # print(activeProject.HRmax, activeProject.HRmin,  activeProject.HRavg)
        # print(f'HR STD: {np.std(self.hrmaxList)}')

        activeProject.SVmax = max(self.svmaxList)
        activeProject.SVmin = min(self.svmaxList)
        activeProject.SVavg = self.avgSv
        self.SVstd = np.std(self.svmaxList)
        # print(activeProject.SVmax, activeProject.SVmin, activeProject.SVavg)
        # print(f'SV STD: {np.std(self.svmaxList)}')

        activeProject.Qmax = max(self.qmaxList)
        activeProject.Qmin = min(self.qmaxList)
        activeProject.Qavg = self.avgQ
        self.Qstd = np.std(self.qmaxList)
        # print(activeProject.Qmax, activeProject.Qmin, activeProject.Qavg)
        # print(f'Q STD: {np.std(self.qmaxList)}')

        activeProject.Hbmax = max(self.hbmaxList)
        activeProject.Hbmin = min(self.hbmaxList)
        activeProject.Hbavg = self.avgHb
        self.HBstd = np.std(self.hbmaxList)
        # print(activeProject.Hbmax, activeProject.Hbmin, activeProject.Hbavg)
        # print(f'Hb STD: {np.std(self.hbmaxList)}')

        activeProject.SaO2max = max(self.sao2maxList)
        activeProject.SaO2min = min(self.sao2maxList)
        activeProject.SaO2avg = self.avgSaO2
        self.SAO2std = np.std(self.sao2maxList)
        # print(activeProject.SaO2max, activeProject.SaO2min, activeProject.SaO2avg)
        # print(f'SaO2 STD: {np.std(self.sao2maxList)}')

        activeProject.DO2max = max(self.do2maxList)
        activeProject.DO2min = min(self.do2maxList)
        activeProject.DO2avg = self.avgDO2
        self.DO2std = np.std(self.do2maxList)
        # print(f'STD DO2: {np.std(self.do2maxList)}')

        activeProject.QaO2max = max(self.qao2maxList)
        activeProject.QaO2min = min(self.qao2maxList)
        activeProject.QaO2avg = self.avgQaO2
        self.QAO2std = np.std(self.qao2maxList)
        # print(f'STD QaO2: {np.std(self.qao2maxList)}')

        self.stdCaO2 = np.std(self.cao2maxList)
        # print(f'STD CaO2: {np.std(self.cao2maxList)}')
        self.stdSvO2 = np.std(self.svo2maxList)
        # print(f'STD SvO2: {np.std(self.svo2maxList)}')
        self.stdCvO2 = np.std(self.cvo2maxList)
        # print(f'STD CvO2: {np.std(self.cvo2maxList)}')
        self.stdCavO2 = np.std(self.cavo2maxList)
        # print(f'STD CavO2: {np.std(self.cavo2maxList)}')
        self.stdPvO2 = np.std(self.pvo2maxList)
        # print(f'STD PvO2: {np.std(self.pvo2maxList)}')
                
        self.refreshDetails()

    def plotMaxMinAvg(self):
        project = app.getActiveProject()
        projectTest = project.getMetricsTestObject()
        app.setActiveTest(projectTest)

        self.getMaxMinAvg()

        # Min load
        minLoad = projectTest.getWorkLoads()[0]
        self.setValues(minLoad, 'min')
        self.updateMC(minLoad)
        self.calcCoords(minLoad)

        # Avg load
        avgLoad = projectTest.getWorkLoads()[1]
        self.setValues(avgLoad, 'avg')
        self.updateMC(avgLoad)
        self.calcCoords(avgLoad)

        # Max load
        maxLoad = projectTest.getWorkLoads()[2]
        self.setValues(maxLoad, 'max')
        self.updateMC(maxLoad)
        self.calcCoords(maxLoad)

        app.getPlottingPanel().plotProject()

    def updateMC(self, load):
        load.getDetails().setMC('VO2_MC', 1)
        load.getDetails().setMC('HR_MC', 1)
        load.getDetails().setMC('Sv_MC', 1)
        load.getDetails().setMC('Q_MC', 1)
        load.getDetails().setMC('Hb_MC', 1)
        load.getDetails().setMC('SaO2_MC', 1)
        load.getDetails().setMC('CaO2_MC', 1)
        load.getDetails().setMC('SvO2_MC', 1)
        load.getDetails().setMC('CvO2_MC', 1)
        load.getDetails().setMC('CavO2_MC', 1)
        load.getDetails().setMC('PvO2_MC', 1)
        load.getDetails().setMC('QaO2_MC', 1)

    def setValues(self, load, mode):

        if mode == 'min':
            load.getDetails().setValue('VO2', self.avgVO2-self.VO2std)
            load.getDetails().setValue('HR', self.avgHR-self.HRstd)
            load.getDetails().setValue('Sv', self.avgSv-self.SVstd)
            load.getDetails().setValue('Q', self.avgQ-self.Qstd)
            load.getDetails().setValue('Hb', self.avgHb-self.HBstd)
            load.getDetails().setValue('SaO2', self.avgSaO2-self.SAO2std)
            load.getDetails().setValue('CaO2', self.avgCaO2-self.stdCaO2)
            load.getDetails().setValue('SvO2', self.avgSvO2-self.stdSvO2)
            load.getDetails().setValue('CvO2', self.avgCvO2-self.stdCvO2)
            load.getDetails().setValue('CavO2', self.avgCavO2-self.stdCavO2)
            load.getDetails().setValue('PvO2', self.avgPvO2-self.stdPvO2)
            load.getDetails().setValue('QaO2', self.avgQaO2-self.QAO2std)
            load.getDetails().setValue('DO2', self.avgDO2-self.DO2std)
        elif mode == 'avg':
            load.getDetails().setValue('VO2', self.avgVO2)
            load.getDetails().setValue('HR', self.avgHR)
            load.getDetails().setValue('Sv', self.avgSv)
            load.getDetails().setValue('Q', self.avgQ)
            load.getDetails().setValue('Hb', self.avgHb)
            load.getDetails().setValue('SaO2', self.avgSaO2)
            load.getDetails().setValue('CaO2', self.avgCaO2)
            load.getDetails().setValue('SvO2', self.avgSvO2)
            load.getDetails().setValue('CvO2', self.avgCvO2)
            load.getDetails().setValue('CavO2', self.avgCavO2)
            load.getDetails().setValue('PvO2', self.avgPvO2)
            load.getDetails().setValue('QaO2', self.avgQaO2)
            load.getDetails().setValue('DO2', self.avgDO2)
        elif mode == 'max':
            load.getDetails().setValue('VO2', self.avgVO2+self.VO2std)
            load.getDetails().setValue('HR', self.avgHR+self.HRstd)
            load.getDetails().setValue('Sv', self.avgSv+self.SVstd)
            load.getDetails().setValue('Q', self.avgQ+self.Qstd)
            load.getDetails().setValue('Hb', self.avgHb+self.HBstd)
            load.getDetails().setValue('SaO2',self.avgSaO2+self.SAO2std)
            load.getDetails().setValue('CaO2', self.avgCaO2+self.stdCaO2)
            load.getDetails().setValue('SvO2', self.avgSvO2+self.stdSvO2)
            load.getDetails().setValue('CvO2', self.avgCvO2+self.stdCvO2)
            load.getDetails().setValue('CavO2', self.avgCavO2+self.stdCavO2)
            load.getDetails().setValue('PvO2', self.avgPvO2+self.stdPvO2)
            load.getDetails().setValue('QaO2', self.avgQaO2+self.QAO2std)
            load.getDetails().setValue('DO2', self.avgDO2+self.DO2std)

    def calcCoords(self, load):
        temp = load.getDetails().getWorkLoadDetails()
        PvO2 = np.arange(0,100,1)
        y = 2* temp['DO2'] * PvO2

        with np.errstate(divide='ignore'):
            SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )
        SvO2[np.isnan(SvO2)] = 0
        y2 = temp['Q'] * ( 1.34 * temp['Hb'] * ( temp['SaO2']/ 100 - SvO2 ) )

        load.getDetails().y = y
        load.getDetails().y2 = y2
        load.getDetails().xi = -1
        load.getDetails().yi = -1