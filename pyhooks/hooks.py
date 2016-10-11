from pyhooks.tags import collect_tags_by_hook, PRECALL_TAG, POSTCALL_TAG


class Hook(object):

    def __init__(self, method):
        self.method = method
        self.name = method.__name__

    def __call__(self, *args, **kwargs):
        self.run_tagged_methods(self.name, PRECALL_TAG, *args, **kwargs)
        return_value = self.method(self,*args, **kwargs)
        self.run_tagged_methods(self.name, POSTCALL_TAG, *args, **kwargs)
        return return_value

    def __get__(self, instance, owner):
        self.tags = collect_tags_by_hook(owner)
        self.instance = instance
        return self

    def run_tagged_methods(self, tag, location, *args, **kwargs):
        methods = self.tags[tag][location]
        for method in methods:
            method(self.instance, *args, **kwargs)


__all__ = ["Hook"]
