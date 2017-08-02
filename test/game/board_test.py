from game.board import Board

def test_board_constructor():
    board = Board(5, 5)
    assert board.tiles.ndim == 2
    assert board.tiles.shape == (5, 5)
    assert board.tiles.dtype.name == "int32"

def test_board_setget():
    board = Board(5, 5)
    board.set(0, 0, 10)
    assert board.get(0, 0) == 10
