def test_testdb(cnxn, cursor):
    """tests the test db connection"""
    assert cnxn
    cnxn_parameters = cnxn.get_dsn_parameters()
    assert cnxn_parameters.get("dbname") == "questioner_test"
    assert cursor
