from src.error import InputError

def echo(input):
    if input == 'echo':
        raise InputError
    return input

