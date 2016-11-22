import httpretty as httpretty
import pytest
import hyperspace
import requests
from laconia import ThingFactory
import re


@pytest.fixture(autouse=True)
def mock_requests_to_use_flask_test_client(request, client):

    def get_callback(http_request, uri, headers):

        r = client.get(uri, **dict(http_request.headers))

        response_headers = {
            'content-type': r['Content-Type'],
        }

        if 'Content-Length' in r:
            response_headers['content-length'] = r['Content-Length']

        response_headers.update(headers)

        return int(r.status_code), response_headers, r.content

    httpretty.register_uri(httpretty.GET, re.compile('.*'), body=get_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.content == 'Hello, World!'


def test_404(client):
    response = client.get('/notreal')
    assert response.status_code == 404


def test_index():
    http = requests.Session()
    http.headers = {'Accept': 'text/turtle'}
    page = hyperspace.jump('http://example.com/', http)
    assert page.response.status_code == 200
