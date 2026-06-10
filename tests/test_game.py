"""Unit tests for game logic."""

import unittest
from tictactoe.game import Board, Game


class TestBoard(unittest.TestCase):

    def test_initial_board_is_empty(self) -> None:
        board = Board()
        self.assertIsNone(board.cells[0])
        self.assertTrue(board.is_valid_move(1))

    def test_place_mark(self) -> None:
        board = Board()
        board.place_mark(5, "X")
        self.assertEqual(board.cells[4], "X")
        self.assertFalse(board.is_valid_move(5))

    def test_is_full(self) -> None:
        board = Board()
        for i in range(1, 10):
            board.place_mark(i, "X" if i % 2 else "O")
        self.assertTrue(board.is_full())

    def test_get_winner_row(self) -> None:
        board = Board()
        board.place_mark(1, "X")
        board.place_mark(2, "X")
        board.place_mark(3, "X")
        self.assertEqual(board.get_winner(), "X")

    def test_get_winner_column(self) -> None:
        board = Board()
        board.place_mark(2, "O")
        board.place_mark(5, "O")
        board.place_mark(8, "O")
        self.assertEqual(board.get_winner(), "O")

    def test_get_winner_diagonal(self) -> None:
        board = Board()
        board.place_mark(1, "O")
        board.place_mark(5, "O")
        board.place_mark(9, "O")
        self.assertEqual(board.get_winner(), "O")

    def test_no_winner(self) -> None:
        board = Board()
        board.place_mark(1, "X")
        board.place_mark(2, "O")
        self.assertIsNone(board.get_winner())

    def test_clone(self) -> None:
        board = Board()
        board.place_mark(1, "X")
        clone = board.clone()
        self.assertEqual(clone.cells, board.cells)
        clone.place_mark(2, "O")
        self.assertNotEqual(clone.cells, board.cells)


class TestGame(unittest.TestCase):

    def test_initial_turn_is_human(self) -> None:
        game = Game()
        self.assertEqual(game.current_turn, "X")

    def test_is_over_win(self) -> None:
        game = Game()
        game.make_move(1)  # X
        game.make_move(2)  # O (but O is computer, human goes first, but we'll force)
        # Actually, to simulate a win, we need to set up board directly
        game.board.cells = ["X", "X", "X", None, None, None, None, None, None]
        self.assertTrue(game.is_over())
        self.assertEqual(game.board.get_winner(), "X")


if __name__ == "__main__":
    unittest.main()
