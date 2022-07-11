
def make_hash(value):
    if isinstance(value, (set, tuple, list)):
        return tuple(map(make_hash, value))
    elif not isinstance(value, dict):
        return hash(value)

    for k, v in value.items():
        value[k] = make_hash(value)

    return hash(tuple(frozenset(sorted(value.items()))))