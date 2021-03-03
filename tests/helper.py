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
            },
            {
                'email': 'yunus24234@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Yunus',
                'name_last': 'Stafford'
            },
            {
                'email': 'joyce.h2@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Joyce',
                'name_last': 'Hodson'
            },
            {
                'email': 'devonte2222@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Devonte',
                'name_last': 'Mcneill'
            },
            {
                'email': 'rocharocha@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Fraser',
                'name_last': 'Rocha'
            },
            {
                'email': 'g_s100008@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Grainger',
                'name_last': 'Siobhan'
            },
            {
                'email': 'bull9949@gmail.com',
                'password': 'qw3rtyAppl3s@99',
                'name_first': 'Simran',
                'name_last': 'Bull'
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
                'name': 'Green or red apples?',
                'is_public': True
            },
            {
                'auth_user_id': 5,
                'name': 'Channel one',
                'is_public': True
            },
            {
                'auth_user_id': 6,
                'name': 'Watermelons',
                'is_public': True
            },
            {
                'auth_user_id': 7,
                'name': 'UNSW Chat',
                'is_public': True
            },
            {
                'auth_user_id': 8,
                'name': 'Chicken Nuggets Channel',
                'is_public': True
            },
            {
                'auth_user_id': 9,
                'name': 'Hungry Jacks Fan Club',
                'is_public': True
            },
            {
                'auth_user_id': 10,
                'name': 'Chicken Lovers',
                'is_public': False
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