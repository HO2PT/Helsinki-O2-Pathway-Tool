from objects.test import Test

class Subject(object):
    def __init__(self, id=None):
        self.id = f'Subject{id}'
        self.tests = []

    def addTest(self, test=None):
        if test == None:
            test = Test()
            self.tests.append(test)
        else:
            self.tests.append(test)

    def getTests(self):
        return self.tests

    def setId(self, id):
        self.id = id