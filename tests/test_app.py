def test_app(main):
    """test root route -- base test just to confirm things are working"""
    res = b"Hello World!"
    response = main.get('/api/v2/')
    assert res in response.data
    assert response.status_code == 200
