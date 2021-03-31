import pytest
import functools
from src.base.channels import channels_create_v1
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from tests.testing_data import testing_data

class Helper:
    @staticmethod
    def register_users(quantity: int) -> None:
        """Register one to many new users for testing purposes 

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
    def get_users_count() -> int:
        return len(testing_data['users'])

    @staticmethod
    def create_channels(quantity: int) -> None:
        """Register one to many channels testing purposes 

        Arguments:
            quantity (int) - The amount of channels that will be registered
    
        Return Value:
            Returns None
        """
        for count, channel in enumerate(testing_data['channels']):
            if quantity == count: 
                break

            channels_create_v1(auth_user_id=channel['channel_id'],
                                name=channel['name'],
                                is_public=channel['is_public']
                                )
        return

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