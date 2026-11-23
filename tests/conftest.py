"""Flask test client with isolated session configuration."""
import pytest
from resumeiq import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "testing-only-not-used-in-production"})
    return app.test_client()
