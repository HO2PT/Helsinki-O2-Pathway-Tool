class Subject(object):
    def __init__(self, id):
        print("Subject instance created")
        self.id = f'Subject{id}'
        self.tests = []

    def addTest(self, test):
        self.tests.append(test)

    def getTests(self):
        return self.tests