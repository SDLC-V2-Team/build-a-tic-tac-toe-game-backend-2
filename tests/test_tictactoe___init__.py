import pytest

def test_import_package():
    """Happy path: package can be imported without error."""
    import tictactoe
    assert tictactoe is not None

def test_import_nonexistent_submodule():
    """Error path: importing a non-existent member raises ImportError."""
    with pytest.raises(ImportError):
        from tictactoe import nonexistent

def test_package_path_exists():
    """Edge: package has the __path__ attribute."""
    import tictactoe
    assert hasattr(tictactoe, '__path__')

def test_package_name():
    """Edge: package __name__ is correct."""
    import tictactoe
    assert tictactoe.__name__ == 'tictactoe'