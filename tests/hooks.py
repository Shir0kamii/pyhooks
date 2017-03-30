def test_method_still_runable_in_mother(mother_class):
    instance = mother_class()
    instance.method()
    assert hasattr(instance, "method_run")


def test_hooks_not_run_in_mother(mother_class):
    instance = mother_class()
    instance.method()
    assert not hasattr(instance, "precall_run")
    assert not hasattr(instance, "postcall_run")


def test_precall_method_run(child_class):
    instance = child_class()
    instance.method()
    assert hasattr(instance, "precall_run")


def test_postcall_method_run(child_class):
    instance = child_class()
    instance.method()
    assert hasattr(instance, "postcall_run")
