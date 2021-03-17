from json import load, JSONDecodeError

data = {
    'users': [

    ],
    'channels': [

    ],
}

try:
    # update dict with stored data
    with open('src/store.json', 'r') as f:
        stored_data = load(f)

    with open('src/store.json', 'w') as f:
        data['users'] = stored_data.get('users')
        data['channels'] = stored_data.get('channels')

except (FileNotFoundError, JSONDecodeError) as e:
    # initialise file
    with open('src/store.json', 'w') as f:
        pass
