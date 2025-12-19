import os
from app import app

def test_app_config():
    """Verify that the app picks up default or environment configs."""
    assert app.config['MYSQL_PORT'] == 3306 or 'MYSQL_PORT' not in app.config
    assert app.secret_key == 'super_secret_key'

def test_env_defaults():
    """Ensure host defaults to 127.0.0.1 if not in environment."""
    if 'MYSQL_HOST' not in os.environ:
        assert app.config['MYSQL_HOST'] == '127.0.0.1'