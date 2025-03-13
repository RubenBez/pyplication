import pytest

def test_route_works(client):
    response = client.post("/", data="<p>Hello python</p>")
    assert response.status_code == 200