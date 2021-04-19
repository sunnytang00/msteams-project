import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_details_v1, dm_messages_v1
from src.message import message_senddm_v1
from tests.helper import clear, useless_message

@clear
def test_no_msg_in_dm():
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    start = 0

    expected = {'messages': [], 'start': 0, 'end': -1}

    msgs = dm_messages_v1(auth_user_id, dm_id, start)

    assert expected == msgs

@clear
def test_few_msg_in_dm():
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    msgs = ['1', '2', '3', '4', '5']

    start = 0

    for msg in msgs:
        message_senddm_v1(auth_user_id, dm_id, msg)
    messages = dm_messages_v1(auth_user_id, dm_id, start)
    assert messages['messages'][0]['message'] == '5' and messages['end'] == -1

@clear
def test_many_msg_in_dm():
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    msgs = []
    msgs.append("orange")
    msgs.extend(useless_message(50))
    msgs.append("last")

    start = 0

    for msg in msgs:
        message_senddm_v1(auth_user_id, dm_id, msg)
    
    messages = dm_messages_v1(auth_user_id, dm_id, start)
    assert "last" in [msg['message'] for msg in messages['messages']] \
            and "orange" not in [msg['message'] for msg in messages['messages']] \
            and messages['end'] == 50
@clear
def test_invalid_token():
    #register a user
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    #make a invalid token
    u_id = auth_user_id + 10

    with pytest.raises(AccessError) as e:
        dm_messages_v1(u_id, dm_id, 0)
        assert f"token {u_id} does not refer to a valid user" in str(e.value)

@clear
def test_not_valid_dm_id():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    # make a invalid dm_id
    dm_id = 10

    with pytest.raises(InputError) as e:
        dm_messages_v1(auth_user_id, dm_id, 0)
        assert f"dm_id {dm_id} does not refer to a valid dm" in str(e.value)

@clear
def start_greater_than_end_of_message():
    #register users
    user = auth_register_v1(email='harrypotter7@gmail.com',
                            password='qw3rtyAppl3s@99',
                            name_first='Harry',
                            name_last='Potter')

    auth_user_id = user.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    start = 100

    with pytest.raises(InputError) as e:
        dm_messages_v1(auth_user_id, dm_id, start)
        assert f"the message in dm is less than {start}" in str(e.value)

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

    auth_user_id = user.get('auth_user_id')
    user2_id = user2.get('auth_user_id')

    #create a dm
    dm_id = dm_create_v1(auth_user_id, []).get('dm_id')

    with pytest.raises(AccessError) as e:
        dm_messages_v1(user2_id, dm_id, 0)
        assert f"auth_user {user2} is not member of dm {dm_id}" in str(e.value)