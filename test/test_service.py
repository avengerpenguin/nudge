def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.content == 'Hello, World!'


def test_404(client):
    response = client.get('/notreal')
    assert response.status_code == 404

