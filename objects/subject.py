from objects.test import Test

class Subject(object):
    def __init__(self, id=None):
        self.id = f'Subject{id}'
        self.tests = []

    def addTest(self, test=None):
        if test == None:
            testId = f'{self.id}-Test-{len(self.tests)+1}'
            test = Test(id=testId)
            self.tests.append(test)
        else:
            self.tests.append(test)

    def getTests(self):
        return self.tests

    def setId(self, id):
        self.id = id