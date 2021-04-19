import pytest
import functools
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.testing_data import testing_data

class Helper:
    @staticmethod
    def register_users(quantity: int) -> None:
        """Register one to many new users
        use when you want to register channels and don't care about any data in each user

        Arguments:
            quantity (int) - The amount of users that will be registered.
    
        Return Value:
            Returns None
        """
        for count, user in enumerate(testing_data['users']):
            if quantity == count:
                break

            auth_register_v1(email=user['email'],
                            password=user['password'],
                            name_first=user['name_first'],
                            name_last=user['name_last']
                            )

    @staticmethod
    def register_user(value: int, email=None, password=None, name_first=None, name_last=None) -> int:
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
            Returns a auth_user_id on success
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

        # if parameter is given use it else get from user dict
        auth_user_id =  auth_register_v1(email=user.get('email') if not email else email,
                                            password=user.get('password') if not password else password,
                                            name_first=user.get('name_first') if not name_first else name_first,
                                            name_last=user.get('name_last') if not name_last else name_last
                                        ).get('auth_user_id')
        return auth_user_id

    @staticmethod
    def get_users_count() -> int:
        return len(testing_data['users'])

    @staticmethod
    def create_channels(quantity: int, auth_user_id: int) -> None:
        """Register one to many channels
        use when you want to register channels and don't care about any data in each channel

        Arguments:
            quantity (int) - The amount of channels that will be registered
    
        Return Value:
            Returns None
        """
        for count, channel in enumerate(testing_data['channels']):
            if quantity == count: 
                break

            channels_create_v1(auth_user_id=auth_user_id,
                                name=channel['name'],
                                is_public=channel['is_public']
                                )

    @staticmethod
    def create_channel(value: int, auth_user_id: str, name = None, is_public = True) -> int:
        """Register one channel.
        Will use "random" but unique (for given value) paramters for ones not given.
        If you need a parameter to be a value in particular you can pass it in as a parameter.

        Arguments:
            value (int) - select a user to register
            auth_user_id (int) - the user's id
            name (str) (optional) - the channel name
            is_public (bool) (optional) - if a channel if public or private
    
        Return Value:
            Returns a channel_id on success
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
            },            {
                'name': 'Space soc',
                'is_public': True
            }
        ]

        if value < 1 or value > len(channels):
            raise ValueError(f'{value} is not a valid value')

        channel = channels[value - 1]
        # if parameter is given use it else get from user dict
        channel_id = channels_create_v1(auth_user_id=auth_user_id,
                                    name=channel.get('name') if not name else name,
                                    is_public=is_public # by default True (for backwards compatibility)
                                ).get('channel_id')
            
        return channel_id

@pytest.fixture
def helper():
    return Helper
    
def clear(func):
    """Resets the internal data of the application to it's initial state before running function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        clear_v1()
        rv = func(*args, **kwargs)
        return rv
    return wrapper

def useless_message(quantity: int) ->None:
    i = 0
    msgs = []
    while i < quantity:
        msgs.append("nothing")
        i += 1
    return msgs