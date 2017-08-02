class Player:
    def isPlayer(player):
        return player == 1 or player == -1

    def otherPlayer(player):
        if player == 1:
            return -1
        elif player == -1:
            return 1
        else:
            return 0
