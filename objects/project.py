from re import sub


class Project(object):
    def __init__(self):
        self.id = 'Project'
        self.subjects = []

    def addSubject(self, subject):
        self.subjects.append(subject)
    
    def getSubjects(self):
        return self.subjects