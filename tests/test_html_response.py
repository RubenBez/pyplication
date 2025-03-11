import pytest

def test_html_parse(client):
    response = client.post("/", data="<p>Hello</p>")
    assert b"Hello" in response.data