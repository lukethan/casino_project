from youpick import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_test(client):
    response = client.get('/test')
    assert response.data == b'Success!'
    #web app returns byte strings, hence the b