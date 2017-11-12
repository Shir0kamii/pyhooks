from collections import defaultdict

from pyhooks import tags, after


def test_bind_tags_use_tag_store(method):
    assert hasattr(method, tags.TAG_STORE)


def test_bind_tags_store_Tag(method):
    assert all(isinstance(stored_element, tags.Tag)
               for stored_element in getattr(method, tags.TAG_STORE))


def test_bind_tags_api(method):
    assert all(tag.location in ("precall", "postcall") and
               tag.name == "method"
               for tag in getattr(method, tags.TAG_STORE))


def test_collect_tags_by_hook_return_defaultdict(child_class):
    collected_tags = tags.collect_tags_by_hook(child_class)
    assert isinstance(collected_tags, defaultdict)


def test_collect_only_tagged_methods(child_class):
    collected_tags = tags.collect_tags_by_hook(child_class)
    for locations in collected_tags.values():
        for methods in locations.values():
            for method in methods:
                test_bind_tags_use_tag_store(method)
                test_bind_tags_store_Tag(method)
                test_bind_tags_api(method)


def test_after(mother_class):
    class Child(mother_class):
        @after("method")
        def test_method(self):
            self.test = 42
    obj = Child()
    obj.method()
    assert obj.test == 42
