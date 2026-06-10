"""AI opponent using minimax algorithm."""

from typing import Optional, Tuple
from tictactoe.game import Board


class AI:
    """AI player that computes optimal moves via minimax."""

    def __init__(self, mark: str = "O", opponent_mark: str = "X") -> None:
        self.mark = mark
        self.opponent_mark = opponent_mark

    def get_move(self, board: Board) -> int:
        """Determine the best move for the AI player."""
        _, best_move = self._minimax(board, self.mark)
        return best_move

    def _minimax(self, board: Board, player: str, depth: int = 0) -> Tuple[int, Optional[int]]:
        """Recursive minimax evaluation.

        Returns (score, best_move).  Score is from the perspective of the AI player.
        """
        winner = board.get_winner()
        if winner == self.mark:
            return 10 - depth, None
        elif winner == self.opponent_mark:
            return depth - 10, None
        elif board.is_full():
            return 0, None

        best_score = -float("inf") if player == self.mark else float("inf")
        best_move = None

        for move in board.get_available_moves():
            new_board = board.clone()
            new_board.place_mark(move, player)
            next_player = self.opponent_mark if player == self.mark else self.mark
            score, _ = self._minimax(new_board, next_player, depth + 1)

            if player == self.mark:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move
