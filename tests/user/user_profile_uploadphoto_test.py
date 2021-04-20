import pytest
from src.auth import auth_register_v1
from src.user import user_profile_uploadphoto_v1, user_profile_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.admin import admin_user_remove_v1
from tests.helper import helper, clear
from src.config import photo_path
"""
@clear
def test_invalid_img_url(helper):
    auth_user_id = helper.register_user(1)
    url = photo_path + 'phototest1'
    x_start = 0
    y_start = 0
    x_end = 3
    y_end = 3
    with pytest.raises(InputError) as e:
        user_profile_uploadphoto_v1(auth_user_id, url, x_start, y_start, x_end, y_end)
        assert "img_url returns an HTTP status other than 200." in str(e)
@clear
def test_wrong_dimension(helper):
    auth_user_id = helper.register_user(1)
    url = photo_path + 'phototest1.jpg'
    x_start = 0
    y_start = 0
    x_end = 10000
    y_end = 10000
    with pytest.raises(InputError) as e:
        user_profile_uploadphoto_v1(auth_user_id, url, x_start, y_start, x_end, y_end)
        assert "any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URLs." in str(e)
@clear
def test_img_not_jpg(helper):
    auth_user_id = helper.register_user(1)
    url = photo_path + 'phototest2.png'
    x_start = 0
    y_start = 0
    x_end = 5
    y_end = 5
    with pytest.raises(InputError) as e:
        user_profile_uploadphoto_v1(auth_user_id, url, x_start, y_start, x_end, y_end)
        assert "Image uploaded is not a JPG." in str(e)

def test_invalid_token(helper):
    auth_user_id = 10
    url = photo_path + 'phototest1.png'
    x_start = 0
    y_start = 0
    x_end = 1000
    y_end = 1000
    with pytest.raises(AccessError) as e:
        user_profile_uploadphoto_v1(auth_user_id, url, x_start, y_start, x_end, y_end)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e)
"""