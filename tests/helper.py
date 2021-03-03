import pytest
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1

class Helper:
    test_data = {
        'users': [
            {
                'email': 'harrypotter@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Harry',
                'name_last': 'Potter'
            },
            {
                'email': 'bobsmith7@gmail.com',
                'password': 'K0zR0xopjfv',
                'name_first': 'Bob',
                'name_last': 'Smith'
            },
            {
                'email': 'gw9999@gmail.com',
                'password': 'K0zvR0xopjfv',
                'name_first': 'Wiktoria',
                'name_last': 'Guerrero'
            },
            {
                'email': 'w3rren444@gmail.com',
                'password': 'K0z423xopjfv',
                'name_first': 'Rhydian',
                'name_last': 'Warren'
            }
        ],
        'channels': [
            {
                'auth_user_id': 1,
                'name': 'A very good channel name',
                'is_public': True
            },
            {
                'auth_user_id': 2,
                'name': 'A very good channel name',
                'is_public': True
            },
            {
                'auth_user_id': 3,
                'name': 'Spaceships are cool',
                'is_public': False
            },
            {
                'auth_user_id': 4,
                'name': 'Wine Connoisseur\'s',
                'is_public': True
            },

        ],
    }

    @staticmethod
    def register_users(quantity: int):
        """Register one to many new users for testing purposes 

        Arguments:
            quantity (int) - The amount of users that will be registered.
    
        Return Value:
            Returns None
        """
        for count, user in enumerate(Helper.test_data['users']):
            if quantity == count:
                break

            auth_register_v1(email=user['email'],
                            password=user['password'],
                            name_first=user['name_first'],
                            name_last=user['name_last']
                            )
        return

    @staticmethod
    def create_channels(quantity: int):
        """Register one to many channels testing purposes 

        Arguments:
            quantity (int) - The amount of channels that will be registered
    
        Return Value:
            Returns None
        """
        for count, channel in enumerate(Helper.test_data['channels']):
            if quantity == count + 1:
                break

            channels_create_v1(auth_user_id=channel['auth_user_id'],
                                name=channel['name'],
                                is_public=channel['is_publc']
                                )
        return

@pytest.fixture
def helper():
    return Helper