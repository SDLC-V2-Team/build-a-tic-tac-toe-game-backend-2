"""Core game logic for Tic Tac Toe."""

from typing import List, Optional, Tuple


class Board:
    """Represents the Tic Tac Toe board.

    Internally uses a list of 9 elements: indices 0-8 correspond to
    the board positions:
        0 | 1 | 2
        ---+---+---
        3 | 4 | 5
        ---+---+---
        6 | 7 | 8
    """

    def __init__(self) -> None:
        self.cells: List[Optional[str]] = [None] * 9

    def display(self) -> str:
        """Return a string representation of the board."""
        rows = []
        for i in range(3):
            row_cells = []
            for j in range(3):
                idx = i * 3 + j
                cell = self.cells[idx] if self.cells[idx] is not None else str(idx + 1)
                row_cells.append(cell)
            rows.append(" | ".join(row_cells))
        return "\n---+---+---\n".join(rows)

    def is_full(self) -> bool:
        """Return True if the board has no empty cells."""
        return all(cell is not None for cell in self.cells)

    def is_valid_move(self, position: int) -> bool:
        """Check if a move (1-9) is valid and the cell is empty."""
        if position < 1 or position > 9:
            return False
        return self.cells[position - 1] is None

    def place_mark(self, position: int, mark: str) -> None:
        """Place the given mark at position (1-9)."""
        if not self.is_valid_move(position):
            raise ValueError(f"Invalid move: position {position}")
        self.cells[position - 1] = mark

    def get_winner(self) -> Optional[str]:
        """Return the winner ('X' or 'O') if there is one, else None."""
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]               # diagonals
        ]
        for line in lines:
            a, b, c = line
            if self.cells[a] is not None and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def clone(self) -> "Board":
        """Return a deep copy of the board."""
        new_board = Board()
        new_board.cells = self.cells[:]
        return new_board

    def get_available_moves(self) -> List[int]:
        """Return list of positions (1-9) that are empty."""
        return [i + 1 for i, cell in enumerate(self.cells) if cell is None]


class Game:
    """Manages the game state and turn logic."""

    def __init__(self, human_mark: str = "X", computer_mark: str = "O") -> None:
        self.board = Board()
        self.human_mark = human_mark
        self.computer_mark = computer_mark
        self.current_turn = human_mark  # human goes first

    def is_over(self) -> bool:
        """Return True if the game is over (win or tie)."""
        return self.board.get_winner() is not None or self.board.is_full()

    def make_move(self, position: int) -> None:
        """Place current player's mark and switch turn."""
        self.board.place_mark(position, self.current_turn)
        self.current_turn = self.computer_mark if self.current_turn == self.human_mark else self.human_mark
