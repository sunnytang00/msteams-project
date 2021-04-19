import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from tests.helper import helper, clear
from src.error import AccessError
from src.channel import channel_invite_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1, dm_leave_v1, dm_invite_v1, dm_remove_v1
from src.message import message_send_v1, message_senddm_v1, message_remove_v1
#from src.data.helper import get_data
from src.user import user_stats_v1

@clear
def test_check_one_user_stats(helper):
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    auth_user_id3 = helper.register_user(3)
    channel_id = channels_create_v1(auth_user_id1, 'test', True).get('channel_id')
    assert channel_id == 1
    stats = user_stats_v1(auth_user_id1)

    assert stats.get('channels_joined')[0]['num_channels_joined'] == 1
    channels_create_v1(auth_user_id1, 'test1', False)
    stats = user_stats_v1(auth_user_id1)
    assert stats.get('channels_joined')[0]['num_channels_joined'] == 2
    channels_create_v1(auth_user_id1, 'testagain', True)
    stats = user_stats_v1(auth_user_id1)
    assert stats.get('channels_joined')[0]['num_channels_joined'] == 3
    message_send_v1(auth_user_id1, channel_id, "hello")
    message_id = message_send_v1(auth_user_id1, channel_id, "hello again").get('message_id')
    message_remove_v1(auth_user_id1, message_id)
    channel_invite_v1(auth_user_id1, channel_id, auth_user_id2)
    channel_leave_v1(auth_user_id1, channel_id)
    stats = user_stats_v1(auth_user_id1)
    assert stats.get('channels_joined')[0]['num_channels_joined'] == 2
    assert len(stats.get('channels_joined')[0]['time_stamp']) == 4
    dm_id1 = dm_create_v1(auth_user_id1, [auth_user_id2]).get('dm_id')
    dm_id2 = dm_create_v1(auth_user_id1, [auth_user_id3]).get('dm_id')
    dm_id3 = dm_create_v1(auth_user_id3, [auth_user_id1]).get('dm_id')
    message_senddm_v1(auth_user_id1, dm_id2, "hello dm")
    message_senddm_v1(auth_user_id1, dm_id2, "hello dm again")
    stats1 = user_stats_v1(auth_user_id1)
    stats2 = user_stats_v1(auth_user_id2)
    stats3 = user_stats_v1(auth_user_id3)
    assert stats1.get('dms_joined')[0]['num_dms_joined'] == 3
    assert stats2.get('dms_joined')[0]['num_dms_joined'] == 1
    assert stats3.get('dms_joined')[0]['num_dms_joined'] == 2
    dm_leave_v1(auth_user_id1, dm_id3)
    dm_leave_v1(auth_user_id2, dm_id1)
    stats1 = user_stats_v1(auth_user_id1)
    stats2 = user_stats_v1(auth_user_id2)
    assert len(stats1.get('dms_joined')[0]['time_stamp']) == 4
    assert stats2.get('dms_joined')[0]['num_dms_joined'] == 0
    assert len(stats2.get('dms_joined')[0]['time_stamp']) == 2
    assert stats1.get('messages_sent')[0]['num_messages_sent'] == 4
    assert len(stats1.get('messages_sent')[0]['time_stamp']) == 4
    message_senddm_v1(auth_user_id1, dm_id2, "hello dm again1")
    stats1 = user_stats_v1(auth_user_id1)
    assert stats1.get('messages_sent')[0]['num_messages_sent'] == 5
    assert len(stats1.get('messages_sent')[0]['time_stamp']) == 5
    assert stats2.get('messages_sent')[0]['num_messages_sent'] == 0
    assert len(stats2.get('messages_sent')[0]['time_stamp']) == 0
    stats2 = user_stats_v1(auth_user_id2)
    assert stats2.get('channels_joined')[0]['num_channels_joined'] == 1
    assert len(stats2.get('channels_joined')[0]['time_stamp']) == 1

@clear
def test_correct_involvement_rate(helper):
    auth_user_id1 = helper.register_user(1)
    auth_user_id2 = helper.register_user(2)
    auth_user_id3 = helper.register_user(3)

    channel_id1 = channels_create_v1(auth_user_id1, 'test1', True).get('channel_id')
    dm_create_v1(auth_user_id1, [auth_user_id3])
    message_send_v1(auth_user_id1, channel_id1, "hello")

    channel_id2 = channels_create_v1(auth_user_id2, 'test2', True).get('channel_id')
    dm_create_v1(auth_user_id2, [auth_user_id3])
    message_send_v1(auth_user_id2, channel_id2, "hello")

    stats1 = user_stats_v1(auth_user_id1)
    assert stats1.get('involvement_rate') == 1/2
    stats3 = user_stats_v1(auth_user_id3)
    assert stats3.get('involvement_rate') == 1/3