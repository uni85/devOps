from app import mysql

def test_mysql_extension_exists():
    """Check if the MySQL extension is properly bound to the Flask app."""
    assert mysql is not None