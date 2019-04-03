from bottle import request, response


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
