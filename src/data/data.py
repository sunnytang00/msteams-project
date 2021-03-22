"""
data = {
    'users': [

    ],
    'channels': [

    ],
}
"""

"""
try:
    # update dict with stored data
    with open(data_path, 'r') as f:
        stored_data = load(f)

    with open(data_path, 'w') as f:
        data['users'] = stored_data.get('users')
        data['channels'] = stored_data.get('channels')

except (FileNotFoundError, JSONDecodeError) as e:
    # initialise file
    with open(data_path, 'w') as f:
        pass

"""