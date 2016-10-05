import inspect


def decorator_with_args(decorator_to_enhance):
    def decorator_maker(*args, **kwargs):
        def decorator_wrapper(func):
            return decorator_to_enhance(func, *args, **kwargs)
        return decorator_wrapper
    return decorator_maker


def mrodir(klass):
    mro = inspect.getmro(cls)
    for attr_name in dir(cls):
        # need to look up the actual descriptor, not whatever might be
        # bound to the class. this needs to come from the __dict__ of the
        # declaring class.
        for parent in mro:
            try:
                attr = parent.__dict__[attr_name]
            except KeyError:
                continue
            else:
                break
        else:
            # in case we didn't find the attribute and didn't break above.
            # we should never hit this - it's just here for completeness
            # to exclude the possibility of attr being undefined.
            continue

        yield attr_name, attr
