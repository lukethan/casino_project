import os
import tempfile

import pytest
from youpick import create_app
from youpick.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

#Pulled from Flask tutorial to set up testing environment
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    #Points to a temporary test, allowing db to have test values instead of true path

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
#Creates temporary client to run tests through rather than the server 


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
#Allows for testing CLI commands

#Pytest matches fixtures with test functions. The client is the argument passed to test function

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
#passes login check to each test using the class written above