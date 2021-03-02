import re

def valid_email(email):
    """Check if email is valid

    Arguments:
        email (str) - The users email address.

    Return Value:
        Returns bool on regexp evalutaion
    """

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    return re.search(regex, email)