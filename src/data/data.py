from json import load

data = {
    'users': [

    ],
    'channels': [

    ],
}

try:
    with open('store.json', 'r') as f:
        data = load(f)
except FileNotFoundError:
    # initialise file
    with open('store.json', 'w') as f:
        pass
