import pytest
import requests
from src.config import url
import functools
from src.base.channels import channels_create_v1
from src.base.auth import auth_register_v1

class Helper:
    @staticmethod
    def register_user(value: int) -> requests.models.Response:
        """Register one user.
        Use when you want to register a user but only care about the user id

        Arguments:
            value (int) - select a user to register
    
        Return Value:
            Returns auth_user_id
        """
        users = [
            {
                'email': 'harrypotter3@gmail.com',
                'password': 'h4bjP9cVIw7FWI',
                'name_first': 'Harrrrry',
                'name_last': 'Pottttter'
            },
            {
                'email': 'marcoslowery@gmail.com',
                'password': '27VRLNZsxmnmIl',
                'name_first': 'Marcos',
                'name_last': 'Lowery'
            },
            {
                'email': 'cadifinch@gmail.com',
                'password': '1tJlH9WIvItbZb',
                'name_first': 'Cadi',
                'name_last': 'Finch'
            },
            {
                'email': 'fletcherparker@gmail.com',
                'password': '0MfdIzEGOr6Jc',
                'name_first': 'Fletcher',
                'name_last': 'Parker'
            },
            {
                'email': 'tomjerry@gmail.com',
                'password': 'ZgeDoajXeZN23',
                'name_first': 'Tom',
                'name_last': 'Jerry'
            }
        ]
        if value < 1 or value > len(users):
            raise ValueError(f'{value} is not a valid value')

        user = users[value - 1]

        response = requests.post(url + 'auth/register/v2', json = {
            'email': user.get('email'),
            'password': user.get('password'),
            'name_first': user.get('name_first'),
            'name_last': user.get('name_last')
        })

        return response

@pytest.fixture
def helper():
    return Helper

def clear(func):
    """Resets the internal data of the application to it's initial state before running function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        requests.delete(url + '/clear/v1', json={})
        rv = func(*args, **kwargs)
        return rv
    return wrapper
