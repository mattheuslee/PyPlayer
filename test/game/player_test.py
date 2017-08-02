from game.player import Player

def test_player_isplayer():
    assert Player.isPlayer(1) == True
    assert Player.isPlayer(-1) == True
    assert Player.isPlayer(0) == False

def test_player_otherplayer():
    assert Player.otherPlayer(1) == -1
    assert Player.otherPlayer(-1) == 1
    assert Player.otherPlayer(0) == 0
