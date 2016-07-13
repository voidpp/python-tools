from functools import wraps

def confirm_prompt(msg = "Are you sure?", help = "(ok: enter, cancel: ctrl+c)"):
    try:
        raw_input("{} {} ".format(msg, help))
        return True
    except KeyboardInterrupt:
        # for new line
        print('')
        return False

def get_func_defaults(func):
    diff = len(func.func_code.co_varnames) - len(func.func_defaults)
    return {func.func_code.co_varnames[diff+idx]: val for idx, val in enumerate(func.func_defaults)}

def confirm(msg = get_func_defaults(confirm_prompt)['msg'], help = get_func_defaults(confirm_prompt)['help']):

    def decor(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not kwargs.get('iamsure', False) and not confirm_prompt(msg, help):
                return
            func(*args, **kwargs)

        return wrapper

    return decor

