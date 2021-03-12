from src.data import data

def clear_v1():
    """ Resets the internal data of the application to it's initial state
        
    Return Value:
        Returns ｛｝ (dict)
    """
    global data
    data['users'] = []
    data['channels'] = []

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
