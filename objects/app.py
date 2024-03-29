import numpy as np
from copy import deepcopy
from modules.notification import notification
from modules.O2PTSolver import O2PTSolver

class App(object):
    def __init__(self):
        self.version = 1.5
        
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
        self.platform = None
        self.path = None

        self.defaultFont = None

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

    def deleteProject(self, index):
        del(self.projects[index])
    
    def addProject(self, project):
        self.projects.append(project)

    def getPlottingPanel(self):
        return self.plottingPanel

    def getProjects(self):
        return self.projects

    def getMaxMinAvg(self, plotProject=False, subjects=None):
        if plotProject == True:
            subjects = self.activeProject.getSubjects()

        self.vo2List = []
        self.hrList = []
        self.svList = []
        self.qList = []
        self.hbList = []
        self.sao2List = []
        self.do2List = []
        self.qao2List = []
        self.cao2List = []
        self.svo2List = []
        self.cvo2List = []
        self.cavo2List = []
        self.pvo2List = []
        self.pHList = []
        self.pH0List = []
        self.TList = []
        self.T0List = []
        # self.p50List = []

        for s in subjects:
            tests = s.getTests()
            wOrig = None

            for t in tests:
                # Find last workload with values
                for l in reversed(t.workLoads):
                    if l.details.getWorkLoadDetails()['Load'] != 0:
                        wOrig = l
                        break

                if wOrig == None:
                    wOrig = t.workLoads[-1] # Last workload object

                w = deepcopy(wOrig)
                workLoadObject = w.getDetails()
                details = w.getDetails().getWorkLoadDetails()

                solver = O2PTSolver(workLoadObject, details)
                validValues = solver.calc()
                if validValues == False:
                    notification.create('error', f"Couldn't calculate project metrics. Check values of subject: {s.id} test: {t.id}", '5000')
                details = w.getDetails().getWorkLoadDetails()

                self.vo2List.append(float(details['VO2']))
                self.hrList.append(float(details['HR']))
                self.svList.append(float(details['SV']))
                self.qList.append(float(details['Q']))
                self.hbList.append(float(details['[Hb]']))
                self.sao2List.append(float(details['SaO2']))

                self.cao2List.append(float(details['CaO2']))
                self.svo2List.append(float(details['SvO2']))
                self.cvo2List.append(float(details['CvO2']))
                self.cavo2List.append(float(details['C(a-v)O2']))
                self.pvo2List.append(float(details['PvO2']))
                self.do2List.append(float(details['DO2']))
                self.qao2List.append(float(details['QaO2']))

                self.pHList.append(float(details['pH']))
                self.pH0List.append(float(details['pH @ rest']))
                self.TList.append(float(details['T']))
                self.T0List.append(float(details['T @ rest']))

                # self.p50List.append(float(details['p50']))

        self.VO2mean = np.mean(self.vo2List)
        self.VO2q75, self.VO2q50, self.VO2q25 = np.percentile(self.vo2List, [75, 50, 25])

        self.HRmean = np.mean(self.hrList)
        self.HRq75, self.HRq50, self.HRq25 = np.percentile(self.hrList, [75, 50, 25])
        
        self.SVmean = np.mean(self.svList)
        self.SVq75, self.SVq50, self.SVq25 = np.percentile(self.svList, [75, 50, 25])
        
        self.Qmean = np.mean(self.qList)
        self.Qq75, self.Qq50, self.Qq25 = np.percentile(self.qList, [75, 50, 25])
        
        self.HBmean = np.mean(self.hbList)
        self.HBq75, self.HBq50, self.HBq25 = np.percentile(self.hbList, [75, 50, 25])
        
        self.SAO2mean = np.mean(self.sao2List)
        self.SAO2q75, self.SAO2q50, self.SAO2q25 = np.percentile(self.sao2List, [75, 50, 25])
        
        self.DO2mean = np.mean(self.do2List)
        self.DO2q75, self.DO2q50, self.DO2q25 = np.percentile(self.do2List, [75, 50, 25])
        
        self.QAO2mean = np.mean(self.qao2List)
        self.QAO2q75, self.QAO2q50, self.QAO2q25 = np.percentile(self.qao2List, [75, 50, 25])
        
        self.CAO2mean = np.mean(self.cao2List)
        self.CAO2q75, self.CAO2q50, self.CAO2q25 = np.percentile(self.cao2List, [75, 50, 25])
        
        self.SVO2mean = np.mean(self.svo2List)
        self.SVO2q75, self.SVO2q50, self.SVO2q25 = np.percentile(self.svo2List, [75, 50, 25])
        
        self.CVO2mean = np.mean(self.cvo2List)
        self.CVO2q75, self.CVO2q50, self.CVO2q25 = np.percentile(self.cvo2List, [75, 50, 25])
        
        self.CAVO2mean = np.mean(self.cavo2List)
        self.CAVO2q75, self.CAVO2q50, self.CAVO2q25 = np.percentile(self.cavo2List, [75, 50, 25])
        
        self.PVO2mean = np.mean(self.pvo2List)
        self.PVO2q75, self.PVO2q50, self.PVO2q25 = np.percentile(self.pvo2List, [75, 50, 25])

        self.pHmean = np.mean(self.pHList)
        self.pHq75, self.pHq50, self.pHq25 = np.percentile(self.pHList, [75, 50, 25])

        self.pH0mean = np.mean(self.pH0List)
        self.pH0q75, self.pH0q50, self.pH0q25 = np.percentile(self.pH0List, [75, 50, 25])

        self.Tmean = np.mean(self.TList)
        self.Tq75, self.Tq50, self.Tq25 = np.percentile(self.TList, [75, 50, 25])

        self.T0mean = np.mean(self.T0List)
        self.T0q75, self.T0q50, self.T0q25 = np.percentile(self.T0List, [75, 50, 25])

        # self.p50mean = np.mean(self.p50List)
        # self.p50q75, self.p50q50, self.p50q25 = np.percentile(self.p50List, [75, 50, 25])

        self.HRstd = np.std(self.hrList)
        self.SVstd = np.std(self.svList)
        self.Qstd = np.std(self.qList)
        self.HBstd = np.std(self.hbList)
        self.SAO2std = np.std(self.sao2List)
        self.VO2std = np.std(self.vo2List)
        self.DO2std = np.std(self.do2List)
        self.QAO2std = np.std(self.qao2List)
        self.CAO2std = np.std(self.cao2List)
        self.SVO2std = np.std(self.svo2List)
        self.CVO2std = np.std(self.cvo2List)
        self.CAVO2std = np.std(self.cavo2List)
        self.PVO2std = np.std(self.pvo2List)

        self.pHstd = np.std(self.pHList)
        self.pH0std = np.std(self.pH0List)
        self.Tstd = np.std(self.TList)
        self.T0std = np.std(self.T0List)
        # self.p50std = np.std(self.p50List)

        if plotProject == True:
            self.activeProject.VO2max = max(self.vo2List)
            self.activeProject.VO2min = min(self.vo2List)
            self.activeProject.VO2mean = self.VO2mean

            self.activeProject.DO2max = max(self.do2List)
            self.activeProject.DO2min = min(self.do2List)
            self.activeProject.DO2mean = self.DO2mean

            self.activeProject.QaO2max = max(self.qao2List)
            self.activeProject.QaO2min = min(self.qao2List)
            self.activeProject.QaO2mean = self.QAO2mean

        if plotProject == True:
            self.projectDetailModule.refreshDetails()

        return self.VO2mean, self.Qmean, self.HBmean, self.SAO2mean

    def plotMean(self, test=None, plotProject=False, subjects=None, iqr=False, ci95=False, export=False):
        self.meanTestObject = test

        if plotProject == True:
            if iqr == True:
                self.meanTestObject.setId(f'{self.meanTestObject.parentSubject.parentProject.id}(Median)')
            elif ci95 == True:
                self.meanTestObject.setId(f'{self.meanTestObject.parentSubject.parentProject.id}(95% CI)')
            else:
                self.meanTestObject.setId(f'{self.meanTestObject.parentSubject.parentProject.id}(Mean)')
        else:
            if len(subjects) > 1:
                if iqr == True:
                    self.meanTestObject.setId('Median (Chosen subjects)')
                elif ci95 == True:
                    self.meanTestObject.setId('Mean(95% CI) (Chosen subjects)')
                else:
                    self.meanTestObject.setId('Mean (Chosen subjects)')
            else:
                if iqr == True:
                    self.meanTestObject.setId(f'{subjects[0].id}-Median')
                elif ci95 == True:
                    self.meanTestObject.setId(f'{subjects[0].id}-Mean(95% CI)')
                else:
                    self.meanTestObject.setId((f'{subjects[0].id}-Mean'))

        self.minLoad = self.meanTestObject.getWorkLoads()[0]
        # self.avgLoad = self.meanTestObject.getWorkLoads()[0]

        if iqr == True:
            self.minLoad.setName('Q1')
            self.avgLoad = self.meanTestObject.createLoad()
            self.avgLoad.setName('Median')
            self.maxLoad = self.meanTestObject.createLoad()
            self.maxLoad.setName('Q3')
        elif ci95 == True:
            self.minLoad.setName('2.5%')
            self.avgLoad = self.meanTestObject.createLoad()
            self.avgLoad.setName('Mean')
            self.maxLoad = self.meanTestObject.createLoad()
            self.maxLoad.setName('97.5%')
        else:
            self.minLoad.setName('-1 SD')
            self.avgLoad = self.meanTestObject.createLoad()
            self.avgLoad.setName('Mean')
            self.maxLoad = self.meanTestObject.createLoad()
            self.maxLoad.setName('+1 SD')

        if export == False:
            self.activeTest = self.meanTestObject

        self.getMaxMinAvg(plotProject, subjects)

        # Min load
        minLoad = self.meanTestObject.getWorkLoads()[0]
        self.setValues(minLoad, 'min', iqr, ci95)
        self.updateMC(minLoad)
        self.calcCoords(minLoad)
        minLoad.details.y = np.full_like(minLoad.details.y, '-1')
        minLoad.details.y2 = np.full_like(minLoad.details.y2, '-1')
        minLoad.details.xi = -1
        minLoad.details.yi = -1

        # Avg load
        avgLoad = self.meanTestObject.getWorkLoads()[1]
        self.setValues(avgLoad, 'avg', iqr, ci95)
        self.updateMC(avgLoad)
        self.calcCoords(avgLoad)

        # Max load
        maxLoad = self.meanTestObject.getWorkLoads()[2]
        self.setValues(maxLoad, 'max', iqr, ci95)
        self.updateMC(maxLoad)
        self.calcCoords(maxLoad)
        maxLoad.details.y = np.full_like(maxLoad.details.y, '-1')
        maxLoad.details.y2 = np.full_like(maxLoad.details.y2, '-1')
        maxLoad.details.xi = -1
        maxLoad.details.yi = -1

        if export == False:
            self.plottingPanel.plotProject()

    def updateMC(self, load):
        load.getDetails().setMC('VO2_MC', 1)
        load.getDetails().setMC('HR_MC', 1)
        load.getDetails().setMC('Sv_MC', 1)
        load.getDetails().setMC('Q_MC', 1)
        load.getDetails().setMC('[Hb]_MC', 1)
        load.getDetails().setMC('SaO2_MC', 1)
        load.getDetails().setMC('CaO2_MC', 1)
        load.getDetails().setMC('SvO2_MC', 1)
        load.getDetails().setMC('CvO2_MC', 1)
        load.getDetails().setMC('C(a-v)O2_MC', 1)
        load.getDetails().setMC('PvO2_MC', 1)
        load.getDetails().setMC('QaO2_MC', 1)

    def setValues(self, load, mode, iqr, ci95):
        if iqr == True:
            load.getDetails().setValue('VO2', self.VO2q50)
            load.getDetails().setValue('HR', self.HRq50)
            load.getDetails().setValue('SV', self.SVq50)
            load.getDetails().setValue('Q', self.Qq50)
            load.getDetails().setValue('[Hb]', self.HBq50)
            load.getDetails().setValue('SaO2', self.SAO2q50)
            load.getDetails().setValue('CaO2', self.CAO2q50)
            load.getDetails().setValue('SvO2', self.SVO2q50)
            load.getDetails().setValue('CvO2', self.CVO2q50)
            load.getDetails().setValue('C(a-v)O2', self.CAVO2q50)
            load.getDetails().setValue('PvO2', self.PVO2q50)
            load.getDetails().setValue('QaO2', self.QAO2q50)
            load.getDetails().setValue('DO2', self.DO2q50)
            load.getDetails().setValue('pH', self.pHq50)
            load.getDetails().setValue('pH @ rest', self.pH0q50)
            load.getDetails().setValue('T', self.Tq50)
            load.getDetails().setValue('T @ rest', self.T0q50)
            # load.getDetails().setValue('p50', self.p50q50)

        else:
            load.getDetails().setValue('VO2', self.VO2mean)
            load.getDetails().setValue('HR', self.HRmean)
            load.getDetails().setValue('SV', self.SVmean)
            load.getDetails().setValue('Q', self.Qmean)
            load.getDetails().setValue('[Hb]', self.HBmean)
            load.getDetails().setValue('SaO2', self.SAO2mean)
            load.getDetails().setValue('CaO2', self.CAO2mean)
            load.getDetails().setValue('SvO2', self.SVO2mean)
            load.getDetails().setValue('CvO2', self.CVO2mean)
            load.getDetails().setValue('C(a-v)O2', self.CAVO2mean)
            load.getDetails().setValue('PvO2', self.PVO2mean)
            load.getDetails().setValue('QaO2', self.QAO2mean)
            load.getDetails().setValue('DO2', self.DO2mean)
            load.getDetails().setValue('pH', self.pHmean)
            load.getDetails().setValue('pH @ rest', self.pH0mean)
            load.getDetails().setValue('T', self.Tmean)
            load.getDetails().setValue('T @ rest', self.T0mean)
            # load.getDetails().setValue('p50', self.p50mean)

        if mode == 'min':
            if iqr == True:
                load.getDetails().setValue('VO2', self.VO2q25)
                load.getDetails().setValue('HR', self.HRq25)
                load.getDetails().setValue('SV', self.SVq25)
                load.getDetails().setValue('Q', self.Qq25)
                load.getDetails().setValue('[Hb]', self.HBq25)
                load.getDetails().setValue('SaO2', self.SAO2q25)
                load.getDetails().setValue('CaO2', self.CAO2q25)
                load.getDetails().setValue('SvO2', self.SVO2q25)
                load.getDetails().setValue('CvO2', self.CVO2q25)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2q25)
                load.getDetails().setValue('PvO2', self.PVO2q25)
                load.getDetails().setValue('QaO2', self.QAO2q25)
                load.getDetails().setValue('DO2', self.DO2q25)
                load.getDetails().setValue('pH', self.pHq25)
                load.getDetails().setValue('pH @ rest', self.pH0q25)
                load.getDetails().setValue('T', self.Tq25)
                load.getDetails().setValue('T @ rest', self.T0q25)
                # load.getDetails().setValue('p50', self.p50q25)

            elif ci95 == True:
                load.getDetails().setValue('VO2', self.VO2mean-(1.96*self.VO2std))
                load.getDetails().setValue('HR', self.HRmean-(1.96*self.HRstd))
                load.getDetails().setValue('SV', self.SVmean-(1.96*self.SVstd))
                load.getDetails().setValue('Q', self.Qmean-(1.96*self.Qstd))
                load.getDetails().setValue('[Hb]', self.HBmean-(1.96*self.HBstd))
                load.getDetails().setValue('SaO2', self.SAO2mean-(1.96*self.SAO2std))
                load.getDetails().setValue('CaO2', self.CAO2mean-(1.96*self.CAO2std))
                load.getDetails().setValue('SvO2', self.SVO2mean-(1.96*self.SVO2std))
                load.getDetails().setValue('CvO2', self.CVO2mean-(1.96*self.CVO2std))
                load.getDetails().setValue('C(a-v)O2', self.CAVO2mean-(1.96*self.CAVO2std))
                load.getDetails().setValue('PvO2', self.PVO2mean-(1.96*self.PVO2std))
                load.getDetails().setValue('QaO2', self.QAO2mean-(1.96*self.QAO2std))
                load.getDetails().setValue('DO2', self.DO2mean-(1.96*self.DO2std))
                load.getDetails().setValue('pH', self.pHmean-(1.96*self.pHstd))
                load.getDetails().setValue('pH @ rest', self.pH0mean-(1.96*self.pH0std))
                load.getDetails().setValue('T', self.Tmean-(1.96*self.Tstd))
                load.getDetails().setValue('T @ rest', self.T0mean-(1.96*self.T0std))
                # load.getDetails().setValue('p50', self.p50mean-(1.96*self.p50std))

            else:
                load.getDetails().setValue('VO2', self.VO2mean-self.VO2std)
                load.getDetails().setValue('HR', self.HRmean-self.HRstd)
                load.getDetails().setValue('SV', self.SVmean-self.SVstd)
                load.getDetails().setValue('Q', self.Qmean-self.Qstd)
                load.getDetails().setValue('[Hb]', self.HBmean-self.HBstd)
                load.getDetails().setValue('SaO2', self.SAO2mean-self.SAO2std)
                load.getDetails().setValue('CaO2', self.CAO2mean-self.CAO2std)
                load.getDetails().setValue('SvO2', self.SVO2mean-self.SVO2std)
                load.getDetails().setValue('CvO2', self.CVO2mean-self.CVO2std)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2mean-self.CAVO2std)
                load.getDetails().setValue('PvO2', self.PVO2mean-self.PVO2std)
                load.getDetails().setValue('QaO2', self.QAO2mean-self.QAO2std)
                load.getDetails().setValue('DO2', self.DO2mean-self.DO2std)
                load.getDetails().setValue('pH', self.pHmean-self.pHstd)
                load.getDetails().setValue('pH @ rest', self.pH0mean-self.pH0std)
                load.getDetails().setValue('T', self.Tmean-self.Tstd)
                load.getDetails().setValue('T @ rest', self.T0mean-self.T0std)
                # load.getDetails().setValue('p50', self.p50mean-self.p50std)
                
        elif mode == 'avg':
            if iqr == True:
                load.getDetails().setValue('VO2', self.VO2q50)
                load.getDetails().setValue('HR', self.HRq50)
                load.getDetails().setValue('SV', self.SVq50)
                load.getDetails().setValue('Q', self.Qq50)
                load.getDetails().setValue('[Hb]', self.HBq50)
                load.getDetails().setValue('SaO2', self.SAO2q50)
                load.getDetails().setValue('CaO2', self.CAO2q50)
                load.getDetails().setValue('SvO2', self.SVO2q50)
                load.getDetails().setValue('CvO2', self.CVO2q50)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2q50)
                load.getDetails().setValue('PvO2', self.PVO2q50)
                load.getDetails().setValue('QaO2', self.QAO2q50)
                load.getDetails().setValue('DO2', self.DO2q50)
                load.getDetails().setValue('pH', self.pHq50)
                load.getDetails().setValue('pH @ rest', self.pH0q50)
                load.getDetails().setValue('T', self.Tq50)
                load.getDetails().setValue('T @ rest', self.T0q50)
                # load.getDetails().setValue('p50', self.p50q50)

            else:
                load.getDetails().setValue('VO2', self.VO2mean)
                load.getDetails().setValue('HR', self.HRmean)
                load.getDetails().setValue('SV', self.SVmean)
                load.getDetails().setValue('Q', self.Qmean)
                load.getDetails().setValue('[Hb]', self.HBmean)
                load.getDetails().setValue('SaO2', self.SAO2mean)
                load.getDetails().setValue('CaO2', self.CAO2mean)
                load.getDetails().setValue('SvO2', self.SVO2mean)
                load.getDetails().setValue('CvO2', self.CVO2mean)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2mean)
                load.getDetails().setValue('PvO2', self.PVO2mean)
                load.getDetails().setValue('QaO2', self.QAO2mean)
                load.getDetails().setValue('DO2', self.DO2mean)
                load.getDetails().setValue('pH', self.pHmean)
                load.getDetails().setValue('pH @ rest', self.pH0mean)
                load.getDetails().setValue('T', self.Tmean)
                load.getDetails().setValue('T @ rest', self.T0mean)
                # load.getDetails().setValue('p50', self.p50mean)
                
        elif mode == 'max':
            if iqr == True:
                load.getDetails().setValue('VO2', self.VO2q75)
                load.getDetails().setValue('HR', self.HRq75)
                load.getDetails().setValue('SV', self.SVq75)
                load.getDetails().setValue('Q', self.Qq75)
                load.getDetails().setValue('[Hb]', self.HBq75)
                load.getDetails().setValue('SaO2', self.SAO2q75)
                load.getDetails().setValue('CaO2', self.CAO2q75)
                load.getDetails().setValue('SvO2', self.SVO2q75)
                load.getDetails().setValue('CvO2', self.CVO2q75)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2q75)
                load.getDetails().setValue('PvO2', self.PVO2q75)
                load.getDetails().setValue('QaO2', self.QAO2q75)
                load.getDetails().setValue('DO2', self.DO2q75)
                load.getDetails().setValue('pH', self.pHq75)
                load.getDetails().setValue('pH @ rest', self.pH0q75)
                load.getDetails().setValue('T', self.Tq75)
                load.getDetails().setValue('T @ rest', self.T0q75)
                # load.getDetails().setValue('p50', self.p50q75)

            elif ci95 == True:
                load.getDetails().setValue('VO2', self.VO2mean + (1.96*self.VO2std))
                load.getDetails().setValue('HR', self.HRmean + (1.96*self.HRstd))
                load.getDetails().setValue('SV', self.SVmean + (1.96*self.SVstd))
                load.getDetails().setValue('Q', self.Qmean + (1.96*self.Qstd))
                load.getDetails().setValue('[Hb]', self.HBmean + (1.96*self.HBstd))
                load.getDetails().setValue('SaO2', self.SAO2mean + (1.96*self.SAO2std))
                load.getDetails().setValue('CaO2', self.CAO2mean + (1.96*self.CAO2std))
                load.getDetails().setValue('SvO2', self.SVO2mean + (1.96*self.SVO2std))
                load.getDetails().setValue('CvO2', self.CVO2mean + (1.96*self.CVO2std))
                load.getDetails().setValue('C(a-v)O2', self.CAVO2mean + (1.96*self.CAVO2std))
                load.getDetails().setValue('PvO2', self.PVO2mean + (1.96*self.PVO2std))
                load.getDetails().setValue('QaO2', self.QAO2mean + (1.96*self.QAO2std))
                load.getDetails().setValue('DO2', self.DO2mean + (1.96*self.DO2std))
                load.getDetails().setValue('pH', self.pHmean + (1.96*self.pHstd))
                load.getDetails().setValue('pH @ rest', self.pH0mean + (1.96*self.pH0std))
                load.getDetails().setValue('T', self.Tmean + (1.96*self.Tstd))
                load.getDetails().setValue('T @ rest', self.T0mean + (1.96*self.T0std))
                # load.getDetails().setValue('p50', self.p50mean + (1.96*self.p50std))

            else:
                load.getDetails().setValue('VO2', self.VO2mean + self.VO2std)
                load.getDetails().setValue('HR', self.HRmean + self.HRstd)
                load.getDetails().setValue('SV', self.SVmean + self.SVstd)
                load.getDetails().setValue('Q', self.Qmean + self.Qstd)
                load.getDetails().setValue('[Hb]', self.HBmean + self.HBstd)
                load.getDetails().setValue('SaO2', self.SAO2mean + self.SAO2std)
                load.getDetails().setValue('CaO2', self.CAO2mean + self.CAO2std)
                load.getDetails().setValue('SvO2', self.SVO2mean + self.SVO2std)
                load.getDetails().setValue('CvO2', self.CVO2mean + self.CVO2std)
                load.getDetails().setValue('C(a-v)O2', self.CAVO2mean + self.CAVO2std)
                load.getDetails().setValue('PvO2', self.PVO2mean + self.PVO2std)
                load.getDetails().setValue('QaO2', self.QAO2mean + self.QAO2std)
                load.getDetails().setValue('DO2', self.DO2mean + self.DO2std)
                load.getDetails().setValue('pH', self.pHmean + self.pHstd)
                load.getDetails().setValue('pH @ rest', self.pH0mean + self.pH0std)
                load.getDetails().setValue('T', self.Tmean + self.Tstd)
                load.getDetails().setValue('T @ rest', self.T0mean + self.T0std)
                # load.getDetails().setValue('p50', self.p50mean + self.p50std)
                
    def calcCoords(self, load):
        temp = load.getDetails().getWorkLoadDetails()
        solver = O2PTSolver(load.details, temp)
        solver.calc()

app = App()