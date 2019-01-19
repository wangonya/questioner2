import pytest

import app


@pytest.fixture
def main():
    """setup testing module with testing config"""
    test = app.create_app("dev")
    return test.test_client()
