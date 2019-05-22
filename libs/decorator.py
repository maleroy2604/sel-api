import functools
from libs.strings import gettext


def verify_permission(func):
    @functools.wraps(func)
    def verify_permission_runs_func():
        if id == get_jwt_identity():
            func()
        else:
            return {"message": gettext("not_Allow")}, 500

    return verify_permission_runs_func
