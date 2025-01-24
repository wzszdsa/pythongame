class Level(object):
    def __init__(self, level):
        self.level = level
        self.blocks = []
        with open('data/level/' + str(self.level) + '.x', 'r') as f:
            r = 0
            for line in f.readlines():
                col = len(line)
                for c in range(col - 1):
                    if line[c] != '0':
                        self.blocks.append((r, c, int(line[c])))
                r += 1

    def getBlocks(self):
        return self.blocks
