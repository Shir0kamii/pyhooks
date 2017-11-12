from collections import defaultdict, namedtuple
from functools import partial

from pyhooks.utils import mrodir, decorator_with_args, defaultdict_factory

Tag = namedtuple("Tag", ["location", "name"])

TAG_STORE = "_pyhook_tags"

PRECALL_TAG = "precall"
POSTCALL_TAG = "postcall"


def bind_tags(function, tag_location, tag_name):
    """Assign a location and name to a function"""
    binded_tags = getattr(function, TAG_STORE, set())
    tags = set([Tag(tag_location, tag_name)]) | binded_tags
    setattr(function, TAG_STORE, tags)


def collect_tags_by_hook(cls):
    """Retrieve all tagged methods of a class and stored them in a dict

    All the tagged methods are stored in a nested dict with the form
    `dict[location][name]`
    """
    results = defaultdict(defaultdict_factory(list))
    for key, value in mrodir(cls):
        tags = getattr(value, TAG_STORE, None)
        if not tags:
            continue
        for tag in tags:
            results[tag.name][tag.location].append(value)
    return results


@decorator_with_args
def tag_register(function, location, tag_name):
    """Decorates a function with location and name"""
    bind_tags(function, location, tag_name)
    return function


precall_register = partial(tag_register, PRECALL_TAG)
postcall_register = partial(tag_register, POSTCALL_TAG)
before = precall_register
after = postcall_register

__all__ = ["after", "before", "bind_tags", "collect_tags_by_hook",
           "tag_register", "precall_register", "postcall_register"]
