from objects.test import Test

class Project(object):
    def __init__(self):
        self.id = 'Project'
        self.subjects = []
        self.data = None
        self.VO2max = 0
        self.VO2min = 0
        self.VO2mean = 0

        self.QaO2max = 0
        self.QaO2min = 0
        self.QaO2mean = 0

        self.DO2max = 0
        self.DO2min = 0
        self.DO2mean = 0
        
        self.metricsTestObject = Test()
        self.metricsTestObject.setId(self.id)
        self.minLoad = self.metricsTestObject.getWorkLoads()[0]
        self.minLoad.setName('-1 SD')
        self.avgLoad = self.metricsTestObject.createLoad()
        self.avgLoad.setName('Mean')
        self.maxLoad = self.metricsTestObject.createLoad()
        self.maxLoad.setName('+1 SD')

        # Columns/rows used in dataimport
        self.dataMode = None
        self.idLoc = None
        self.loadLoc = None

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