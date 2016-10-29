from collections import defaultdict, namedtuple

from pyhooks.utils import mrodir, decorator_with_args, defaultdict_factory

Tag = namedtuple("Tag", ["location", "name"])

TAG_STORE = "_pyhook_tags"

PRECALL_TAG = "precall"
POSTCALL_TAG = "postcall"


def bind_tags(function, tag_location, *tag_names):
    """Assign a location and names to a function"""
    binded_tags = getattr(function, TAG_STORE, set())
    tags_to_add = set(Tag(tag_location, tag) for tag in tag_names)
    tags = tags_to_add | binded_tags
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
def tag_register(function, location, *tag_names):
    """Decorates a function with location and names"""
    bind_tags(function, location, *tag_names)
    return function


@decorator_with_args
def precall_register(function, *tag_names):
    """Decorates a function with precall location and names"""
    bind_tags(function, PRECALL_TAG, *tag_names)
    return function


@decorator_with_args
def postcall_register(function, *tag_names):
    """Decorates a function with postcall location and names"""
    bind_tags(function, POSTCALL_TAG, *tag_names)
    return function


__all__ = ["bind_tags", "collect_tags_by_hook", "tag_register",
           "precall_register", "postcall_register"]
