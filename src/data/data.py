from json import load

data = {
    'users': [

    ],
    'channels': [

    ],
}

try:
    # update dict with stored data
    with open('store.json', 'r') as f:
        stored_data = load(f)
        data['users'] = stored_data.get('users')
        data['channels'] = stored_data.get('channels')
except FileNotFoundError:
    # initialise file
    with open('store.json', 'w') as f:
        pass
