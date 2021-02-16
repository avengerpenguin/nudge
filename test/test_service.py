import re

import httpretty as httpretty
import hyperspace
import pytest
from laconia import ThingFactory


@pytest.fixture(autouse=True)
def mock_requests_to_use_flask_test_client(request, client):
    def get_callback(http_request, uri, headers):

        r = client.get(uri, **dict(http_request.headers))

        response_headers = {
            "content-type": r["Content-Type"],
        }

        if "Content-Length" in r:
            response_headers["content-length"] = r["Content-Length"]

        response_headers.update(headers)

        return int(r.status_code), response_headers, r.content

    def post_callback(http_request, uri, headers):

        r = client.post(uri, **dict(http_request.headers))

        response_headers = {
            "content-type": r["Content-Type"],
        }

        if "Content-Length" in r:
            response_headers["content-length"] = r["Content-Length"]

        response_headers.update(headers)

        return int(r.status_code), response_headers, r.content

    httpretty.register_uri(httpretty.GET, re.compile(".*"), body=get_callback)
    httpretty.register_uri(
        httpretty.POST, re.compile(".*"), body=post_callback
    )
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


def test_index():
    page = hyperspace.jump("http://example.com/")
    assert page.response.status_code == 200


def test_dump_stuff():
    page = hyperspace.jump("http://example.com/")
    page = page.templates["collect"][0].build({"text": "Buy milk"}).submit()
    page.data.bind("nudge", "http://example.com/apidocs#")
    Thing = ThingFactory(page.data)
    dashboard = Thing(page.response.url)
    users = dashboard.nudge_users
    assert len(users) == 1
    user = list(dashboard.users)[0]
    assert len(user.nudge_stuff) == 1
    assert "Buy milk" in list(user.nudge_stuff)[0].nudge_text
