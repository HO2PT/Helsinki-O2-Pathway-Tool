from objects.test import Test

class Project(object):
    def __init__(self):
        self.id = 'Project'
        self.subjects = []
        self.VO2max = 0
        self.VO2min = 0
        self.VO2avg = 0

        """ self.HRmax = 0
        self.HRmin = 0
        self.HRavg = 0

        self.SVmax = 0
        self.SVmin = 0
        self.SVavg = 0

        self.Qmax = 0
        self.Qmin = 0
        self.Qavg = 0

        self.Hbmax = 0
        self.Hbmin = 0
        self.Hbavg = 0

        self.SaO2max = 0
        self.SaO2min = 0
        self.SaO2avg = 0 """

        self.QaO2max = 0
        self.QaO2min = 0
        self.QaO2avg = 0

        self.DO2max = 0
        self.DO2min = 0
        self.DO2avg = 0

        """ self.vo2maxList = []
        self.hrmaxList = []
        self.svmaxList = []
        self.qmaxList = []
        self.hbmaxList = []
        self.sao2maxList = [] """
        
        self.metricsTestObject = Test()
        self.metricsTestObject.setId(self.id)
        self.minLoad = self.metricsTestObject.getWorkLoads()[0]
        self.minLoad.setName('-1 STD')
        self.avgLoad = self.metricsTestObject.createLoad()
        self.avgLoad.setName('Avg')
        self.maxLoad = self.metricsTestObject.createLoad()
        self.maxLoad.setName('+1 STD')

    def addSubject(self, subject):
        self.subjects.append(subject)
    
    def getSubjects(self):
        return self.subjects

    def setId(self, id):
        self.id = id

    def setMetricsTestObject(self, testObject):
        self.metricsTestObject = testObject

    def getMetricsTestObject(self):
        return self.metricsTestObject