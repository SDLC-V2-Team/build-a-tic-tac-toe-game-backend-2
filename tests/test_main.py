import os
import unittest.mock
import runpy
import pytest


def test_entry_point_calls_main():
    """Happy path: running as __main__ should call tictactoe.cli.main once."""
    main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
    with unittest.mock.patch('tictactoe.cli.main') as mock_main:
        runpy.run_path(main_path, run_name='__main__')
        mock_main.assert_called_once()


def test_entry_point_does_not_call_main_when_not_main():
    """Edge case: when script is not run as __main__, main is not called."""
    main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
    with unittest.mock.patch('tictactoe.cli.main') as mock_main:
        runpy.run_path(main_path)
        mock_main.assert_not_called()


def test_entry_point_main_exception_propagates():
    """Error path: an exception from main() propagates up when run as __main__."""
    main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
    with unittest.mock.patch('tictactoe.cli.main', side_effect=RuntimeError("test error")):
        with pytest.raises(RuntimeError, match="test error"):
            runpy.run_path(main_path, run_name='__main__')