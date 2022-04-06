from objects.test import Test

class Subject(object):
    def __init__(self, id=None, parentProject=None):
        self.id = f'Subject{id}'
        self.parentProject = parentProject
        self.tests = []

    def addTest(self, test=None):
        if test == None:
            testId = f'{self.id}-Test-{len(self.tests)+1}'
            test = Test(id=testId, parentSubject=self)
            self.tests.append(test)
        else:
            self.tests.append(test)

    def getTests(self):
        return self.tests

    def deleteTest(self, index):
        del self.tests[index]

    def setId(self, id):
        self.id = id