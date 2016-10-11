from collections import defaultdict, namedtuple

from pyhooks.utils import mrodir, decorator_with_args

Tag = namedtuple("Tag", ["location", "name"])

TAG_STORE = "_pyhook_tags"

PRECALL_TAG = "precall"
POSTCALL_TAG = "postcall"


def bind_tags(function, tag_location, *tag_names):
    binded_tags = getattr(function, TAG_STORE, set())
    tags_to_add = set(Tag(tag_location, tag) for tag in tag_names)
    tags = tags_to_add | binded_tags
    setattr(function, TAG_STORE, tags)


def defaultdict_factory(factory):
    def init():
        return defaultdict(factory)
    return init


def collect_tags_by_hook(cls):
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
    bind_tags(function, location, *tag_names)
    return function


@decorator_with_args
def precall_register(function, *tag_names):
    bind_tags(function, PRECALL_TAG, *tag_names)
    return function


@decorator_with_args
def postcall_register(function, *tag_names):
    bind_tags(function, POSTCALL_TAG, *tag_names)
    return function


__all__ = ["bind_tags", "collect_tags_by_hook", "tag_register",
           "precall_register", "postcall_register"]
