def test_get_upcoming_meetups(main):
    """test view upcoming meetups"""
    res = main.get('/api/v2/meetups/upcoming')
    assert res.status_code == 200
