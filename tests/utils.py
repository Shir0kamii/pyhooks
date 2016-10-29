from collections import defaultdict
from pyhooks import utils


def test_defaultdict_factory_return_initializer():
    default_dict_initializer = utils.defaultdict_factory(list)
    assert isinstance(default_dict_initializer(), defaultdict)
