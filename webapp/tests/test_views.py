import pytest
from flask import url_for

from webapp import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class Tests:

    def test_show(self, client):
        assert client.get('/show').status_code == 200

    def test_add(self, client):
        assert client.get('/add/').status_code == 200

    def test_delete(self, client):
        assert client.post('/delete/', data='1').status_code == 302

    def test_update(self, client):
        assert client.get('/2/update/').status_code == 200
