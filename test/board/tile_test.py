from board.tile import Tile

def test_tile():
    tile = Tile(0, 1, -1)
    assert tile.i == 0
    assert tile.j == 1
    assert tile.val == -1

    assert tile.toString() == "(0, 1): -1"
