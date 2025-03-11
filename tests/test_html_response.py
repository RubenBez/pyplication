import pytest

def test_html_parse(client):
    response = client.post("/", data="<p>Hello python</p>")
    assert b"Hello python" in response.data