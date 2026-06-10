import pytest
from unittest.mock import patch, MagicMock
from tictactoe.cli import main


def test_human_wins(capsys):
    mock_game = MagicMock()
    mock_board = MagicMock()
    mock_game.board = mock_board
    mock_game.human_mark = 'X'
    mock_game.computer_mark = 'O'
    mock_game.current_turn = 'X'
    mock_game.is_over.side_effect = [False, True]
    mock_board.display.return_value = "board"
    mock_board.is_valid_move.return_value = True
    mock_board.get_winner.return_value = 'X'

    with patch('tictactoe.cli.Game', return_value=mock_game), \
         patch('tictactoe.cli.AI'), \
         patch('builtins.input', return_value='5'):
        main()

    out = capsys.readouterr().out
    assert "Congratulations! You win!" in out


def test_computer_wins(capsys):
    mock_game = MagicMock()
    mock_board = MagicMock()
    mock_game.board = mock_board
    mock_game.human_mark = 'X'
    mock_game.computer_mark = 'O'
    mock_game.current_turn = 'O'
    mock_game.is_over.side_effect = [False, True]
    mock_board.display.return_value = "board"
    mock_board.is_valid_move.return_value = True
    mock_board.get_winner.return_value = 'O'

    mock_ai = MagicMock()
    mock_ai.get_move.return_value = 7

    with patch('tictactoe.cli.Game', return_value=mock_game), \
         patch('tictactoe.cli.AI', return_value=mock_ai), \
         patch('builtins.input', return_value='1'):  # not used (computer turn)
        main()

    out = capsys.readouterr().out
    assert "Computer wins" in out
    assert "Computer plays 7" in out


def test_draw(capsys):
    mock_game = MagicMock()
    mock_board = MagicMock()
    mock_game.board = mock_board
    mock_game.human_mark = 'X'
    mock_game.computer_mark = 'O'
    mock_game.current_turn = 'X'
    mock_game.is_over.side_effect = [False, True]
    mock_board.display.return_value = "board"
    mock_board.is_valid_move.return_value = True
    mock_board.get_winner.return_value = None

    with patch('tictactoe.cli.Game', return_value=mock_game), \
         patch('tictactoe.cli.AI'), \
         patch('builtins.input', return_value='3'):
        main()

    out = capsys.readouterr().out
    assert "It's a draw!" in out


def test_invalid_input_non_numeric(capsys):
    mock_game = MagicMock()
    mock_board = MagicMock()
    mock_game.board = mock_board
    mock_game.human_mark = 'X'
    mock_game.computer_mark = 'O'
    mock_game.current_turn = 'X'
    # flow: is_over() first -> False, invalid input, continue,
    # is_over() again -> False, valid input -> move, is_over() -> True
    mock_game.is_over.side_effect = [False, False, True]
    mock_board.display.return_value = "board"
    mock_board.is_valid_move.return_value = True
    mock_board.get_winner.return_value = 'X'

    inputs = ['abc', '5']

    with patch('tictactoe.cli.Game', return_value=mock_game), \
         patch('tictactoe.cli.AI'), \
         patch('builtins.input', side_effect=inputs):
        main()

    out = capsys.readouterr().out
    assert "Invalid input. Please enter a number 1-9." in out
    assert "Congratulations! You win!" in out


def test_invalid_move_out_of_range(capsys):
    mock_game = MagicMock()
    mock_board = MagicMock()
    mock_game.board = mock_board
    mock_game.human_mark = 'X'
    mock_game.computer_mark = 'O'
    mock_game.current_turn = 'X'
    mock_game.is_over.side_effect = [False, False, True]
    mock_board.display.return_value = "board"
    mock_board.is_valid_move.side_effect = [False, True]   # first move invalid, second valid
    mock_board.get_winner.return_value = 'X'

    inputs = ['99', '5']

    with patch('tictactoe.cli.Game', return_value=mock_game), \
         patch('tictactoe.cli.AI'), \
         patch('builtins.input', side_effect=inputs):
        main()

    out = capsys.readouterr().out
    assert "That cell is already taken or out of range. Try again." in out
    assert "Congratulations! You win!" in out