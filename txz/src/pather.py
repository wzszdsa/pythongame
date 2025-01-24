

class Pather(object):
    def __init__(self):
        self.level = 1
        self.path = []
        self.optPath = []
    
    def startRecord(self,level):
        self.level = level
        self.path = []
        self.optPath = None

        with open("data/path/" + str(level) + ".y","r") as fp:
            path = fp.readlines()[0]
            path = path.split(',')
            self.optPath = [int(p) for p in path]
    
    def addRecord(self,dir):
        self.path.append(str(dir))

    def dumpRecord(self):
        if self.optPath == None or len(self.path) < len(self.optPath):
            line = ','.join(self.path)
            with open("data/path/" + str(self.level) + ".y", "w") as fp:
                fp.write(line)
    
    def getRecord(self):
        return self.optPath or []