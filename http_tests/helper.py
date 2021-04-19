import pytest
import requests
from src.config import url
import functools
from src.channels import channels_create_v1
from src.auth import auth_register_v1

class Helper:
    @staticmethod
    def register_user(value: int, email=None, password=None, name_first=None, name_last=None) -> requests.models.Response:
        """Register one user.
        Will use "random" but unique (for given value) paramters for ones not given.
        If you need a parameter to be a value in particular you can pass it in as a parameter.

        Arguments:
            value (int) - select a user to register
            email (str) (optional) - the user's email
            password (str) (optional) - the user's password
            name_first (str) (optional) - the user's first name
            name_last (str) (optional) - the user's last name
    
        Return Value:
            Returns a response object
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
            # if parameter is given use it else get from user dict
            'email': user.get('email') if not email else email,
            'password': user.get('password') if not password else password,
            'name_first': user.get('name_first') if not name_first else name_first,
            'name_last': user.get('name_last') if not name_last else name_last
        })

        return response

    @staticmethod
    def create_channel(value: int, token: str, name = None, is_public = True) -> requests.models.Response:
        """Register one channel.
        Will use "random" but unique (for given value) paramters for ones not given.
        If you need a parameter to be a value in particular you can pass it in as a parameter.

        Arguments:
            value (int) - select a user to register
            token (str) - the token used for validation
            name (str) (optional) - the channel name
            is_public (bool) (optional) - if a channel if public or private
    
        Return Value:
            Returns a response object
        """
        channels = [
            {
                'name': 'Harvey N',
                'is_public': True
            },
            {
                'name': 'Bill G',
                'is_public': True
            },
            {
                'name': 'Dog soc',
                'is_public': True
            },
            {
                'name': 'Pancakes',
                'is_public': True
            },            
            {
                'name': 'Space soc',
                'is_public': True
            }
        ]
        if value < 1 or value > len(channels):
            raise ValueError(f'{value} is not a valid value')

        channel = channels[value - 1]

        response = requests.post(url + 'channels/create/v2', json = {
            # if parameter is given use it else get from user dict
            'token': token,
            'name': name if not channel.get('name') else channel.get('name'),
            'is_public': is_public # by default True (for backwards compatibility)
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
