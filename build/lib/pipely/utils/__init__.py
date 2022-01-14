from collections import Mapping

def deep_update(source, overrides):
    """Update a nested dictionary or similar mapping. Modify `source` in place."""
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            # if key not in source:
            #     source[key] = {}
            # s_c = source[key]
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source