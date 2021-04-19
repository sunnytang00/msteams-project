""" Functionality to DMs.

This module demonstrates the creation, removal, invitation, ability to leave and display DMs.
As specified by the COMP1531 Major Project specification.
"""

from src.error import InputError, AccessError
from src.helper import create_dm_name, get_current_user, get_dm, user_is_dm_member, get_user, create_notification, get_react_uids
from src.data.helper import get_dm_count, store_dm, get_dms, update_dm_list, get_users, update_dm_users, store_notification, update_user_stats_dms

def dm_create_v1(auth_user_id, u_ids):
    """Create a DM.
    
    Arguements:
        auth_user_id (int) - an authorised user
        u_ids (int) - contains the user(s) that this DM is, creator would not included on this list
        directed to, and will not include the creator.
    Exceptions:
        InputError when auth_user_id does not refer to a valid user
        InputError when u_id does not refer to a valid user
    
    Return Value:
        Returns a dict containing dm_id and dm_name on success
    """

    if not get_current_user(auth_user_id):
        raise InputError(f"auth_user_id {auth_user_id} does not refer to a valid user")
    
    for u_id in u_ids:
        if not get_current_user(u_id):
            raise InputError(f"u_id {u_id} does not refer to a valid user")

    dm_id = get_dm_count() + 1

    members = [auth_user_id]
    members.extend(u_ids)
    dm_name = create_dm_name(members)
    
    dm = {
        'auth_user_id' : auth_user_id,
        'dm_id': dm_id,
        'dm_name': dm_name,
        'u_ids': members,
        'messages': []
    }
    store_dm(dm)
    update_user_stats_dms(auth_user_id, 'add')
    for u_id in u_ids:
        update_user_stats_dms(u_id, 'add')

    return {
        'dm_id': dm_id,
        'dm_name': dm_name
    }

def dm_list_v1(auth_user_id):
    """List all the dms a user is a part of

    Args:
        auth_user_id (int): id of the user

    Raises:
        AccessError: tthe user is not valid

    Returns:
        dm_list: list of dms that the user is a member of
    """
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")
    
    dm_list = []
    for dm in get_dms():
        if user_is_dm_member(dm['dm_id'], auth_user_id):
            dm_data = get_dm(dm['dm_id'])
            dms = {'dm_id': dm_data['dm_id'], 'name': dm_data['dm_name']}
            dm_list.append(dms)

    return dm_list

def dm_details_v1(auth_user_id, dm_id):
    """Users that are part of this dm can view basic information about the dm

    Args:
        auth_user_id (int): id of authorised user
        dm_id (int): id of the dm

    Raises:
        AccessError: if the user id does not refer to a valid user
        InputError: if the dm_id does not refer to a valid dm
        AccessError: if the authorised user is not a amember of this dm with dm_id

    Returns:
        A dict containing the dm name and members of the dm
    """    
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    dm = get_dm(dm_id)
    members = []
    for u_id in dm['u_ids']:
        user = get_user(u_id)
        members.append(user)
    return {'name': dm['dm_name'], 'members': members}


def dm_messages_v1(auth_user_id, dm_id, start):
    """Given a DM with ID dm_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. 
    This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel, 
    returns -1 in "end" to indicate there are no more messages to load after this return.

    Args:
        auth_user_id (int): id of authorised user
        dm_id (int): id of the dm
        start (int): index of messages

    Raises:
        AccessError: if the user id does not refer to a valid user
        InputError: DM ID is not a valid DM
        AccessError: Authorised user is not a member of DM with dm_id
        InputError: start is greater than the total number of messages in the channel

    Returns:
        A dict containing the messages in the dm, along with the start and end index
    """    
    if not get_current_user(auth_user_id):
        raise AccessError(f"token {auth_user_id} does not refer to a valid user")

    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f"auth_user {auth_user_id} is not member of dm {dm_id}")

    msgs = get_dm(dm_id).get('messages').copy()

    if start > len(msgs):
        raise InputError(f'Start {start} is greater than the total number of messages in the channel')
    msgs.sort(reverse = True, key = Func_for_sort_msg)

    end = -1
    if len(msgs) > (start + 50):
        end = start + 50

    messages  = msgs[start : end]
    if end == -1 and not len(msgs) == 0:
        messages.append(msgs[-1])

    for message in messages:
        message_id = message.get('message_id')
        if auth_user_id in get_react_uids(message_id):
            message['reacts'][0]['is_this_user_reacted'] = True
        if auth_user_id not in get_react_uids(message_id):
            message['reacts'][0]['is_this_user_reacted'] = False

    return {
        'messages': messages,
        'start': start,
        'end': end
    }
def dm_leave_v1(u_id, dm_id):
    """Given a DM ID, the user is removed as a member of this DM

    Args:
        u_id (int): id of a user in the dm
        dm_id (int): id of the dm

    Raises:
        InputError: dm_id is not a valid DM
        AccessError: Authorised user is not a member of DM with dm_id
    """    
    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")
    
    if not user_is_dm_member(dm_id, u_id):
        raise AccessError(f"auth_user {u_id} is not member of dm {dm_id}")

    dm_users = get_dm(dm_id).get('u_ids')
    dm_users.remove(u_id)
    update_dm_users(dm_users, dm_id)
    update_user_stats_dms(u_id, 'remove')


def dm_invite_v1(auth_user_id, dm_id, u_id):
    """Inviting a user to an existing dm

    Args:
        auth_user_id (int): id of authorised user
        dm_id (int): id of the dm
        u_id (int): id of user to be invited to dm

    Raises:
        InputError: dm_id does not refer to an existing dm.
        InputError: u_id does not refer to a valid user. 
        AccessError: the authorised user is not already a member of the DM
    """    
    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")

    if not get_current_user(u_id):
        raise InputError(f"u_id {auth_user_id} does not refer to a valid user")

    if not user_is_dm_member(dm_id, auth_user_id):
        raise AccessError(f'user with auth_user_id {auth_user_id} is not part of the dm')

    dm_users = get_dm(dm_id).get('u_ids')
    dm_users.append(u_id)
    update_dm_users(dm_users, dm_id)

    notification = create_notification(channel_id=-1, dm_id=dm_id, u_id=auth_user_id, added=True)
    store_notification(notification, u_id)
    update_user_stats_dms(u_id, 'add')


def dm_remove_v1(auth_user_id, dm_id):
    """Remove an existing DM. This can only be done by the original creator of the DM.

    Args:
        auth_user_id (int) : id of user trying to remove dm
        dm_id (int): id of dm being removed

    Raises:
        InputError: dm_id does not refer to a valid DM 
        AccessError: the user is not the original DM creator
    """    
    if not get_dm(dm_id):
        raise InputError(f"dm_id {dm_id} does not refer to a valid dm")
    
    if get_dm(dm_id).get('auth_user_id') != auth_user_id:
        raise AccessError(f'auth_user_id with auth_user_id {auth_user_id} is not creator')

    dm_list = get_dms()
    dm = get_dm(dm_id)
    dm_users = get_dm(dm_id).get('u_ids')
    for u_id in dm_users:
        update_user_stats_dms(u_id, 'remove')
    dm_list.remove(dm)
    update_dm_list(dm_list)
    #update_user_stats_dms(auth_user_id, 'remove')



def Func_for_sort_msg(msgs):
    return msgs['message_id']