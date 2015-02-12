from flask import abort, json
from functools import wraps

def ValidatedResource(code):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            res = f(*args, **kwargs)
            if (not res):
                abort(code)
            else:
                return res
        return wrapped_f
    return wrap

def JsonResponse(cname, xform=dict):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            res = f(*args, **kwargs)

            jsonArgs = {cname: xform(res)}

            return json.jsonify(**jsonArgs)
        return wrapped_f
    return wrap