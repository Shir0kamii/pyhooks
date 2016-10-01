from collections import defaultdict
import inspect

HOOK_STORE = "_pyhook_hooks"


def hook_register(*hook_names):
    """Tag a method to be picked up later"""
    def decorator(function):
        hooks = getattr(function, HOOK_STORE, set())
        hooks |= set(hook_names)
        setattr(function, HOOK_STORE, hooks)
        return function
    return decorator


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
                hook_names = getattr(attr, HOOK_STORE)
            except AttributeError:
                continue

            for name in hook_names:
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


__all__ = ["hook", "HookableClass"]
