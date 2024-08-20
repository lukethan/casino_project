import pytest
from youpick.db import get_db

def test_index(client, auth):
    response = client.get('/', follow_redirects=True)
    assert b"Username" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Logout' in response.data
    assert b'You Pick!' in response.data
    assert b'Welcome' in response.data
    # assert b'test\nbody' in response.data
    # assert b'href="/1/update"' in response.data