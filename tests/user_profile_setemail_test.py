import pytest
from src.base.auth import auth_register_v1
from src.base.user import user_profile_setname_v1
from src.base.other import clear_v1
from src.base.error import InputError
from tests.helper import helper
from src.base.user import user_profile_v1
from src.base.user import user_profile_setemail_v1

def test_single_user():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1
    u_id = 1

    new_email = 'harrypotter1@gmail.com'

    user_profile_setemail_v1(auth_user_id, new_email)

    assert user_profile_v1(auth_user_id, u_id).get('user').get('email') == new_email

def test_invalid_email():
    
    clear_v1()
    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_email = 'invalidemail!!!'
    
    with pytest.raises(InputError) as e:
        user_profile_setemail_v1(auth_user_id, new_email)
        assert f'Email {email} is not a valid email' in str(e)

def test_email_in_use():
    
    clear_v1()

    email = 'harrypotter@gmail.com'
    password = 'qw3rtyAppl3s@99'
    name_first='Harry'
    name_last='Potter'

    email1 = 'severussnape@gmail.com'
    password1 = 'potter'
    name_first1='Severus'
    name_last1='Snape'

    user = auth_register_v1(email=email,
                            password=password,
                            name_first=name_first,
                            name_last=name_last)

    auth_register_v1(email=email1,
                            password=password1,
                            name_first=name_first1,
                            name_last=name_last1)
    
    auth_user_id = user['auth_user_id']
    assert auth_user_id == 1

    new_email = 'severussnape@gmail.com'
    
    with pytest.raises(InputError) as e:
        user_profile_setemail_v1(auth_user_id, new_email)
        assert f'Email address {email} is already being used by another user' in str(e)

