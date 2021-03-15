import requests
from json import loads
from src.base.config import url

def test_register_basic():

    response = requests.post(url + 'auth/register/v2', json = {
        'email' : 'harrypotter@gmail.com',
        'password' : 'dumbledore',
        'name_first' : 'harry',
        'name_last' : 'potter'
    })

    # reading data from response
    data = response.json()
    print(data)
    auth_user_id = data.get('auth_user_id')


    #may need to assert what token is = to? apparently atm should be user_id
    #but not sure
    
    #auth user is 2 as pytest runs auth_login http test first, still need to implement
    #a reset function
    assert auth_user_id == 2
    
 