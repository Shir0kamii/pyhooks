from collections import defaultdict
import inspect


def decorator_with_args(decorator_to_enhance):
    """Decorate a decorator that takes arguments to change how it's called

    it allows to change how it's defined. Instead of this defintion :

    def decorator(*outer_args, **outer_kwargs):
        def __inner_decorate(func):
            def __inner_func(*args, **kwargs):
                kwargs.update(outer_kwargs)
                return do_whatever(args + outer_args, **kwargs)
            return __inner_func
        return __inner_decorate

    You can use this form :

    def decorator(func, *outer_args, **outer_kwargs):
        def __inner_func(*args, **kwargs):
            kwargs.update(outer_args)
            return do_whatever(args + outer_args, kwargs)
        return __inner_func
    """
    def decorator_maker(*args, **kwargs):
        def decorator_wrapper(func):
            return decorator_to_enhance(func, *args, **kwargs)
        return decorator_wrapper
    return decorator_maker


def mrodir(cls):
    """Iterate on attributes of a class with respect to MRO"""
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
        else:  # pragma: no cover
            # in case we didn't find the attribute and didn't break above.
            # we should never hit this - it's just here for completeness
            # to exclude the possibility of attr being undefined.
            continue

        yield attr_name, attr


def defaultdict_factory(factory):
    """Factory for defaultdict

    `factory` is a function without parameters instantiating an object

    It returns a function without parameter that instantiate a defaultdict with
    `factory` as argument

    This function can be used to make a nested defaultdict
    """
    def init():
        """Instantiate a defaultdict with `factory` as argument"""
        return defaultdict(factory)
    return init
