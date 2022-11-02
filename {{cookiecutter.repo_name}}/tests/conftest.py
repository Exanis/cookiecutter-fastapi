from os import environ
from fastapi.testclient import TestClient
import pytest


environ.setdefault('DEBUG', 'True')


@pytest.fixture(scope='session')
def client():
    from {{cookiecutter.repo_name}}.main import app

    with TestClient(app) as client:
        yield client
