class Tile:
    "Class abstracting a single tile in the game"
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val

    def toString(self):
        return "(" + str(self.i) + ", " + str(self.j) + "): " + str(self.val)
