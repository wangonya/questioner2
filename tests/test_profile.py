from .conftest import admin_get


def test_get_admin_meetups(main):
    """test view upcoming meetups"""
    res = admin_get(main, '/api/v2/admin')
    assert res.status_code == 200


def test_get_user_profile(main):
    """test get user profile"""
    res = admin_get(main, '/api/v2/profile')
    assert res.status_code == 200
