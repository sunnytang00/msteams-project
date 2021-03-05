import pytest
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from .testing_data import testing_data

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

            channels_create_v1(auth_user_id=channel['auth_user_id'],
                                name=channel['name'],
                                is_public=channel['is_public']
                                )
        return

@pytest.fixture
def helper():
    return Helper