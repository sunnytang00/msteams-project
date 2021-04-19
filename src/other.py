from src.data.helper import clear_data, get_data
from src.helper import user_is_channel_member
from src.error import InputError, AccessError

def clear_v1():
    """ Resets the internal data of the application to it's initial state
        
    Return Value:
        Returns ｛｝ (dict)
    """
    clear_data()

def search_v1(auth_user_id, query_str):

    """Given a query string, return a collection of messages 
    in all of the channels/DMs that the user has joined that match the query

    Raises:
        InputError: query_str is above 1000 characters
        InputError: auth_user is not valid
        InputError: auth_user is not valid
        InputError: empty query string

    Returns:
        List of dictionaries, where each dictionary contains types 
        { message_id, u_id, message, time_created }
    """    
    data = get_data()

    if type(auth_user_id) is not int:
        raise InputError(f'Auth_user_id is not real')
    
    if auth_user_id <= 0:
        raise InputError(f'Auth_user_id is not real')

    if query_str == "":
        raise InputError(f'Query string is empty')
    
    if len(query_str) > 1000:
        raise InputError(f'Query string is too long')
    
    message_matches = []

    #for loop to check if the user is actually in any channels or has any dms

    for channel in data['channels']:

        channel_id = channel['channel_id']
        
        if user_is_channel_member(channel_id, auth_user_id) is True:

            for message in channel['messages']:

                if query_str in message['message']:

                    message_to_add =  {
                        'message_id': message['message_id'],
                        'u_id': message['u_id'],
                        'message': message['message'],
                        'time_created': message['time_created'],
                        }

                    message_matches.append(message_to_add)
    
    return message_matches