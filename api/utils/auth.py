from flask import request, abort
from config import ADMIN_API_KEY

def require_api_key(fn):
    def wrapper(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != ADMIN_API_KEY:
            abort(401)
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
