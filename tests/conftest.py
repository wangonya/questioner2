import os
import pytest
import psycopg2

from psycopg2.extras import RealDictCursor

import app


@pytest.fixture
def main():
    """setup testing module with testing config"""
    test = app.create_app("testing")

    with test.app_context():
        yield test.test_client()


@pytest.fixture
def cnxn(main):
    """testdb connection fixture"""
    cnxn = psycopg2.connect(os.getenv("TESTING_DB_URI"))
    yield cnxn
    cnxn.close()


@pytest.fixture
def cursor(cnxn):
    """testdb cursor fixture"""
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)
    yield cursor
    cnxn.rollback()
