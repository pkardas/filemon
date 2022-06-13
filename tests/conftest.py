import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture()
def api_test_client():
    return TestClient(app)
