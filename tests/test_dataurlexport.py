"""Package level tests"""

from dataurlexport import __version__


def test_version() -> None:
    """Make sure version matches expected"""
    assert __version__ == "0.2.0"
