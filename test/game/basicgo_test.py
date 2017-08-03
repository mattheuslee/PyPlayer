from game.basicgo import BasicGo

def test_basicgo_constructor():
    basicGo = BasicGo()
    assert basicGo.board.tiles.ndim == 2
    assert basicGo.board.tiles.shape == (basicGo.iDim, basicGo.jDim)
    assert basicGo.board.tiles.dtype.name == "int32" or basicGo.board.tiles.dtype.name == "int64"

def test_basicgo_gameOver():
    basicGo = BasicGo()
    assert basicGo.gameOver() == False
    for i in range(basicGo.numTurns):
        basicGo.set(0, 0, 1)
    assert basicGo.gameOver() == True

def test_basicgo_winner():
    basicGo = BasicGo()
    assert basicGo.winner() == 0
    basicGo.set(0, 0, 1)
    assert basicGo.winner() == 1
    basicGo.set(0, 1, -1)
    assert basicGo.winner() == -1

def test_basicgo_setGet():
    basicGo = BasicGo()
    basicGo.set(0, 0, -1)
    assert basicGo.get(0, 0) == -1

def test_basicgo_checkNorth():
    basicGo = BasicGo()
    basicGo.set(0, 0, -1)
    basicGo.set(1, 0, -1)
    basicGo.set(2, 0, 1)
    assert basicGo.get(0, 0) == 0
    assert basicGo.get(1, 0) == 0

def test_basicgo_checkNorthEast():
    basicGo = BasicGo()
    basicGo.set(0, 2, -1)
    basicGo.set(1, 1, -1)
    basicGo.set(2, 0, 1)
    assert basicGo.get(0, 2) == 0
    assert basicGo.get(1, 1) == 0

def test_basicgo_checkEast():
    basicGo = BasicGo()
    basicGo.set(0, 3, 1)
    basicGo.set(0, 2, -1)
    basicGo.set(0, 1, -1)
    basicGo.set(0, 0, 1)
    assert basicGo.get(0, 2) == 0
    assert basicGo.get(0, 1) == 0

def test_basicgo_checkSouthEast():
    basicGo = BasicGo()
    basicGo.set(3, 3, 1)
    basicGo.set(2, 2, -1)
    basicGo.set(1, 1, -1)
    basicGo.set(0, 0, 1)
    assert basicGo.get(2, 2) == 0
    assert basicGo.get(1, 1) == 0

def test_basicgo_checkSouth():
    basicGo = BasicGo()
    basicGo.set(3, 0, 1)
    basicGo.set(2, 0, -1)
    basicGo.set(1, 0, -1)
    basicGo.set(0, 0, 1)
    assert basicGo.get(2, 0) == 0
    assert basicGo.get(1, 0) == 0

def test_basicgo_checkSouthWest():
    basicGo = BasicGo()
    basicGo.set(2, 0, -1)
    basicGo.set(1, 1, -1)
    basicGo.set(0, 2, 1)
    assert basicGo.get(2, 0) == 0
    assert basicGo.get(1, 1) == 0

def test_basicgo_checkWest():
    basicGo = BasicGo()
    basicGo.set(0, 1, -1)
    basicGo.set(0, 0, -1)
    basicGo.set(0, 2, 1)
    assert basicGo.get(0, 1) == 0
    assert basicGo.get(0, 0) == 0

def test_basicgo_checkNorthWest():
    basicGo = BasicGo()
    basicGo.set(1, 1, -1)
    basicGo.set(0, 0, -1)
    basicGo.set(2, 2, 1)
    assert basicGo.get(1, 1) == 0
    assert basicGo.get(0, 0) == 0