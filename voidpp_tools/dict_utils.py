import collections

def recursive_update(target, source):
    for key, val in source.items():
        if isinstance(val, collections.Mapping) and key in target and isinstance(target[key], collections.Mapping):
            target[key] = recursive_update(target[key], val)
        elif isinstance(val, collections.Sequence) and key in target and isinstance(target[key], collections.Sequence):
            target[key] += source[key]
        else:
            target[key] = source[key]
    return target
