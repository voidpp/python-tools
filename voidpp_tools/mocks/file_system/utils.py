
def override(target):
    def wrapper(func):
        func.target_name = target
        return func
    return wrapper
