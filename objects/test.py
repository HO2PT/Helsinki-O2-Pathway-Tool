from tkinter.messagebox import NO


import uuid

class Test(object):
    def __init__(self):
        print("Test instance created")
        self.id = uuid.uuid1()
        self.date = None
        self.data = None
        self.subjectDetails = None
        self.envDetails = None
        self.workLoadCount = None
        self.endWorkLoad = None
        self.workLoads = []