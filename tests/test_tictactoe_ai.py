import pytest
from unittest.mock import MagicMock
from tictactoe.ai import AI


class TestAIInitialization:
    def test_default_marks(self):
        ai = AI()
        assert ai.mark == "O"
        assert ai.opponent_mark == "X"

    def test_custom_marks(self):
        ai = AI(mark="A", opponent_mark="B")
        assert ai.mark == "A"
        assert ai.opponent_mark == "B"


class TestGetMove:
    def test_single_available_move_returns_that_move(self):
        board = MagicMock()
        board.get_available_moves.return_value = [5]
        board.get_winner.return_value = None
        board.is_full.return_value = False
        # No need to simulate clone/place_mark because only one move exists;
        # any loop will pick the only move.
        ai = AI()
        move = ai.get_move(board)
        assert move == 5

    def test_chooses_winning_move_over_losing(self):
        ai = AI(mark="O", opponent_mark="X")
        board = MagicMock()
        board.get_available_moves.return_value = [1, 2]
        board.get_winner.return_value = None
        board.is_full.return_value = False

        # After playing move 1, the board is a win for AI
        board_win = MagicMock()
        board_win.get_winner.return_value = ai.mark
        board_win.is_full.return_value = False
        board_win.get_available_moves.return_value = [2]

        # After playing move 2, the board is a win for opponent
        board_lose = MagicMock()
        board_lose.get_winner.return_value = ai.opponent_mark
        board_lose.is_full.return_value = False
        board_lose.get_available_moves.return_value = [1]

        board.clone.side_effect = [board_win, board_lose]

        move = ai.get_move(board)
        assert move == 1

    def test_no_available_moves_returns_none(self):
        board = MagicMock()
        board.get_available_moves.return_value = []
        board.get_winner.return_value = None
        board.is_full.return_value = True
        ai = AI()
        move = ai.get_move(board)
        assert move is None


class TestMinimaxBaseCases:
    @pytest.mark.parametrize(
        "winner, is_full, expected_score",
        [
            ("O", False, 10),   # AI wins
            ("X", False, -10),  # AI loses
            (None, True, 0),    # draw (board full, no winner)
        ],
    )
    def test_terminal_state_evaluation(self, winner, is_full, expected_score):
        ai = AI()  # defaults: mark="O", opponent="X"
        board = MagicMock()
        board.get_winner.return_value = winner
        board.is_full.return_value = is_full
        board.get_available_moves.return_value = []  # not used in terminal path

        score, move = ai._minimax(board, ai.mark, depth=0)

        assert score == expected_score
        assert move is None  # base cases never return a move