import pytest

from route.route import create_app


@pytest.fixture
def app():

    app = create_app()

    return app
