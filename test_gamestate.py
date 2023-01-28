from game_state import GameState


def test_constructor():
    game = GameState()
    assert(game.matrix == [
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1]])


def test_is_cell_in_border():
    game = GameState()
    assert(not game.is_cell_in_border(-1, 0))
    assert(not game.is_cell_in_border(-1, 8))
    assert(not game.is_cell_in_border(-1, -1))
    assert(game.is_cell_in_border(0, 7))
    assert(not game.is_cell_in_border(0, 8))
    assert(not game.is_cell_in_border(0, -1))
    assert(not game.is_cell_in_border(8, 0))
    assert(not game.is_cell_in_border(8, 8))
    assert(not game.is_cell_in_border(8, -1))


def test_is_enemy():
    game = GameState()
    assert(not game.is_enemy(1, 0))
    assert(not game.is_enemy(1, 1))
    assert(game.is_enemy(1, 2))
    assert(not game.is_enemy(1, 3))
    assert(game.is_enemy(1, 4))
    assert(not game.is_enemy(2, 0))
    assert(game.is_enemy(2, 1))
    assert(not game.is_enemy(2, 2))
    assert(game.is_enemy(2, 3))
    assert(not game.is_enemy(2, 4))
    assert(not game.is_enemy(3, 0))
    assert(not game.is_enemy(3, 1))
    assert(game.is_enemy(3, 2))
    assert(not game.is_enemy(3, 3))
    assert(game.is_enemy(3, 4))


def test_is_same():
    game = GameState()
    assert(not game.is_same(1, 0))
    assert(game.is_same(1, 1))
    assert(not game.is_same(1, 2))
    assert(game.is_same(1, 3))
    assert(not game.is_same(1, 4))
    assert(not game.is_same(2, 0))
    assert(not game.is_same(2, 1))
    assert(game.is_same(2, 2))
    assert(not game.is_same(2, 3))
    assert(game.is_same(2, 4))


def test_all_valid_pieces():
    game = GameState()
    assert(game.all_valid_pieces(1) == [(5, 1), (5, 3), (5, 5), (5, 7)])
    assert(game.all_valid_pieces(2) == [(2, 0), (2, 2), (2, 4), (2, 6)])


def test_all_capturing_moves():
    game = GameState()
    game.matrix = [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    assert(game.all_capturing_moves(1) == [(5, 3)])


def test_valid_moves():
    game = GameState()
    game.matrix = [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    assert(game.valid_moves([5, 3]) == [(3, 1)])  # capturing
    assert(game.valid_moves([5, 5]) == [(4, 4), (4, 6)])  # non_capturing


def test_get_capturing_moves():
    game = GameState()
    game.matrix = [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    assert(game.get_capturing_moves([5, 3]) == [(3, 1), (3, 5)])
    assert(game.get_capturing_moves([5, 5]) == [(3, 3)])


def test_get_non_capturing_moves():
    game = GameState()
    game.matrix = [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    assert(game.get_non_capturing_moves([5, 5]) == [(4, 6)])
    assert(game.get_non_capturing_moves([5, 7]) == [(4, 6)])


def test_move_piece():
    game = GameState()
    game.matrix = [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    game.move_piece([5, 1], [4, 2])  # non_capturing move
    assert(game.matrix == [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]])
    game.move_piece([2, 0], [3, 1])  # non_capturing move
    assert(game.matrix == [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]])
    game.move_piece([4, 2], [2, 0])  # capturing move
    assert(game.matrix == [
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [1, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]])


def test_become_king():
    game = GameState()
    game.matrix = [
        [2, 0, 1, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 2, 0, 1, 0, 1]]
    game.become_king()
    assert(game.matrix == [
        [2, 0, 3, 0, 2, 0, 2, 0],  # black king
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 4, 0, 1, 0, 1]])  # red king


def test_check_lose():
    game = GameState()
    game.matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    assert(game.check_lose(2))  # no piece
    game.matrix = [
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]  # has pieces but no valid moves
    assert(game.check_lose(2))


def test_erase_captured_piece():
    game = GameState()
    game.matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]]
    game.erase_captured_piece([5, 7], [3, 5])  # capturing move
    assert(game.matrix == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]])
    game.erase_captured_piece([5, 1], [4, 2])  # non_capturing move
    assert(game.matrix == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1]])
