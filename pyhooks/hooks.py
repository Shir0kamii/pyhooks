from pyhooks.tags import collect_tags_by_hook, PRECALL_TAG, POSTCALL_TAG


class Hook(object):
    """Decorate a method to make it hookable

    There are cureently two hooks available :
         - precall hooks, which are called before the call to the method
         - postcall hooks, which are called after the call to the method

    These two hooks are called with the arguments and keyword arguments passed
    to thw hooked method
    """

    def __init__(self, method):
        """Decorate the method"""
        self.method = method
        self.name = method.__name__

    def __call__(self, *args, **kwargs):
        """Run the hooks and the hooked method, respecting the location of
        hooks
        """
        self.run_tagged_methods(self.name, PRECALL_TAG, *args, **kwargs)
        return_value = self.method(self.instance, *args, **kwargs)
        self.run_tagged_methods(self.name, POSTCALL_TAG, *args, **kwargs)
        return return_value

    def __get__(self, instance, owner):
        """inspect the method's class to retrieve tagged methods (hooks)"""
        self.tags = collect_tags_by_hook(owner)
        self.instance = instance
        return self

    def run_tagged_methods(self, tag, location, *args, **kwargs):
        """Run the tagged methods corresponding to `tag` and `location`

        These methods are called with the remaining arguments and keyword
        arguments
        """
        methods = self.tags[tag][location]
        for method in methods:
            method(self.instance, *args, **kwargs)


__all__ = ["Hook"]
