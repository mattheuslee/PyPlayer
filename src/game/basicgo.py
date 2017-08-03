from game.board import Board
from game.player import Player

class BasicGo:
    iDim = 10
    jDim = 10
    numTurns = 500

    score = 0
    turn = 0
    def __init__(self):
        board = Board(self.iDim, self.jDim)
        self.board = board

    def gameOver(self):
        return self.turn == self.numTurns

    def winner(self):
        if self.score > 0:
            return 1
        elif self.score < 0:
            return -1
        else:
            return 0

    def set(self, i, j, player):
        self.turn = self.turn + 1
        if not Player.isPlayer(self.board.get(i, j)):
            self.score = self.score + player
            self.board.set(i, j, player)
            self.checkSurround(i, j, player)

    def get(self, i, j):
        return self.board.get(i, j)

    def checkSurround(self, i, j, player):
        self.checkNorth(i, j, player)
        self.checkNorthEast(i, j, player)
        self.checkEast(i, j, player)
        self.checkSouthEast(i, j, player)
        self.checkSouth(i, j, player)
        self.checkSouthWest(i, j, player)
        self.checkWest(i, j, player)
        self.checkNorthWest(i, j, player)

    def checkNorth(self, iStart, jStart, player):
        i = iStart - 1
        j = jStart
        while i >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
            i = i - 1 # Keep checking for the other player's pieces
        if i != iStart - 1 and (i == -1 or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart - 1
            while i >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i - 1

    def checkNorthEast(self, iStart, jStart, player):
        i = iStart - 1
        j = jStart + 1
        while i >= 0 and j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
            i = i - 1 # Keep checking for the other player's pieces
            j = j + 1
        if i != iStart - 1 and j != jStart + 1 and (i == -1 or j == self.jDim or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart - 1
            j = jStart + 1
            while i >= 0 and j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i - 1
                j = j + 1

    def checkEast(self, iStart, jStart, player):
        i = iStart
        j = jStart + 1
        while j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
            j = j + 1  # Keep checking for the other player's pieces
        if j != jStart + 1 and (j == self.jDim or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            j = jStart + 1
            while j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                j = j + 1

    def checkSouthEast(self, iStart, jStart, player):
        i = iStart + 1
        j = jStart + 1
        while i < self.iDim and j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
            i = i + 1 # Keep checking for the other player's pieces
            j = j + 1
        if i != iStart + 1 and j != jStart + 1 and (i == self.iDim or j == self.jDim or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart + 1
            j = jStart + 1
            while i < self.iDim and j < self.jDim and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i + 1
                j = j + 1

    def checkSouth(self, iStart, jStart, player):
        i = iStart + 1
        j = jStart
        while i < self.iDim and self.board.get(i, j) == Player.otherPlayer(player):
            i = i + 1  # Keep checking for the other player's pieces
        if i != iStart + 1 and (i == self.iDim or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart + 1
            while i < self.iDim and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i + 1

    def checkSouthWest(self, iStart, jStart, player):
        i = iStart + 1
        j = jStart - 1
        while i < self.iDim and j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
            i = i + 1 # Keep checking for the other player's pieces
            j = j - 1
        if i != iStart + 1 and j != jStart - 1 and (i ==self.iDim or j == -1 or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart + 1
            j = jStart - 1
            while i < self.iDim and j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i + 1
                j = j - 1

    def checkWest(self, iStart, jStart, player):
        i = iStart
        j = jStart - 1
        while j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
            j = j - 1  # Keep checking for the other player's pieces
        if j != jStart - 1 and (j == -1 or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            j = jStart - 1
            while j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                j = j - 1

    def checkNorthWest(self, iStart, jStart, player):
        i = iStart - 1
        j = jStart - 1
        while i >= 0 and j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
            i = i - 1 # Keep checking for the other player's pieces
            j = j - 1
        if i != iStart - 1 and j != jStart - 1 and (i == -1 or j == -1 or self.board.get(i, j) == player):
            # There are the other player's pieces and they're closed off
            i = iStart - 1
            j = jStart - 1
            while i >= 0 and j >= 0 and self.board.get(i, j) == Player.otherPlayer(player):
                self.score = self.score - Player.otherPlayer(player)
                self.board.set(i, j, 0)
                i = i - 1
                j = j - 1
