import pytest
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_addowner_v1, channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from tests.helper import helper, clear

@clear
def test_valid_input(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch_name = "big fish"
    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']
    channel_addowner_v1(auth_user_id, ch_id, auth_user_id_2)

    ch_details = channel_details_v1(auth_user_id, ch_id)

    assert auth_user_id_2 in [user['u_id'] for user in ch_details['owner_members']]

@clear
def test_valid_input2(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch_name = "big fish"
    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']
    channel_join_v1(auth_user_id_2, ch_id)

    channel_addowner_v1(auth_user_id, ch_id, auth_user_id_2)

    ch_details = channel_details_v1(auth_user_id, ch_id)

    assert auth_user_id_2 in [user['u_id'] for user in ch_details['owner_members']]

@clear
def test_invalid_channel_id(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch_id = 3

    with pytest.raises(InputError) as e: 
        channel_addowner_v1(auth_user_id, ch_id, auth_user_id_2)
        assert f'channel_id {ch_id} does not refer to a valid channel' in str(e.value)

@clear
def test_invalid_token(helper):
    auth_user_id = helper.register_user(1)

    ch_name = "big fish"

    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']

    auth_user_id_2 = helper.register_user(2)

    with pytest.raises(AccessError) as e: 
        channel_addowner_v1(auth_user_id + 10, ch_id, auth_user_id_2)
        assert f'token {auth_user_id} does not refer to a valid token' in str(e.value)

@clear
def test_auth_user_has_no_access(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)
    auth_user_id_3 = helper.register_user(3)

    ch_name = "big fish"

    ch_id = channels_create_v1(auth_user_id_2, ch_name, True)['channel_id']

    with pytest.raises(AccessError) as e: 
        channel_addowner_v1(auth_user_id_3, ch_id, auth_user_id)
        assert f'Auth_user with id {auth_user_id} is not owner of channel or owner of dreams' in str(e.value)

@clear
def test_is_already_owner(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)

    ch_name = "big fish"
    ch_id = channels_create_v1(auth_user_id, ch_name, True)['channel_id']
    channel_addowner_v1(auth_user_id, ch_id, auth_user_id_2)

    with pytest.raises(InputError) as e: 
        channel_addowner_v1(auth_user_id, ch_id, auth_user_id_2)
        assert f' user with ID {auth_user_id_2} is arleady owner of channel' in str(e.value)

@clear
def test_auth_user_is_owner_of_Dream(helper):
    auth_user_id = helper.register_user(1)
    auth_user_id_2 = helper.register_user(2)
    auth_user_id_3 = helper.register_user(3)

    ch_name = "big fish"

    ch_id = channels_create_v1(auth_user_id_2, ch_name, True)['channel_id']

    channel_addowner_v1(auth_user_id, ch_id, auth_user_id_3)

        #check the details of channel
    ch_details = channel_details_v1(auth_user_id_2, ch_id)

    assert auth_user_id_3 in [user['u_id'] for user in ch_details['owner_members']]

'''
more test needed when add permission functions finished
'''