from functools import wraps
import time
import datetime


def is_loggedIn(func=None, *args, **kwargs):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        return f"Anonymous user not allowed operation on {func.__name__}"
    return wrapper