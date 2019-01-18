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
def testdb_cnxn(main):
    """testdb connection fixture"""
    testdb_cnxn = psycopg2.connect(os.getenv("TESTING_DB_URI"))
    yield testdb_cnxn
    testdb_cnxn.close()


@pytest.fixture
def testdb_cursor(testdb_cnxn):
    """testdb cursor fixture"""
    testdb_cursor = testdb_cnxn.cursor(cursor_factory=RealDictCursor)
    yield testdb_cursor
    testdb_cnxn.rollback()


@pytest.fixture
def devdb_cnxn(main):
    """devdb connection fixture"""
    devdb_cnxn = psycopg2.connect(os.getenv("DEV_DB_URI"))
    yield devdb_cnxn
    devdb_cnxn.close()


@pytest.fixture
def devdb_cursor(devdb_cnxn):
    """devdb cursor fixture"""
    devdb_cursor = devdb_cnxn.cursor(cursor_factory=RealDictCursor)
    yield devdb_cursor
    devdb_cnxn.rollback()
