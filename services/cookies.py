# Cookie Variables
ADD_BOOK_COOKIE = 'add_book_message'
BOOK_COOKIE = 'book_message'
JOIN_COOKIE = 'join_message'
LOGIN_COOKIE = 'login_message'
EDIT_ACC_COOKIE = 'edit_acc_message'
AUTH_COOKIE = 'auth_user_id'
ACCTYPE_COOKIE = 'acc_type'

from config import AUTH_COOKIE_SECRET
from bottle import request, response

def get_auth_cookie():
    return request.get_cookie(AUTH_COOKIE, secret=AUTH_COOKIE_SECRET)

def del_auth_cookie():
    response.delete_cookie(AUTH_COOKIE)

def get_acctype_cookie():
    return request.get_cookie(ACCTYPE_COOKIE, secret=AUTH_COOKIE_SECRET)

def get_cookie(cookie_name, cookie_path=None):
    message = request.get_cookie(cookie_name)

    if message:
        if cookie_path is not None:
            response.delete_cookie(cookie_name, path=cookie_path)
        else:
            response.delete_cookie(cookie_name)
        return message
    else:
        return ""


def set_cookie(cookie_name, value, cookie_path=None):
    if cookie_path is None:
        response.set_cookie(cookie_name, value)
    else:
        response.set_cookie(cookie_name, value, path=cookie_path)

    return
