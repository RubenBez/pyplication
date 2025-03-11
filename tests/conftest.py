import pytest
from pyplication import app

@pytest.fixture()
def api_app():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(api_app):
    return app.test_client()


@pytest.fixture()
def runner(api_app):
    return app.test_cli_runner()
