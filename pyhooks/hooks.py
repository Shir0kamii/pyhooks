from collections import defaultdict
import inspect

from pyhooks.utils import decorator_with_args

TAG_STORE = "_pyhook_tags"
PRECALL_TAG_PREFIX = "pre_"
POSTCALL_TAG_PREFIX = "post_"


def bind_tags_to_function(function, *tag_names):
    binded_tags = getattr(function, TAG_STORE, set())
    tags = set(tag_names)
    setattr(function, TAG_STORE, tags)


@decorator_with_args
def hook_register(function, *tag_names):
    """Tag a method to be picked up later"""
    bind_tags_to_function(function, *tag_names)
    return function


@decorator_with_args
def precall_hook_register(function, *tag_names):
    """Tag a method to be run before the call to a method"""
    tag_names = [PRECALL_TAG_PREFIX + name for name in tag_names]
    bind_tags_to_function(function, *tag_names)
    return function


@decorator_with_args
def postcall_hook_register(function, *tag_names):
    """Tag a method to be run after the call to a method"""
    tag_names = [POSTCALL_TAG_PREFIX + name for name in tag_names]
    bind_tags_to_function(function, *tag_names)
    return function


@decorator_with_args
def call_hook(method, name):
    """Run the call hooks before and after calling the method"""
    def _wrapped(self, *args, **kwargs):
        self.run_hooks(PRECALL_TAG_PREFIX + name, *args, **kwargs)
        rv = method(self, *args, **kwargs)
        self.run_hooks(POSTCALL_TAG_PREFIX + name, *args, **kwargs)
    return _wrapped


class HookableClass():

    def __init__(self):
        self.register_hooks()

    @classmethod
    def register_hooks(cls):
        if hasattr(cls, "__hooks__"):
            return
        cls.__hooks__ = defaultdict(list)
        for _, value in cls.iter_real_attrs():
            try:
                tag_names = getattr(value, TAG_STORE)
            except AttributeError:
                continue

            for name in tag_names:
                cls.__hooks__[name].append(value)

    @classmethod
    def iter_real_attrs(cls):
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

    @classmethod
    def get_hook(cls, name):
        return cls.__hooks__[name]

    def run_hooks(self, name, *attrs, **kwargs):
        for method in self.get_hook(name):
            method(self, *attrs, **kwargs)


__all__ = ["hook_register", "HookableClass", "precall_hook_register",
           "postcall_hook_register", "call_hook"]
