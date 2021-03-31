import pytest

from src.base.error import InputError, AccessError
from src.base.auth import auth_register_v1
from src.base.other import clear_v1
from src.base.dm import dm_create, dm_details_v1, dm_messages_v1
from tests.helper import clear

'''
This function is to abstract the msgs on the dm, some tests need to send msg to dm and 
therefore should add tests after messsage_senddm() finished
'''

@clear
def test_no_msg_in_dm():
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create(user_id, [user_id]).get('dm_id')

    start = 0

    expected = {'messages': [], 'start': 0, 'end': -1}

    msgs = dm_messages_v1(user_id, dm_id, start)

    assert expected == msgs

@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create(user_id, [user_id]).get('dm_id')

    #make a invalid token
    u_id = user_id + 10

    with pytest.raises(AccessError) as e:
        dm_messages_v1(u_id, dm_id, 0)
        assert f"token {u_id} does not refer to a valid user" in str(e)

@clear
def test_not_valid_dm_id():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    user_id = user.get('auth_user_id')

    # make a invalid dm_id
    dm_id = 10

    with pytest.raises(InputError) as e:
        dm_messages_v1(user_id, dm_id, 0)
        assert f"dm_id {dm_id} does not refer to a valid dm" in str(e)

@clear
def start_greater_than_end_of_message():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create(user_id, [user_id]).get('dm_id')

    start = 100

    with pytest.raises(InputError) as e:
        dm_messages_v1(user_id, dm_id, start)
        assert f"the message in dm is less than {start}" in str(e)

@clear 
def test_auth_user_not_member():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')
    user2 = auth_register_v1(email='harrypotter@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')

    #create a dm
    dm_id = dm_create(user_id, [user_id]).get('dm_id')

    with pytest.raises(AccessError) as e:
        dm_messages_v1(user2_id, dm_id, 0)
        assert f"auth_user {user2} is not member of dm {dm['dm_id']}" in str(e)