import requests
from json import loads
from src.config import url
from http_tests.helper import clear, helper
from urllib.parse import urlencode
from src.config import photo_path

@clear
def test_invalid_img_url(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1

    img_url = photo_path + 'phototest1'
    x_start = 0
    y_start = 0
    x_end = 3
    y_end = 3
    response = requests.post(url + "/user/profile/uploadphoto/v1", json = {
        "token": token1,
        "img_url": img_url,
        "x_start": x_start,
        "y_start": y_start,
        "x_end": x_end,
        "y_end": y_end
    })
    assert response.status_code == 400

@clear
def test_wrong_dimension(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1
    img_url = photo_path + 'phototest1.png'
    x_start = 0
    y_start = 0
    x_end = 10000
    y_end = 10000
    response = requests.post(url + "/user/profile/uploadphoto/v1", json = {
        "token": token1,
        "img_url": img_url,
        "x_start": x_start,
        "y_start": y_start,
        "x_end": x_end,
        "y_end": y_end
    })
    assert response.status_code == 400
@clear
def test_img_not_jpg(helper):
    user1 = helper.register_user(1)
    token1 = user1.json().get('token')
    assert token1
    img_url = photo_path + 'phototest2.png'
    x_start = 0
    y_start = 0
    x_end = 5
    y_end = 5
    response = requests.post(url + "/user/profile/uploadphoto/v1", json = {
        "token": token1,
        "img_url": img_url,
        "x_start": x_start,
        "y_start": y_start,
        "x_end": x_end,
        "y_end": y_end
    })
    assert response.status_code == 400