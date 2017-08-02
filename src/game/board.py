import numpy as np

class Board:
    def __init__(self, iDim, jDim):
        tiles = np.zeros( shape = (iDim, jDim), dtype = int)
        self.tiles = tiles

    def set(self, i, j, val):
        self.tiles[i][j] = val

    def get(self, i, j):
        return self.tiles[i][j]
