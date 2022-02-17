import uuid
from objects.envDetails import EnvDetails
from objects.workLoadDetails import WorkLoadDetails

class Test(object):
    def __init__(self):
        self.id = uuid.uuid1()
        self.date = None
        self.data = None
        self.subjectDetails = None
        self.envDetails = EnvDetails()
        self.workLoadCount = None
        self.endWorkLoad = None
        self.workLoads = []

        # Initiate load object
        self.workLoads.append( Load() )

    def getWorkLoads(self):
        return self.workLoads

    def addWorkLoad(self, load):
        self.workLoads.append(load)

    def createLoad(self):
        newLoad = Load()
        self.workLoads.append( newLoad )
        return newLoad

    def nWorkLoads(self):
        return len(self.workLoads)

    def getEnvDetails(self):
        return self.envDetails

    def setId(self, id):
        self.id = id

class Load(object):
    def __init__(self):
        self.name = None
        self.details = WorkLoadDetails()
    
    def getDetails(self):
        return self.details

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name