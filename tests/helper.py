import pytest
import functools
from src.base.channels import channels_create_v1
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
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
        return

    @staticmethod
    def register_user(value: int) -> int:
        """Register one user
        use when you want to register a user but only care about the user id

        Arguments:
            value (int) - select a user to register
    
        Return Value:
            Returns user_id
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
            }
        ]

        if value < 1 or value > len(users):
            raise ValueError(f'{value} is not a valid value')

        user = users[value - 1]
        return auth_register_v1(email=user['email'],
                                password=user['password'],
                                name_first=user['name_first'],
                                name_last=user['name_last']
                            ).get('auth_user_id')

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
        return

    @staticmethod
    def register_channel(value: int, auth_user_id: int) -> int:
        """Register one channel 
        use when you want to register a channel but only care about the channel_id

        Arguments:
            value (int) - select a channel to register
    
        Return Value:
            Returns channel_id
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
            }
        ]

        if value < 1 or value > len(channels):
            raise ValueError(f'{value} is not a valid value')

        channel = channels[value - 1]
        return channels_create_v1(auth_user_id=auth_user_id,
                                    name=channel['name'],
                                    is_public=channel['is_public']
                                ).get('channel_id')


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