"""TODO"""
import requests
import urllib.request
import imgspy
from PIL import Image
from src.config import photo_path, photo_storage_path
from src.helper import get_user
from src.helper import valid_email, valid_password, valid_first_name, valid_last_name, email_exists, \
                            get_handle_str, handle_str_exists, get_current_user
from src.error import InputError, AccessError
from src.data.helper import get_users, update_name_first, update_name_last, update_email, update_handle_str, get_user_stats, get_channels, get_dms, get_valid_msg_ids
from src.data.helper import get_channels, get_dms, get_message_count, store_involvement_rate, update_profile_img_url



def user_profile_v1(auth_user_id, u_id):
    
    user = get_user(u_id)
    if not bool(user):
        raise InputError(f'User with u_id {u_id} is not a valid user')

    email = user.get('email')
    name_first = user.get('name_first')
    name_last = user.get('name_last')
    handle_str = user.get('handle_str')
    profile_img_url = user.get('profile_img_url')
    if not get_current_user(u_id):
        name_first = 'Removed'
        name_last = 'user'

    return {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': handle_str,
            'profile_img_url': profile_img_url
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    

    if not valid_first_name(name_first):
        raise InputError(f'name_first {name_first} is not between 1 and 50 characters inclusively in length')

    if not valid_last_name(name_last):
        raise InputError(f'name_last {name_last} is not between 1 and 50 characters inclusively in length')

    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_name_first(auth_user_id, name_first)
            update_name_last(auth_user_id, name_last)
    return {}

def user_profile_setemail_v1(auth_user_id, email):
    

    if not valid_email(email):
        raise InputError(f'Email {email} is not a valid email')

    if email_exists(email):
        raise InputError(f'Email address {email} is already being used by another user') 
        
    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_email(auth_user_id, email)

    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    

    #need to change to tokens eventually
    if len(handle_str) not in range(3, 21):
        raise InputError(f'Handle string {handle_str} is not between 3 and 20 characters inclusive')

    if handle_str_exists(handle_str):
        raise InputError(f'Handle string {handle_str} is already in use')

    for user in get_users():
        if user['u_id'] == auth_user_id:
            update_handle_str(auth_user_id, handle_str)

    return {
    }

def user_stats_v1(auth_user_id):
    user_stats = get_user_stats(auth_user_id)
    num_channels_joined = user_stats.get('channels_joined')[0].get('num_channels_joined')
    num_dms_joined = user_stats.get('dms_joined')[0].get('num_dms_joined')
    num_messages_sent = user_stats.get('messages_sent')[0].get('num_messages_sent')
    num_dreams_channels = len(get_channels())
    num_dreams_dms = len(get_dms())
    num_dreams_msgs = get_message_count()
    involvement_rate = (num_channels_joined + num_dms_joined + num_messages_sent)/(num_dreams_channels + num_dreams_dms + num_dreams_msgs)
    store_involvement_rate(auth_user_id, involvement_rate)
    user_stats = get_user_stats(auth_user_id)
    return user_stats

def user_profile_uploadphoto_v1(auth_user_id, img_url, x_start, y_start, x_end, y_end):
    if not get_current_user(auth_user_id):
        raise AccessError(f'token {auth_user_id} does not refer to a valid token')

    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError("img_url returns an HTTP status other than 200.")

    img_info = imgspy.info(img_url)
    if img_info.get('type') != 'jpg':
        raise InputError("Image uploaded is not a JPG.")

    img_width = img_info.get('width')
    img_height = img_info.get('height')

    wrong_dimension = False

    if x_start < 0 or x_start > x_end or x_end > img_width:
        wrong_dimension = True
    if y_start < 0 or y_start > y_end or y_end > img_height:
        wrong_dimension = True

    if wrong_dimension:
        raise InputError("any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URLs.")

    user = get_current_user(auth_user_id)
    handle_str = user.get('handle_str')

    user_photo_path = photo_storage_path + handle_str + '.jpg'

    urllib.request.urlretrieve(img_url, user_photo_path)

    photo = Image.open(user_photo_path)
    cropped_photo = photo.crop((x_start, y_start, x_end, y_end))
    cropped_photo.save(user_photo_path)

    url = photo_path + handle_str + '.jpg'

    update_profile_img_url(auth_user_id, url)

    