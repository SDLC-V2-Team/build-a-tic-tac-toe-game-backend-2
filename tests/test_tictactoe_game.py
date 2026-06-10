import pytest
from tictactoe.game import Board, Game

def test_initial_board():
    board = Board()
    display = board.display()
    expected_rows = ["1 | 2 | 3", "4 | 5 | 6", "7 | 8 | 9"]
    assert display == "\n---+---+---\n".join(expected_rows)
    assert board.get_available_moves() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert not board.is_full()
    assert board.get_winner() is None

def test_winning_move():
    game = Game(human_mark="X", computer_mark="O")
    game.make_move(1)   # X at 1
    assert game.board.cells[0] == "X"
    assert game.current_turn == "O"
    game.make_move(5)   # O at 5
    assert game.current_turn == "X"
    game.make_move(2)   # X at 2
    game.make_move(9)   # O at 9
    game.make_move(3)   # X at 3 → win
    assert game.board.get_winner() == "X"
    assert game.is_over()

def test_invalid_move_raises_error():
    board = Board()
    with pytest.raises(ValueError, match="Invalid move"):
        board.place_mark(0, "X")
    with pytest.raises(ValueError, match="Invalid move"):
        board.place_mark(10, "X")
    board.place_mark(1, "X")
    with pytest.raises(ValueError, match="Invalid move"):
        board.place_mark(1, "O")

def test_board_clone_independence():
    board = Board()
    board.place_mark(1, "X")
    clone = board.clone()
    assert clone.cells[0] == "X"
    assert clone.get_available_moves() == board.get_available_moves()
    clone.place_mark(2, "O")
    assert clone.cells[1] == "O"
    assert board.cells[1] is None

def test_full_board_tie():
    game = Game()
    moves = [1, 2, 3, 5, 4, 6, 8, 7, 9]   # pattern without winner
    for pos in moves:
        game.make_move(pos)
    assert game.board.is_full()
    assert game.board.get_winner() is None
    assert game.is_over()