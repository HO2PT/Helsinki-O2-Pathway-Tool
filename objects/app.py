import numpy as np
from copy import deepcopy
from modules.notification import notification

class App(object):

    def __init__(self):
        self.activeProject = None
        self.activeSubject = None
        self.activeTest = None
        self.activeMode = None
        self.projects = []
        self.settings = None

        self.sidePanel = None
        self.sidepanel_projectList = None
        self.sidepanel_subjectList = None
        self.sidepanel_testList = None

        self.detailsPanel = None
        self.projectDetailModule = None
        self.testDetailModule = None
        self.envDetailModule = None
        self.plottingPanel = None
        self.menu = None

        self.root = None
        self.strVars = None
        self.intVars = None

    def setActiveTest(self, test):
        self.activeTest = test

    def getActiveTest(self):
        return self.activeTest

    def setActiveSubject(self, subject):
        self.activeSubject = subject

    def getActiveSubject(self):
        return self.activeSubject

    def setActiveProject(self, project):
        self.activeProject = project

    def getActiveProject(self):
        return self.activeProject
    
    def addProject(self, project):
        self.projects.append(project)

    def getActiveMode(self):
        return self.activeMode

    def setActiveMode(self, mode):
        self.activeMode = mode

    def getPlottingPanel(self):
        return self.plottingPanel

    def getProjects(self):
        return self.projects

    def getMaxMinAvg(self, plotProject=False, subjects=None):
        if plotProject == True:
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
                wOrig = t.getWorkLoads()[-1] # Last workload object
                w = deepcopy(wOrig)
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
                self.qao2maxList.append(float(details['QaO2']))
    
        self.avgVO2 = np.mean(self.vo2maxList)
        self.avgHR = np.mean(self.hrmaxList)
        self.avgSv= np.mean(self.svmaxList)
        self.avgQ = np.mean(self.qmaxList)
        self.avgHb = np.mean(self.hbmaxList)
        self.avgSaO2 = np.mean(self.sao2maxList)
        self.avgDO2 = np.mean(self.do2maxList)
        self.avgQaO2 = np.mean(self.qao2maxList)
        self.avgCaO2 = np.mean(self.cao2maxList)
        self.avgSvO2 = np.mean(self.svo2maxList)
        self.avgCvO2 = np.mean(self.cvo2maxList)
        self.avgCavO2 = np.mean(self.cavo2maxList)
        self.avgPvO2 = np.mean(self.pvo2maxList)

        self.HRstd = np.std(self.hrmaxList)
        self.SVstd = np.std(self.svmaxList)
        self.Qstd = np.std(self.qmaxList)
        self.HBstd = np.std(self.hbmaxList)
        self.SAO2std = np.std(self.sao2maxList)

        if plotProject == True:
            activeProject.VO2max = max(self.vo2maxList)
            activeProject.VO2min = min(self.vo2maxList)
            activeProject.VO2avg = self.avgVO2
        self.VO2std = np.std(self.vo2maxList)
        print(f'STD VO2: {self.VO2std}')

        if plotProject == True:
            activeProject.DO2max = max(self.do2maxList)
            activeProject.DO2min = min(self.do2maxList)
            activeProject.DO2avg = self.avgDO2
        self.DO2std = np.std(self.do2maxList)
        print(f'STD DO2: {np.std(self.do2maxList)}')

        if plotProject == True:
            activeProject.QaO2max = max(self.qao2maxList)
            activeProject.QaO2min = min(self.qao2maxList)
            activeProject.QaO2avg = self.avgQaO2
        self.QAO2std = np.std(self.qao2maxList)
        print(f'STD QaO2: {np.std(self.qao2maxList)}')

        self.stdCaO2 = np.std(self.cao2maxList)
        print(f'STD CaO2: {np.std(self.cao2maxList)}')
        self.stdSvO2 = np.std(self.svo2maxList)
        print(f'STD SvO2: {np.std(self.svo2maxList)}')
        self.stdCvO2 = np.std(self.cvo2maxList)
        print(f'STD CvO2: {np.std(self.cvo2maxList)}')
        self.stdCavO2 = np.std(self.cavo2maxList)
        print(f'STD CavO2: {np.std(self.cavo2maxList)}')
        self.stdPvO2 = np.std(self.pvo2maxList)
        print(f'STD PvO2: {np.std(self.pvo2maxList)}')

        if plotProject == True:
            self.projectDetailModule.refreshDetails()

    def plotMaxMinAvg(self, test=None, plotProject=False, subjects=None):
        self.meanTestObject = test

        if plotProject == False:
            if len(subjects) > 1:
                self.meanTestObject.setId('Subjects mean')
            else:
                self.meanTestObject.setId(f'{subjects[0].id} mean')
        if plotProject == True:
            self.meanTestObject.setId('Project mean')
        self.minLoad = self.meanTestObject.getWorkLoads()[0]
        self.minLoad.setName('-1 STD')
        self.avgLoad = self.meanTestObject.createLoad()
        self.avgLoad.setName('Avg')
        self.maxLoad = self.meanTestObject.createLoad()
        self.maxLoad.setName('+1 STD')

        # project = app.getActiveProject()
        # projectTest = project.getMetricsTestObject()
        # app.setActiveTest(projectTest)
        app.setActiveTest(self.meanTestObject)

        self.getMaxMinAvg(plotProject, subjects)

        # Min load
        minLoad = self.meanTestObject.getWorkLoads()[0]
        self.setValues(minLoad, 'min')
        self.updateMC(minLoad)
        self.calcCoords(minLoad)

        # Avg load
        avgLoad = self.meanTestObject.getWorkLoads()[1]
        self.setValues(avgLoad, 'avg')
        self.updateMC(avgLoad)
        self.calcCoords(avgLoad)

        # Max load
        maxLoad = self.meanTestObject.getWorkLoads()[2]
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

app = App()