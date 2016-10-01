from collections import defaultdict
import inspect

from pyhooks.utils import decorator_with_args

TAG_STORE = "_pyhook_tags"
PRECALL_TAG_PREFIX = "pre_"
POSTCALL_TAG_PREFIX = "post_"


@decorator_with_args
def hook_register(function, *tag_names):
    """Tag a method to be picked up later"""
    tags = getattr(function, TAG_STORE, set())
    tags |= set(tag_names)
    setattr(function, TAG_STORE, tags)
    return function


@decorator_with_args
def precall_hook_register(function, *tag_names):
    """Tag a method to be run before the call to a method"""
    tag_names = [PRECALL_TAG_PREFIX + name for name in tag_names]
    return hook_register(*tag_names)(function)


@decorator_with_args
def postcall_hook_register(function, *tag_names):
    """Tag a method to be run after the call to a method"""
    tag_names = [POSTCALL_TAG_PREFIX + name for name in tag_names]
    return hook_register(*tag_names)(function)


@decorator_with_args
def call_hook(method, name):
    """Run the call hooks before and after calling the method"""
    def _wrapped(self, *args, **kwargs):
        self.run_hooks(PRECALL_TAG_PREFIX + name, *args, **kwargs)
        rv = method(self, *args, **kwargs)
        self.run_hooks(POSTCALL_TAG_PREFIX + name, *args, **kwargs)
    return _wrapped


class HookMeta(type):

    def __init__(self, name, bases, attrs, **kwargs):
        super(HookMeta, self).__init__(name, bases, attrs, **kwargs)
        self.__hooks__ = defaultdict(list)
        mro = inspect.getmro(self)

        for attr_name in dir(self):
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

            try:
                tag_names = getattr(attr, TAG_STORE)
            except AttributeError:
                continue

            for name in tag_names:
                # use name here so we can get the bound method later, in case
                # the processor was a descriptor or something.
                self.__hooks__[name].append(attr)
    

class HookableClass(metaclass=HookMeta):

    @classmethod
    def get_hook(cls, name):
        return cls.__hooks__[name]

    def run_hooks(self, name, *attrs, **kwargs):
        for method in self.get_hook(name):
            method(self, *attrs, **kwargs)


__all__ = ["hook_register", "HookableClass", "precall_hook_register",
           "postcall_hook_register", "call_hook"]
